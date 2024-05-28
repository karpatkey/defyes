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

from . import contracts


class BalancerToken(Unwrappable, DeployedToken):
    protocol = "balancer"

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        ta = token_position
        lp = contracts.LiquidityPool(ta.token.chain, ta.block, ta.token.address)
        pool_tokens = contracts.Vault(self.chain, ta.block).get_pool_data(lp.poolid)
        balances = {}
        for n, (addr, balance) in enumerate(pool_tokens):
            if n == lp.bpt_index:
                continue
            token = contracts.PoolToken(self.chain, ta.block, addr)
            token_addr, token_balance = lp.calc_amount(token, ta.amount, balance, decimals=True)
            balances[token_addr] = balances.get(token_addr, 0) + token_balance
        return [
            UnderlyingTokenPosition(token=Token.objs.get_or_create(chain=self.chain, address=addr), amount=amount)
            for addr, amount in balances.items()
        ]


BalancerToken.objs.create(chain=Chain.ETHEREUM, address="0x93d199263632a4EF4Bb438F1feB99e57b4b5f0BD")


class Position(Position):
    protocol: str = "balancer"
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
