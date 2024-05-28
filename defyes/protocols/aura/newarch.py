from typing import Iterator

from defabipedia import Blockchain, Chain

from defyes.portfolio import (
    DeployedToken,
    FrozenKwInit,
    Position,
    Token,
    TokenPosition,
    UnderlyingTokenPosition,
    Unwrappable,
    repr_for,
)


class AuraToken(Unwrappable, DeployedToken):
    protocol = "aura"

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        balancer_symbol = self.symbol[4:-6]
        underlying_token = Token.objs.get(chain=self.chain, symbol=balancer_symbol, protocol="balancer")
        return [UnderlyingTokenPosition(token=underlying_token, amount_teu=token_position.amount_teu)]


AuraToken.objs.create(chain=Chain.ETHEREUM, address="0x2a14dB8D09dB0542f6A371c0cB308A768227D67D")


class Position(Position):
    protocol: str = "aura"
    context: "Positions"
    address: str


class Positions(FrozenKwInit):
    wallet: str
    chain: Blockchain
    block: int

    __repr__ = repr_for("wallet", "chain", "block")

    def __iter__(self) -> Iterator[Position]:
        return
        yield
