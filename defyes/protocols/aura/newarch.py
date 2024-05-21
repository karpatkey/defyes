from typing import Iterator

from defabipedia import Blockchain, Chain

from defyes.porfolio import (
    ERC20Token,
    Frozen,
    KwInit,
    Position,
    TokenAmount,
    UnderlyingTokenAmount,
    Unwrappable,
    repr_for,
)


class VaultToken(Unwrappable, ERC20Token):
    protocol = "aura"

    def unwrap(self, tokenamount: TokenAmount) -> list[UnderlyingTokenAmount]:
        balancer_symbol = self.symbol[4:-6]
        underlying_token = self.objs.get(symbol=balancer_symbol, protocol="balancer")
        return [UnderlyingTokenAmount(token=underlying_token, amount_teu=tokenamount.amount_teu)]


VaultToken(chain=Chain.ETHEREUM, address="0x2a14dB8D09dB0542f6A371c0cB308A768227D67D")


class Position(Position):
    protocol: str = "aura"
    context: "Positions"
    address: str


class Positions(Frozen, KwInit):
    wallet: str
    chain: Blockchain
    block: int

    __repr__ = repr_for("wallet", "chain", "block")

    def __iter__(self) -> Iterator[Position]:
        return
        yield
