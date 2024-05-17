import inspect
import logging
from decimal import Decimal
from functools import cached_property
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr, erc20_contract
from karpatkit.node import get_node
from web3 import Web3

from defyes.contracts import Erc20
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
    source: str | None = None
    symbol: str | None = None

    def __init__(self, value, *, source=None):
        super().__init__()
        self.source = source

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({float(self)}, source={self.source!r})"

    def __str__(self) -> str:
        return f"{float(self)} {self.symbol}"

    def __mul__(self, other: float) -> "Fiat":
        return self.__class__(float(other) * float(self), source=self.source)

    __rmul__ = __mul__


class USD(Fiat):
    symbol: str = "USD"


class InstancesManager(list):
    unique = dict()

    def __set_name__(self, owner, name):
        self.initial_class_owner = owner

    @property
    def current_class_owner(self):
        raise NotImplementedError("Pending")

    def __get__(self, instance, owner=None):
        if owner is self.initial_class_owner:
            return self
        else:
            return InstancesManager(ins for ins in self if isinstance(ins, owner))

    def add(self, obj):
        self.append(obj)
        return
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
        try:
            return next(self.filter(**kwargs))
        except StopIteration:
            raise LookupError(f"No instance found in {self.__class__} for {kwargs!r}.")

    def get_or_create(self, **kwargs):
        try:
            return self.get(**kwargs)
        except LookupError:
            return self.current_class_owner(**kwargs)


class Crypto(Frozen, KwInit):
    chain: Blockchain
    node: Web3


class Token(Crypto):
    symbol: str
    name: str
    price: Fiat
    decimals: int
    protocol: str | None = None

    __repr__ = repr_for("chain", "symbol", "protocol")

    instances = InstancesManager()
    objs = instances

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
        self.__dict__["protocol"] = _get_protocol_from_module(owner.__module__)


def _get_protocol_from_module(module: str) -> str | None:
    prev_part = None
    for part in reversed(module.split(".")):
        if part == "protocols":
            return prev_part
        prev_part = part


class NativeToken(Token):
    decimals: int = 18

    @default
    def node(self) -> Web3:
        return get_node(self.chain)

    def __hash__(self):
        return self.chain.chain_id

    def price(self, block: int) -> Fiat:
        value = chainlink.get_native_token_price(self.node, block, self.chain)
        return USD(value, source="chainlink")

    def balance_of(self, wallet: str, block: int) -> int:
        return self.node.eth.get_balance(wallet, block)


NativeToken(chain=Chain.ETHEREUM, symbol="ETH", name="Ether")
NativeToken(chain=Chain.POLYGON, symbol="MATIC", name="Matic")
NativeToken(chain=Chain.GNOSIS, symbol="xDAI", name="Gnosis native DAI")


class Deployment:
    abi_class: type
    address: str | None = None
    # deploy_block: int | None = None

    @default
    def abi(self):
        return self.abi_class(self.chain, "latest", self.address)

    @default
    def node(self) -> Web3:
        return self.abi.contract.w3


class DeploymentCrypto(Deployment, Crypto):
    pass


class ERC20Token(Deployment, Token):
    abi_class: type = Erc20

    @default
    def symbol(self) -> str:
        return self.abi.symbol

    @default
    def name(self) -> str:
        return self.abi.name

    @default
    def decimals(self) -> int:
        return self.abi.decimals

    def price(self, block: int) -> Fiat:
        price, source, _ = get_price_in_usd(self.address, block, self.chain)
        return USD(price, source=source)

    def __hash__(self):
        return hash((self.chain.chain_id, self.address))

    def balance_of(self, wallet: str, block: int) -> int:
        self.abi.block = block  # TODO: improve this workarround
        return self.abi.balance_of(wallet)

    def amount_of(self, wallet: str, block: int) -> "TokenAmount":
        return TokenAmount(token=self, wallet=wallet, block=block)


class Unwrappable:
    unwrapped_token: Token

    def unwrap(self, tokenamount: "TokenAmount") -> "UnderlyingTokenAmount":
        raise NotImplementedError


