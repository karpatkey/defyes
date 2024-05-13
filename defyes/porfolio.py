import logging
import inspect
from functools import cached_property

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr
from defyes.prices import Chainlink as chainlink

from .contracts import Erc20

logger = logging.getLogger(__name__)

def default(method):
    if inspect.isgeneratorfunction(method):
        def wrapper(self):
            return list(method(self))
    else:
        def wrapper(self):
            return method(self)
    return cached_property(wrapper)

class AssetManager(list):
    unique = dict()

    def add(self, obj):
        h = hash(obj)
        new_i = len(self)
        i = self.unique.setdefault(h, new_i)
        if i != new_i:
            raise ValueError(f"Already defined instance (current:{self[i]}, new:{obj}")
        else:
            self.append(obj)

    def __get__(self, instance, owner=None):
        if owner is BaseAsset:
            return self
        else:
            return AssetManager(ins for ins in self if isinstance(ins, owner))

    def filter(self, **kwargs):
        for ins in self:
            if all(getattr(ins, attr, None) == value for attr, value in kwargs.items()):
                yield ins

    def __call__(self, **kwargs):
        return AssetManager(self.filter(**kwargs))

    def get(self, **kwargs):
        return next(self.filter(**kwargs))


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


class BaseAsset:
    """
    No magical alternative to mitigate the extreme complexity of dataclasses when dealing with inheritance.
    """

    def __init__(self, /, **attrs):
        """
        Set all keyword arguments defined by `attrs` as instance attributes.
        Add the instance to the asset instances list.
        Call __post_init__, like dataclass.
        """
        self.__dict__.update(attrs)
        BaseAsset.instances.add(self)
        self.__post_init__()

    instances = AssetManager()

    def __post_init__(self):
        """
        Override this method in subclasses instead of __init__.
        """

    def __setattr__(self, name, value):
        """
        Make derivative clases with "fozen" instances to reduce incoherent states and all the good behaviours of
        inmutable data ;)
        """
        raise Exception("read-only")


class Asset(BaseAsset):
    symbol: str
    name: str
    price_usd: float

    __repr__ = repr_for("symbol")

    def __hash__(self):
        return hash(self.symbol)

class Price(Decimal):
    symbol: str
    name: str
    source: str
    blockchain: Blockchain

class Crypto(Asset):
    def __getitem__(self, block):
        new_instance = self.__class__()
        new_instance.__dict__ = self.__dict__.copy()



class Native(Crypto):
    chain: Blockchain
    decimals: int = 18

    __repr__ = repr_for("chain", "symbol")

    def __hash__(self):
        return self.chain.chain_id

    def price(self) -> Price:
        value = chainlink.get_native_token_price(self.node, block="latest", self.blockchain)
        #, "chainlink", blockchain


Native(chain=Chain.ETHEREUM, symbol="ETH", name="Ether")
Native(chain=Chain.POLYGON, symbol="MATIC", name="Matic")
Native(chain=Chain.GNOSIS, symbol="xDAI", name="Gnosis native DAI")





class Deployment:
    chain: Blockchain
    address: str
    deploy_block: int | None = None

    @default
    def deployment(self):
        """Get the token ERC20 contract."""
        return self.contract(self.chain, block="latest", address=self.address)
        # TODO: Fix block using nodetime.
        # TODO: discrimitate contract class as a function of chain (and address)


class Token(Deployment, Crypto):
    contract = Erc20

    @default
    def symbol(self) -> str:
        return self.deployment.symbol

    @default
    def name(self) -> str:
        return self.deployment.name

    @property
    def price(self) -> Price:
        price, _, _ = get_price_in_usd(self.address, self.block, self.chain)
        return price

    @default
    def decimals(self) -> int:
        return self.deployment.decimals

    __repr__ = repr_for("chain", "symbol")

    def __hash__(self):
        return hash((self.chain.chain_id, self.address))


USDCe = Token(chain=Chain.POLYGON, address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174", symbol="USDC.e")


def discover_defabipedia_tokens():
    from defabipedia import tokens

    for chain, container_class in tokens.Addresses.items():
        for attr_name, attr_value in vars(container_class).items():
            if not attr_name.startswith("_") and isinstance(attr_value, str):
                try:
                    Token(chain=chain, symbol=attr_name, address=attr_value)
                except ValueError as e:
                    logger.error(f"{e!s}")
                    print(e)


discover_defabipedia_tokens()

"""
    amount: Amount
    @property
    def amount(self) -> Amount:
        raise NotImplemented
Asset (like Unit) add
|- Token (ERC20) add Deploy
|- PositionClass add Deploy underlying:set[AssetAmount] unclaimed_rewards:set[AssetAmount]
|- ...
|- Native add FakeDeploy
|- Fiat
|- DelegatedNative add Native real_address:str
|- DelegatedToken add Token real_address:str
|- DelegatedAsset add Asset delegated:Asset
"""

def public_attrs_dict(class_) -> dict[str, Module]:
    return {name: attr for name, attr in vars(class_).items() if not name.startswith("_")}


@public_attrs_dict
class compatible_protocol:
    from defyes.protocols import maker


class Porfolio(Init, Frozen):
    wallet: str
    blockchain: Blockchain
    block: int

    @default
    def crypto_set(self) -> set[Crypto]:
        return {*Native.intances, *Token.instances}

    @default
    def elementary_crypto(self) -> set[Crypto]:
        return {*Native.intances, *Token.instances}

    def __iter__(self) -> Iterator[list[Crypto]]
        porfolio: list[Crypto] = list(self.cryptos)
        while True:
            yield porfolio
            porfolio = [
                *crypto.underlyings for crypto in porfolio if crypto not in self.elementary_crypto
            ]
            if has_just(porfolio, self.elementary_crypto):
                break

    @default
    def cryptos(self):
        for protocol in compatible_protocols:

            for token in protocol.tokens:
                if token.chain == self.blockchain:
                    yield token.amount(self.wallet, self.block)

            for position in protocol.Positions(self.wallet, self.blockchain, self.block)
                yield position.underlyings
                yield position.unclaimed_rewards



