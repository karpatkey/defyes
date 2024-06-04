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
    default,
    repr_for,
)
from defyes.serializers import DeployedTokenSerializer

protocol_path = Path(__file__).parent


class AuraToken(Unwrappable, DeployedToken):
    protocol = "aura"
    unwrapped_address: str

    @default
    def unwrapped_token(self) -> DeployedToken:
        return DeployedToken.objs.get_or_create(chain=self.chain, address=self.unwrapped_address)

    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        return [UnderlyingTokenPosition(token=self.unwrapped_token, amount_teu=token_position.amount_teu)]


class AuraTokenSerializer(DeployedTokenSerializer):
    token_class = AuraToken
    filename = protocol_path / "tokens.json"

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
            "address": token.address,
            "unwrapped_address": token.unwrapped_token.address,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.token_class(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
            address=d["address"],
            unwrapped_address=d["unwrapped_address"],
        )


AuraTokenSerializer.load_replacing_but_distinguishing_symbols()


@management.updater.register
def update_jsons():
    # oldarch.update_db()
    # Load tokens from db.json
    # AuraTokenSerializer.load_replacing_but_distinguishing_symbols()
    AuraTokenSerializer.save()


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