USDCe = ERC20Token(
    chain=Chain.POLYGON,
    address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    symbol="USDC.e",
)


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
    __repr__ = repr_for("underlyings", "unclaimed_rewards")

    def __bool__(self):
        return bool(self.underlyings) or bool(self.unclaimed_rewards)


class TokenAmount(Asset):
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
        Amount in terms of units of the token. Calculated from TEU and decimals.
        """
        return Decimal(self.amount_teu).scaleb(-self.token.decimals)

    @default
    def amount_teu(self) -> int:
        """
        Amount in terms of TEU (the minimun fraction of the token). Got from the token balance_of.
        """
        return self.token.balance_of(self.wallet, self.block)

    @default
    def amount_fiat(self) -> Fiat:
        """
        Amount in Fiat (mainly USD). Converted to Fiat using the token price.
        """
        return float(self.amount) * self.token.price(self.block)

    @default
    def underlyings(self) -> list["UnderlyingTokenAmount"]:
        """
        Returns one UnderlyingTokenAmount or zero in the list, which is the unwrapped token with its converted value.
        """
        if isinstance(self.token, Unwrappable):
            yield self.token.unwrap(self)

    @default
    def time(self) -> Time:
        if isinstance(self.block, int):
            return Time(self.token.node.eth.get_block(self.block).timestamp)
        else:
            raise ValueError("Undefined time, because `block` isn't defined as an integer.")

    def __bool__(self):
        return self.amount_teu != 0


class UnderlyingTokenAmount(TokenAmount):
    """
    An underlying value/balance for a Token.
    """

    block: int | None = None
    wallet: str | None = None
    parent: Asset | None = None

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
        if not {"amount", "amount_teu"}.intersection(self.__dict__):
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
    from .protocols.maker import newarch as maker

discover_defabipedia_tokens()

class Porfolio(Frozen, KwInit):
    chain: Blockchain
    block: int
    wallet: str
    included_protocols_name: set[str] = set(compatible_protocols.keys())

    @default
    def included_tokens(self) -> set[Token]: # TODO: no conviene tirar aunque no se conozcan. solamente filtrar para tokenamount, no para underlyings
        """
        All tokens by default.
        """
        return set(Token.instances)

    @default
    def target_tokens(self) -> set[Token]:
        """
        Not unwrappable tokens by default.
        """
        return set(token for token in Token.instances if not isinstance(token, Unwrappable))

    def __iter__(self) -> Iterator[list[Token]]:
        porfolio: list[Asset] = list(self.assets)
        while True:
            yield porfolio
            if self.has_just_target_tokens(porfolio):
                break
            porfolio = list(self.deeper(porfolio))

    def has_just_target_tokens(self, porfolio):
        return False
        #if target_tokens.intersection({ta.token for ta in porfolio if ta)

    def deeper(self, porfolio):
        for position in porfolio:
            # Stop underlying/unwrapping on target tokens
            if hasattr(position, "token") and position.token in self.target_tokens:
                yield position
                continue

            for underlying in position.underlyings:
                underlying.__dict__["parent"] = position
                yield underlying

            for unclaimed_reward in position.unclaimed_rewards:
                unclaimed_reward.__dict__["parent"] = position
                yield unclaimed_reward
    @default
    def protocols(self) -> dict[str, Module]:
        return {
            name: module
            for name, module in compatible_protocols.items()
            if name in self.included_protocols_name
        }

    @default
    def assets(self):
        for protocol_name, protocol in self.protocols.items():
            for token in Token.instances.filter(chain=self.chain, protocol=protocol_name):
                if token.chain == self.chain and token in self.included_tokens:
                    tokenamount = token.amount_of(self.wallet, self.block)
                    yield tokenamount

            yield from protocol.Positions(wallet=self.wallet, chain=self.chain, block=self.block)

    @default
    def token_positions(self):
        for token in self.included_tokens:
            if token.chain == self.chain:
                yield token.amount_of(self.wallet, self.block)


def initial_protocol(position):
    while hasattr(position, "parent"):
        position = position.parent
    try:
        return position.protocol
    except AttributeError:
        try:
            return position.token.protocol
        except AttributeError:
            return None
