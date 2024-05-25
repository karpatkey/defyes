import importlib
import inspect
import logging
import time
from collections import defaultdict
from decimal import Decimal
from functools import cached_property, wraps
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.node import get_node
from web3 import Web3

from defyes.contracts import Erc20
from defyes.lazytime import Duration, Time
from defyes.prices import Chainlink as chainlink
from defyes.prices.prices import get_price as get_price_in_usd

Module = type(logging)

logger = logging.getLogger(__name__)


def timeit(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        t0 = time.monotonic()
        result = method(self, *args, **kwargs)
        t1 = time.monotonic()
        attr = f"{method.__name__}_timeit"
        try:
            ti = self.__dict__[attr]
        except KeyError:
            ti = {}
        cumsum = ti.get("cumsum", 0)
        n_calls = ti.get("n_calls", 0)
        duration = Duration.seconds(t1 - t0)
        cumsum += duration
        n_calls += 1
        self.__dict__[attr] = {
            "last_call": {"duration": duration, "args": args, "kwargs": kwargs},
            "cumsum": cumsum,
            "n_calls": n_calls,
        }
        return result

    return wrapper


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


def repr_dict():
    def __repr__(self):
        pairs = ", ".join(f"{name}={value!r}" for name, value in vars(self).items())
        return f"{self.__class__.__name__}({pairs})"

    return __repr__


class FrozenKwInit:
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
        return f"{self.__class__.__name__}({format(float(self), '_')}, source={self.source!r})"

    def __str__(self) -> str:
        return f"{format(float(self), '_')} {self.symbol}"

    def __mul__(self, other: float) -> "Fiat":
        return self.__class__(float(other) * float(self), source=self.source)

    __rmul__ = __mul__


class USD(Fiat):
    symbol: str = "USD"


class InstancesManager(list):
    unique = dict()

    def __new__(cls, seq: Iterator = None, *, current_class_owner=None, **kwargs):
        self = super().__new__(cls, seq)
        if current_class_owner:
            self.current_class_owner = current_class_owner
        return self

    def __set_name__(self, owner, name):
        self.initial_class_owner = owner

    @default
    def current_class_owner(self):
        return self.initial_class_owner

    def __get__(self, instance, owner=None):
        if owner is self.initial_class_owner:
            return self
        else:
            if instance:
                gen = (obj for obj in self if self._alike(instance, obj))
            else:
                gen = (obj for obj in self if isinstance(obj, owner))
            return InstancesManager(gen, current_class_owner=owner)

    @staticmethod
    def _alike(instance, obj):
        return all(getattr(obj, attr) == getattr(instance, attr) for attr in instance.filter_attrs)

    def filter(self, **kwargs):
        for obj in self:
            if all(getattr(obj, attr, None) == value for attr, value in kwargs.items()):
                yield obj

    def __call__(self, **kwargs):
        return InstancesManager(self.filter(**kwargs))

    def get(self, **kwargs):
        iteration = self.filter(**kwargs)
        try:
            obj = next(iteration)
        except StopIteration:
            raise LookupError(f"No instance found in {self.__class__} for {kwargs!r}.")
        try:
            next(iteration)
        except StopIteration:
            return obj  # OK. Just one object.
        else:
            raise ValueError(f"Just one object expected. There are multiple objects for the filter {kwargs!r}")

    def create(self, **kwargs):
        obj = self.current_class_owner(**kwargs)
        return obj

    def add(self, obj):
        """
        Add a new obj. Replace if it already exists.
        """
        obj_hash = hash(obj)
        try:
            i = self.unique[obj_hash]
        except KeyError:
            self.unique[obj_hash] = len(self)
            self.append(obj)
        else:
            self[i] = obj

    def get_or_create(self, **kwargs):
        try:
            return self.get(**kwargs)
        except LookupError:
            return self.current_class_owner(**kwargs)


class Token(FrozenKwInit):
    node: Web3
    chain: Blockchain
    symbol: str
    name: str
    price: Fiat
    decimals: int
    protocol: str | None = None
    filter_attrs: set[str] = {"chain"}

    __repr__ = repr_for("chain", "symbol", "protocol")

    objs = InstancesManager()

    def __post_init__(self):
        super().__post_init__()
        Token.objs.add(self)

    def __hash__(self):
        return hash(self.symbol)


class NativeToken(Token):
    decimals: int = 18

    @default
    def node(self) -> Web3:
        return get_node(self.chain)

    def __hash__(self):
        return self.chain.chain_id

    @timeit
    def price(self, block: int) -> Fiat:
        value = chainlink.get_native_token_price(self.node, block, self.chain)
        return USD(value, source="chainlink")

    def balance_of(self, wallet: str, block: int) -> int:
        return self.node.eth.get_balance(wallet, block)

    def position_of(self, wallet: str, block: int) -> "TokenPosition":
        return TokenPosition(token=self, wallet=wallet, block=block)


class Deployment:
    contract_class: type
    address: str | None = None
    deployed_block: int | str = "latest"

    @default
    def address(self):
        return self.contract_class.default_addresses[self.chain]

    @default
    def contract(self):
        return self.contract_class(self.chain, self.deployed_block, self.address)

    @default
    def node(self) -> Web3:
        return self.contract.contract.w3


class DeployedToken(Deployment, Token):
    contract_class: type = Erc20

    @default
    def symbol(self) -> str:
        return self.contract.symbol

    @default
    def name(self) -> str:
        return self.contract.name

    @default
    def decimals(self) -> int:
        return self.contract.decimals

    @timeit
    def price(self, block: int) -> Fiat:
        price, source, _ = get_price_in_usd(self.address, block, self.chain)
        return USD(price if price else float("nan"), source=source)

    def __hash__(self):
        return hash((self.chain.chain_id, self.address))

    def balance_of(self, wallet: str, block: int) -> int:
        return self.contract.contract.functions.balanceOf(wallet).call(block_identifier=block)

    def position_of(self, wallet: str, block: int) -> "TokenPosition":
        return TokenPosition(token=self, wallet=wallet, block=block)


class Unwrappable:
    def unwrap(self, token_position: "TokenPosition") -> list["UnderlyingTokenPosition"]:
        raise NotImplementedError


class Position(FrozenKwInit):
    """
    A finantial value.
    """

    wallet: str
    chain: Blockchain
    block: int
    protocol: str | None = None
    underlyings: list["Position"] = list()
    unlaimed_rewards: list["Position"] = list()

    __repr__ = repr_dict()

    def __bool__(self):
        return bool(self.underlyings) or bool(self.unclaimed_rewards)


class TokenPosition(Position):
    """
    A value/balance for a Token.
    """

    __repr__ = repr_for("amount", "token")
    token: Token
    amount: Decimal | None
    amount_teu: int | None

    @default
    def amount(self) -> Decimal:
        """
        Amount in terms of units of the token. Calculated from TEU and decimals.
        """
        return Decimal(self.amount_teu).scaleb(-self.token.decimals) if self else Decimal(0)

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
    def underlyings(self) -> list["UnderlyingTokenPosition"]:
        """
        Returns one UnderlyingTokenPosition or zero in the list, which is the unwrapped token with its converted value.
        """
        if isinstance(self.token, Unwrappable):
            yield from self.token.unwrap(self)

    @default
    def time(self) -> Time:
        if isinstance(self.block, int):
            return Time(self.token.node.eth.get_block(self.block).timestamp)
        else:
            raise ValueError("Undefined time, because `block` isn't defined as an integer.")

    @default
    def protocol(self) -> str:
        return self.token.protocol

    @default
    def chain(self) -> str:
        return self.token.chain

    def __bool__(self):
        return self.amount_teu != 0


class UnderlyingTokenPosition(TokenPosition):
    """
    An underlying value/balance for a Token.
    """

    parent: Position | None = None

    @default
    def amount_teu(self) -> int:
        """
        Amount in terms of the minimun fraction of the token.
        """
        return int(self.amount.scaleb(self.token.decimals))

    def __post_init__(self):
        """
        Check that at least `amount` or `amount_teu` is defined, to avoid circular recursion.
        """
        if not {"amount", "amount_teu"}.intersection(self.__dict__):
            raise ValueError("At least one of either `amount` or `amount_teu` must be defined.")


#### Some token definitions

ETH = NativeToken(chain=Chain.ETHEREUM, symbol="ETH", name="Ether")
NativeToken(chain=Chain.POLYGON, symbol="MATIC", name="Matic")
NativeToken(chain=Chain.GNOSIS, symbol="xDAI", name="Gnosis native DAI")


DeployedToken(
    chain=Chain.POLYGON,
    address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    symbol="USDC.e",
)


class WETHToken(Unwrappable, DeployedToken):
    chain = Chain.ETHEREUM
    address = EthereumTokenAddr.WETH

    def unwrap(self, token_position: "TokenPosition") -> list["UnderlyingTokenPosition"]:
        return [UnderlyingTokenPosition(token=ETH, amount=token_position.amount, parent=token_position)]


WETHToken()

###


compatible_protocols = {
    name: importlib.import_module(f"defyes.protocols.{name}.newarch") for name in {"aura", "balancer", "maker", "lido"}
}


class Porfolio(FrozenKwInit):
    chain: Blockchain
    block: int
    wallet: str
    included_protocols_name: set[str] = set(compatible_protocols.keys())

    __repr__ = repr_for("chain", "block", "wallet")

    # TODO: no conviene tirar aunque no se conozcan. solamente filtrar para token_position, no para underlyings
    @default
    def included_tokens(self) -> set[Token]:
        """
        All tokens for this chain by default.
        """
        return set(Token.objs.filter(chain=self.chain))

    @default
    def target_tokens(self) -> set[Token]:
        """
        Not unwrappable tokens by default.
        """
        return set(token for token in Token.objs.filter(chain=self.chain) if not isinstance(token, Unwrappable))

    def __iter__(self) -> Iterator[list[Token]]:
        portfolio: list[Position] = [*self.token_positions, *self.positions]
        while True:
            yield portfolio
            if self.has_just_target_tokens(portfolio):
                break
            portfolio = list(self.deeper(portfolio))

    def has_just_target_tokens(self, portfolio):
        return False
        # if target_tokens.intersection({ta.token for ta in portfolio if ta)

    def deeper(self, portfolio):
        for position in portfolio:
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
        return {name: compatible_protocols[name] for name in self.included_protocols_name}

    @default
    def positions(self):
        for protocol_name, protocol in self.protocols.items():
            yield from protocol.Positions(wallet=self.wallet, chain=self.chain, block=self.block)

    @default
    def token_positions(self):
        for token in self.included_tokens:
            if token.chain == self.chain:
                try:
                    token_position = token.position_of(self.wallet, self.block)
                except Exception as e:
                    logger.error(f"Token {token.symbol}: {e!r}")
                else:
                    if token_position:
                        yield token_position


def origin_protocol(position):
    while hasattr(position, "parent"):
        position = position.parent
    try:
        return position.protocol
    except AttributeError:
        return None


def boolsplit(seq, key=lambda element: element):
    true, false = [], []
    for element in seq:
        (true if key(element) else false).append(element)
    return true, false


def groupby(seq, key):
    d = defaultdict(list)
    for element in seq:
        d[key(element)].append(element)
    return dict(d)


def like_debank(portfolio: Porfolio, show_fiat=False):
    inprotocol, inwallet = boolsplit(portfolio.token_positions, lambda ta: ta.underlyings)
    print("Wallet")
    for ta in inwallet:
        print_amounts(ta, "  ")
        if ta and show_fiat:
            print(f"    {ta.amount_fiat!r}")
    print()

    for protocol, positions in groupby(inprotocol + portfolio.positions, lambda p: p.protocol).items():
        print(protocol)
        print_pos(positions, show_fiat=show_fiat)
        print()


def decimal_format(dec):
    s = str(dec)
    if "." in s:
        inte, frac = s.split(".")
        return f"{format(int(inte), '_')}.{frac}"
    else:
        return s


def print_amounts(ta, prefix=""):
    print(f"{prefix}{ta.token.symbol} {decimal_format(ta.amount)}")


def print_pos(positions, level=1, show_fiat=False):
    for p in positions:
        if isinstance(p, TokenPosition):
            ta = p
            print_amounts(ta, "  " * level)
            if ta and show_fiat and not ta.underlyings:
                print(f"{'  '*(level+1)}{ta.amount_fiat!r}")
        else:
            print(f"  {p.__class__.__name__}")
        if p.underlyings:
            print_pos(p.underlyings, level + 1, show_fiat)


def discover_defabipedia_tokens():
    from defabipedia import tokens

    for chain, container_class in tokens.Addresses.items():
        for attr, obj in vars(container_class).items():
            if not attr.startswith("_") and attr not in {"ZERO", "E"} and isinstance(obj, str):
                try:
                    DeployedToken.objs.get_or_create(chain=chain, symbol=attr, address=obj)
                except ValueError as e:
                    logger.error(f"{e!s}")
                    print(e)


discover_defabipedia_tokens()
