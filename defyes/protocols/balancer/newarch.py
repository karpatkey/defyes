from pathlib import Path
from typing import Iterator

from defabipedia import Blockchain, Chain

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
    id: int

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
            UnderlyingTokenPosition(
                token=DeployedToken.objs.get_or_create(chain=self.chain, address=addr), amount=amount
            )
            for addr, amount in balances.items()
        ]


class BalancerTokenSerializer(DeployedTokenSerializer):
    token_class = BalancerToken
    filename = protocol_path / "tokens.json"

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
            "address": token.address,
            "id": token.id,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.token_class(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
            address=d["address"],
            id=d["id"],
        )

    @staticmethod
    def orderby(token):
        return token.chain, token.id


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
        return
        yield
