from typing import Iterator

from defabipedia import Blockchain, Chain

from defyes.portfolio import (
    ERC20Token,
    Frozen,
    KwInit,
    Position,
    TokenAmount,
    UnderlyingTokenAmount,
    Unwrappable,
    repr_for,
)

from . import contracts


class BalancerToken(Unwrappable, ERC20Token):
    protocol = "balancer"

    def unwrap(self, tokenamount: TokenAmount) -> list[UnderlyingTokenAmount]:
        ta = tokenamount
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
            UnderlyingTokenAmount(token=self.objs.get_or_create(address=addr), amount=amount)
            for addr, amount in balances.items()
        ]


BalancerToken(chain=Chain.ETHEREUM, address="0x93d199263632a4EF4Bb438F1feB99e57b4b5f0BD")


class Position(Position):
    protocol: str = "balancer"
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
