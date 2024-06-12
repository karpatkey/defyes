import importlib
import logging
from decimal import Decimal
from functools import cached_property
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.helpers import listify
from karpatkit.node import get_node
from web3 import Web3

from defyes.contracts import Erc20
from defyes.dataclasses import FrozenKwInit, repr_dict, repr_for
from defyes.descriptors import DefaultNameFromClass, InstancesManager
from defyes.helpers import timeit
from defyes.lazytime import Time
from defyes.prices import Chainlink as chainlink
from defyes.prices.prices import get_price as get_price_in_usd

default = cached_property
Module = type(logging)

logger = logging.getLogger(__name__)


class Fiat(float):
    source: str | None = None
    symbol: str | None = None

    def __init__(self, value, *, source=None, chain=None, block=None):
        super().__init__()
        self.source = source
        self.block = block

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({format(float(self), '_')}, source={self.source!r})"

    def __str__(self) -> str:
        return f"{format(float(self), '_')} {self.symbol}"

    def __mul__(self, other: float) -> "Fiat":
        return self.__class__(float(other) * float(self), source=self.source)

    __rmul__ = __mul__


class USD(Fiat):
    symbol: str = "USD"


class Token(FrozenKwInit):
    node: Web3
    chain: Blockchain
    symbol: str
    name: str
    price: Fiat
    decimals: int
    protocol: str | None = None

    __repr__ = repr_for("chain", "symbol", "protocol")

    objs = InstancesManager()

    indexes = [
        ["chain", "symbol"],
    ]


class NativeToken(Token):
    decimals: int = 18

    @default
    def node(self) -> Web3:
        return get_node(self.chain)

    indexes = [
        ["chain"],
        ["symbol"],
        ["chain", "symbol"],
    ]

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

    indexes = [
        ["chain", "address"],
        ["chain", "symbol"],
    ]

    @timeit
    def price(self, block: int) -> Fiat:
        price, source, _ = get_price_in_usd(self.address, block, self.chain)
        return USD(price if price else float("nan"), source=source, block=block, chain=self.chain)

    def balance_of(self, wallet: str, block: int) -> int:
        return self.contract.contract.functions.balanceOf(wallet).call(block_identifier=block)

    def position_of(self, wallet: str, block: int) -> "TokenPosition":
        return TokenPosition(token=self, wallet=wallet, block=block)

    @default
    def block(self):
        return self.contract.block


class Unwrappable:
    def unwrap(self, token_position: "TokenPosition") -> list["UnderlyingTokenPosition"]:
        raise NotImplementedError


frozenlist = tuple


class Position(FrozenKwInit):
    """
    A finantial value.
    """

    wallet: str
    chain: Blockchain
    block: int
    protocol: str | None = None
    underlying: list["Position"] = frozenlist()  # Frozen just to make the default inmutable
    unclaimed_rewards: list["Position"] = frozenlist()
    name: str = DefaultNameFromClass()

    __repr__ = repr_dict()

    def __bool__(self):
        return bool(self.underlying) or bool(self.unclaimed_rewards)


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
    @listify
    def underlying(self) -> list["UnderlyingTokenPosition"]:
        """
        Returns one UnderlyingTokenPosition or zero in the list, which is the unwrapped token with its converted value.
        """
        if isinstance(self.token, Unwrappable):
            yield from self.token.unwrap(self)

    @default
    def block(self):
        return self.token.block

    @default
    def time(self) -> Time:
        if isinstance(self.block, int):
            return Time(self.token.node.eth.get_block(self.block).timestamp)
        else:
            raise ValueError("Undefined time, because `block` isn't defined as an integer.")

    @property
    def protocol(self) -> str:
        return self.token.protocol

    @property
    def chain(self) -> str:
        return self.token.chain

    def __bool__(self):
        return self.amount_teu != 0

    def __add__(self, other):
        if self.token == other.token:
            return self.__class__(token=self.token, amount_teu=self.amount_teu + other.amount_teu)
        else:
            raise ValueError(f"Cannot add positions for different tokens ({self.token=} {other.token=}")


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
        try:
            return int(self.amount.scaleb(self.token.decimals))
        except AttributeError as exc:
            if not isinstance(self.amount, Decimal):
                raise ValueError(f"{self.amount=} is expected to be Decimal") from exc
            raise

    def __post_init__(self):
        """
        Check that at least `amount` or `amount_teu` is defined, to avoid circular recursion.
        """
        if not {"amount", "amount_teu"}.intersection(self.__dict__):
            raise ValueError("At least one of either `amount` or `amount_teu` must be defined.")

    @cached_property
    def root_protocol(self):
        position = self
        while hasattr(position, "parent"):
            position = position.parent
        try:
            return position.protocol
        except AttributeError:
            return None


#### Some token definitions

ETH = NativeToken.objs.create(chain=Chain.ETHEREUM, symbol="ETH", name="Ether")
NativeToken.objs.create(chain=Chain.POLYGON, symbol="MATIC", name="Matic")
NativeToken.objs.create(chain=Chain.GNOSIS, symbol="xDAI", name="Gnosis native DAI")


DeployedToken.objs.create(
    chain=Chain.POLYGON,
    address="0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    symbol="USDC.e",
)


class WETHToken(Unwrappable, DeployedToken):
    chain = Chain.ETHEREUM
    address = EthereumTokenAddr.WETH

    def unwrap(self, token_position: "TokenPosition") -> list["UnderlyingTokenPosition"]:
        return [UnderlyingTokenPosition(token=ETH, amount=token_position.amount, parent=token_position)]


WETHToken.objs.create()

###


class Portfolio(FrozenKwInit):
    chain: Blockchain
    block: int
    wallet: str

    __repr__ = repr_for("chain", "block", "wallet")

    @default
    def included_protocols_name(self) -> set[str]:
        return set(compatible_protocols.keys())

    # TODO: no conviene tirar aunque no se conozcan. solamente filtrar para token_position, no para underlying
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
        # if target_tokens.intersection({pos.token for pos in portfolio if pos)

    def deeper(self, portfolio):
        for position in portfolio:
            # Stop underlying/unwrapping on target tokens
            if hasattr(position, "token") and position.token in self.target_tokens:
                yield position
                continue

            for underlying in position.underlying:
                yield underlying

            for unclaimed_reward in position.unclaimed_rewards:
                yield unclaimed_reward

    @default
    def protocols(self) -> dict[str, Module]:
        return {name: compatible_protocols[name] for name in self.included_protocols_name}

    @default
    @listify
    def positions(self):
        for protocol_name, protocol in self.protocols.items():
            yield from protocol.Positions(wallet=self.wallet, chain=self.chain, block=self.block)

    @default
    @listify
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


## Loading protocols and tokens

compatible_protocols = {
    name: importlib.import_module(f"defyes.protocols.{name}.newarch") for name in ["aura", "balancer", "maker", "lido"]
}

discover_defabipedia_tokens()
