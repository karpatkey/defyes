from pathlib import Path
from typing import Iterator

from defabipedia import Blockchain

from defyes import management
from defyes.portfolio import (
    DeployedToken,
    FrozenKwInit,
    Position,
    TokenPosition,
    UnderlyingTokenPosition,
    Unwrappable,
    repr_for,
)
from defyes.serializers import DeployedTokenSerializer

from . import contracts

protocol_path = Path(__file__).parent


class BalancerToken(Unwrappable, DeployedToken):
    protocol = "balancer"

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        pos = token_position
        lp = contracts.LiquidityPool(pos.token.chain, pos.block, pos.token.address)
        pool_tokens = contracts.Vault(self.chain, pos.block).get_pool_data(lp.poolid)
        balances = {}
        for n, (addr, balance) in enumerate(pool_tokens):
            if n == lp.bpt_index:
                continue
            token = contracts.PoolToken(self.chain, pos.block, addr)
            token_addr, token_balance = lp.calc_amount(token, pos.amount, balance, decimals=True)
            balances[token_addr] = balances.get(token_addr, 0) + token_balance
        return [
            UnderlyingTokenPosition(
                token=DeployedToken.objs.get_or_create(chain=self.chain, address=addr),
                amount=amount,
                parent=token_position,
            )
            for addr, amount in balances.items()
        ]


class BalancerTokenSerializer(DeployedTokenSerializer):
    token_class = BalancerToken
    filename = protocol_path / "tokens.json"


BalancerTokenSerializer.load_replacing_but_distinguishing_symbols()

management.updater.register(BalancerTokenSerializer.save)


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
        return iter([])
