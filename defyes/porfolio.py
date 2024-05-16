import inspect
import logging
from decimal import Decimal
from functools import cached_property
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr, erc20_contract
from karpatkit.node import get_node

from defyes.lazytime import Time
from defyes.prices import Chainlink as chainlink
from defyes.prices.prices import get_price as get_price_in_usd

Module = type(logging)

logger = logging.getLogger(__name__)


def default(method):
    if inspect.isgeneratorfunction(method):

        def wrapper(self):
            return list(method(self))

    else:

        def wrapper(self):
            return method(self)

    return cached_property(wrapper)


def repr_for(*attrs):
    """
    Easy create your class repr function including the specific attributes `attrs`.

    class A:
        ...
        __repr__ = repr_for("a", "b")

    repr(A(...)) -> "A(a=1, b=2)"
    """

    def __repr__(self):
        pairs = ", ".join(f"{name}={getattr(self, name)!r}" for name in attrs)
        return f"{self.__class__.__name__}({pairs})"

    return __repr__


class KwInit:
    """
    No magical alternative to mitigate the extreme complexity of dataclasses when dealing with inheritance.
    """

    def __init__(self, /, **attrs):
        """
        Set all keyword arguments defined by `attrs` as instance attributes.
        Call __post_init__, like dataclass.
        """
        self.__dict__.update(attrs)
        self.__post_init__()

    def __post_init__(self):
        """
        Override this method in subclasses instead of __init__.
        """


class Frozen:
    def __setattr__(self, name, value):
        """
        Make derivative clases with "fozen" instances to reduce incoherent states and all the good behaviours of
        inmutable data ;)
        """
        raise Exception("read-only")


class Fiat(float):
    source: str
    symbol: str

    def __repr__(self) -> str:
        return f"Fiat({super()}, symbol={self.symbol}, source={self.source})"

    def __str__(self) -> str:
        return f"{super()} {self.symbol}"

    def __mul__(self, other: float) -> "Fiat":
        return Fiat(float(other) * float(self), source=self.source, symbol=self.symbol)

    __rmul__ = __mul__


class USDPrice(Fiat):
    symbol: str = "USD"


class InstancesManager(list):
    unique = dict()

    def __set_name__(self, owner, name):
        self.initial_class_owner = owner

    def __get__(self, instance, owner=None):
        if owner is self.initial_class_owner:
            return self
        else:
            return InstancesManager(ins for ins in self if isinstance(ins, owner))

    def add(self, obj):
        h = hash(obj)
        new_i = len(self)
        i = self.unique.setdefault(h, new_i)
        if i != new_i:
            raise ValueError(f"Already defined instance (current:{self[i]}, new:{obj}")
        else:
            self.append(obj)

    def filter(self, **kwargs):
        for ins in self:
            if all(getattr(ins, attr, None) == value for attr, value in kwargs.items()):
                yield ins

    def __call__(self, **kwargs):
        return InstancesManager(self.filter(**kwargs))

    def get(self, **kwargs):
        return next(self.filter(**kwargs))

    def get_or_create(self, *a, **b):
        print("Not implemented", self, a, b)


class Token(Frozen, KwInit):
    chain: Blockchain
    symbol: str
    name: str
    # price: Fiat
    decimals: int = 18

    __repr__ = repr_for("chain", "symbol")

    instances = InstancesManager()

    def __post_init__(self):
        super().__post_init__()
        Token.instances.add(self)

    def __hash__(self):
        return hash(self.symbol)

    def __set_name__(self, owner, symbol: str):
        """
        Allows to set the symbol from the class attribute name by default.
            class X:
                ETH = Token(chain=..., name=...)  # symbol -> "ETH"

        Anyways, an override during initialization has priority.
            class X:
                USDCe = Token(chain=..., name=..., symbol="USDC.e")  # symbol -> "USDC.e"
        """
        self.__dict__["symbol"] = symbol


class NativeToken(Token):
    def __hash__(self):
        return self.chain.chain_id

    def price(self, block: int) -> Fiat:
        value = chainlink.get_native_token_price(self.node, block, self.chain)
        return USDPrice(value, source="chainlink")


NativeToken(chain=Chain.ETHEREUM, symbol="ETH", name="Ether")
NativeToken(chain=Chain.POLYGON, symbol="MATIC", name="Matic")
NativeToken(chain=Chain.GNOSIS, symbol="xDAI", name="Gnosis native DAI")


class Deployment:
    contract: type
    address: str
    deploy_block: int | None = None


class ERC20Token(Deployment, Token):
    @default
    def contract(self):
        node = get_node(self.chain)
        return erc20_contract(node, self.address)

    @default
    def symbol(self) -> str:
        return self.contract.functions.symbol()

    @default
    def name(self) -> str:
        return self.contract.functions.name()

    def price(self, block: int) -> Fiat:
        price, source, _ = get_price_in_usd(self.address, block, self.chain)
        return USDPrice(price, source=source)

    @default
    def decimals(self) -> int:
        return self.contract.functions.decimals()

    __repr__ = repr_for("chain", "symbol")

    def __hash__(self):
        return hash((self.chain.chain_id, self.address))

    def amount_of(self, wallet: str, block: int) -> "TokenAmount":
        return TokenAmount(token=self, wallet=wallet, block=block)


