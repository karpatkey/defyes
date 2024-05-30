import json
from pathlib import Path
from typing import Iterator

from defabipedia import Chain

from . import portfolio as models


class JSONSerializer:
    filename: str | Path
    model: type  # Class to create each instance

    @staticmethod
    def asdict(obj) -> dict:
        """
        JSON compatible python dict.
        """
        raise NotImplementedError

    @classmethod
    def fromdict(cls, d: dict):
        """
        JSON compatible python dict.
        """
        raise NotImplementedError

    @classmethod
    def save(cls):
        with open(cls.filename, "w") as f:
            json.dump([obj.asdict for obj in cls.model.objs.all], f, indent=2)

    @classmethod
    def generate_objs(cls) -> Iterator:
        with open(cls.filename) as f:
            dicts_list = json.load(f)
        for obj_dict in dicts_list:
            yield cls.fromdict(obj_dict)


class TokenSerializer(JSONSerializer):
    model = models.Token

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.model(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
        )

    @classmethod
    def load_replacing(cls):
        for token in cls.generate_objs():
            cls.model.objs.add_or_replace(token)


class DeployedTokenSerializer(TokenSerializer):
    model = models.DeployedToken

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
            "address": token.address,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.model(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
            address=d["address"],
        )
