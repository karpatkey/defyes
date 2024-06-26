from pathlib import Path
from typing import Iterator

from defabipedia import Blockchain, Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr
from karpatkit.helpers import listify

from defyes import management
from defyes.portfolio import (
    DeployedToken,
    FrozenKwInit,
    Position,
    Rewardable,
    TokenPosition,
    UnderlyingTokenPosition,
    Unwrappable,
    default,
    repr_for,
)
from defyes.serializers import DeployedTokenSerializer

from . import contracts

protocol_path = Path(__file__).parent


class Aura:
    protocol = "aura"


class AuraToken(Aura, DeployedToken):
    pass


AuraToken.objs.create(symbol="AURA", chain=Chain.ETHEREUM, address=EthereumTokenAddr.AURA)
AuraToken.objs.create(symbol="AURA", chain=Chain.GNOSIS, address=GnosisTokenAddr.AURA)


class UnwrappableAuraToken(Unwrappable, AuraToken):
    @listify
    def unwrap(self, token_position: TokenPosition) -> list[UnderlyingTokenPosition]:
        yield UnderlyingTokenPosition(
            token=self.unwrapped_token, amount_teu=token_position.amount_teu, parent=token_position
        )


class LockerToken(Rewardable, UnwrappableAuraToken):
    contract_class = contracts.Locker

    @default
    def unwrapped_token(self) -> DeployedToken:
        return DeployedToken.objs.get_or_create(chain=self.chain, symbol="AURA")

    @listify
    def unclaimed_rewards(self, position: Position) -> list[UnderlyingTokenPosition]:
        for token_addr, balance in self.contract.claimable_rewards(position.wallet):
            token = DeployedToken.objs.get_or_create(chain=self.chain, address=token_addr)
            yield UnderlyingTokenPosition(token=token, amount_teu=balance)


LockerToken.objs.create(symbol="vlAURA", chain=Chain.ETHEREUM, address="0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC")


class Positions(FrozenKwInit):
    wallet: str
    chain: Blockchain
    block: int

    __repr__ = repr_for("wallet", "chain", "block")

    def __iter__(self) -> Iterator[Position]:
        return iter([])


@management.updater.register
def update_jsons():
    # oldarch.update_db() # TODO: fix update_db in __init__.py
    load_tokens_from_db_json()
    AuraTokenSerializer.save()


class WrappedToken(UnwrappableAuraToken):
    unwrapped_address: str
    id: int

    @default
    def unwrapped_token(self) -> DeployedToken:
        return DeployedToken.objs.get_or_create(chain=self.chain, address=self.unwrapped_address)


class AuraTokenSerializer(DeployedTokenSerializer):
    token_class = WrappedToken
    filename = protocol_path / "tokens.json"

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
            "address": token.address,
            "id": token.id,
            "deployment_block": token.deployment_block,
            "unwrapped_address": token.unwrapped_token.address,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.token_class(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
            address=d["address"],
            id=d["id"],
            unwrapped_address=d["unwrapped_address"],
            deployment_block=d["deployment_block"],
        )

    @staticmethod
    def orderby(token):
        return token.chain, token.id


AuraTokenSerializer.load_replacing_but_distinguishing_symbols()


def load_tokens_from_db_json():
    import json

    with open(protocol_path / "db.json", "r") as db_file:
        db_data = json.load(db_file)
        for chain_str, balancer_addresses in db_data.items():
            chain = Chain.get_blockchain_by_name(chain_str)
            for balancer_address, data in balancer_addresses.items():
                for block, block_data in data.items():
                    aura_address = block_data["rewarder"]
                    break
                try:
                    AuraToken.objs.get(
                        chain=chain,
                        address=aura_address,
                    )
                except LookupError:
                    AuraToken.objs.create(
                        chain=chain,
                        address=aura_address,
                        id=block_data["poolId"],
                        unwrapped_address=balancer_address,
                        deployment_block=block,
                    )