class Unwrappable:
    unwrapped_token: Token

    def unwrapping_rate(self, block: int) -> float:
        raise NotImplementedError


USDCe = ERC20Token(chain=Chain.POLYGON, address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", symbol="USDC.e")


class USDCe(ERC20Token):
    chain = Chain.POLYGON
    address = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
    symbol = "USDC.e"


class Asset(Frozen, KwInit):
    """
    Something with value. Not a type of value.
    """

    underlyings: list["Asset"] = list()
    unclaimed_rewards: list["Asset"] = list()
    __repr__ = repr_for()


class Position(Asset):
    """
    A unit of finantial value.
    """


class TokenAmount(Token, Asset):
    """
    A value/balance for a Token.
    """

    __repr__ = repr_for("amount", "token")
    token: Token
    block: int
    wallet: str
    amount: Decimal | None
    amount_teu: int | None

    @default
    def amount(self) -> Decimal:
        """
        Amount in terms of units of the token.
        """
        return Decimal(self.amount_teu).scaleb(-self.token.decimals)

    @default
    def amount_teu(self) -> int:
        """
        Amount in terms of the minimun fraction of the token.
        """
        return self.token.contract.functions.balanceOf(self.wallet).call(block_identifier=self.block)

    @default
    def amount_usd(self) -> Fiat:
        """
        Amount in USD
        """
        return float(self.amount) * self.token.price(self.block)

    @default
    def underlyings(self) -> list[Asset]:
        """
        Returns just one TokenAmount in the list, which is the unwrapped token with its converted value.
        """
        if isinstance(self.token, Unwrappable):
            yield TokenAmount(
                token=self.token.unwrapped_token, amount=self.amount * self.token.unwrapping_rate(self.block)
            )

    @property
    def time(self) -> Time:
        if isinstance(self.block, int):
            return Time(self.token.deployment.w3.eth.get_block(self.block)["timestamp"])
        else:
            raise ValueError("Undefined time, because `block` isn't defined as an integer.")


class UnderlyingTokenAmount(TokenAmount):
    """
    A value but not a balance for a Token.
    """

    block: int | None = None
    wallet: str | None = None

    @default
    def amount_teu(self) -> int:
        """
        Amount in terms of the minimun fraction of the token.
        """
        return int(self.amount.scaleb(self.token.decimals))

    def __post_init__(self):
        """
        Check that at least `amount` or `amout_teu` is defined, to avoid circular recursion.
        """
        super().__post_init__()
        if self.__dict__["amount"] is None and self.__dict__["amount_teu"] is None:
            raise ValueError("At least one of either `amount` or `amount_teu` must be defined.")


def discover_defabipedia_tokens():
    from defabipedia import tokens

    for chain, container_class in tokens.Addresses.items():
        for attr_name, attr_value in vars(container_class).items():
            if not attr_name.startswith("_") and isinstance(attr_value, str):
                try:
                    ERC20Token(chain=chain, symbol=attr_name, address=attr_value)
                except ValueError as e:
                    logger.error(f"{e!s}")
                    print(e)


discover_defabipedia_tokens()


# class Crypto(Asset):
#    def __getitem__(self, block):
#        new_instance = self.__class__()
#        new_instance.__dict__ = self.__dict__.copy()
#
# USDC = Crpto(......)
# USDC[1883747463]
# USDC.__getitem__(1888...)

"""
    amount: Amount
    @property
    def amount(self) -> Amount:
        raise NotImplemented
Asset (like Unit) add
|- ERC20Token (ERC20) add Deploy
|- PositionClass add Deploy underlying:set[AssetAmount] unclaimed_rewards:set[AssetAmount]
|- ...
|- NativeToken add FakeDeploy
|- Fiat
|- DelegatedNativeToken add NativeToken real_address:str
|- DelegatedERC20Token add ERC20Token real_address:str
|- DelegatedAsset add Asset delegated:Asset

TODO:

"""


def public_attrs_dict(class_) -> dict[str, Module]:
    return {name: attr for name, attr in vars(class_).items() if not name.startswith("_")}


@public_attrs_dict
class compatible_protocols:
    pass  # from .protocols import maker


class Porfolio(Frozen, KwInit):
    wallet: str
    chain: Blockchain
    block: int
    included_protocols_name: set[str] = set(compatible_protocols.keys())

    @default
    def included_tokens(self) -> set[Token]:
        """
        All tokens by default.
        """
        return set(Token.instances)

    @default
    def target_tokens(self) -> set[Token]:
        """
        Not unwrappable tokens by default.
        """
        return set(token for token in Token.intances if not isinstance(token, Unwrappable))

    def __iter__(self) -> Iterator[list[Token]]:
        porfolio: list[Asset] = list(self.assets)
        while True:
            yield porfolio
            porfolio = [sub_asset for sub_asset in asset.underlyings for asset in porfolio]
            if has_just(porfolio, self.target_tokens):
                break

    @default
    def protocols(self):
        for name, module in compatible_protocols.items():
            if name in self.included_protocols_name:
                yield module

    @default
    def assets(self):
        for protocol in self.protocols:
            for token in protocol.tokens:
                if token.chain == self.chain and token in self.included_tokens:
                    yield token.amount(self.wallet, self.block)

            for position in protocol.Positions(self.wallet, self.chain, self.block):
                yield from position.underlyings
                yield from position.unclaimed_rewards
