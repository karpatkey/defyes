import json
from pathlib import Path
from typing import Iterator

from defabipedia import Chain

from . import portfolio as models


class JSONSerializer:
    filename: str | Path

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
    def generate_objs(cls) -> Iterator:
        with open(cls.filename) as f:
            dicts_list = json.load(f)
        for obj_dict in dicts_list:
            yield cls.fromdict(obj_dict)


class TokenSerializer(JSONSerializer):
    token_class = models.Token

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.token_class(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
        )

    @classmethod
    def load_replacing(cls):
        for token in cls.generate_objs():
            cls.token_class.objs.add_or_replace(token)

    @classmethod
    def save(cls):
        token_list = sorted(cls.token_class.objs.all, key=lambda token: (token.chain, token.symbol))
        token_dict_list = [cls.asdict(token) for token in token_list]
        json_str = json.dumps(token_dict_list, indent=2)
        with open(cls.filename, "w") as f:
            f.write(json_str)
            f.write("\n")


class DeployedTokenSerializer(TokenSerializer):
    token_class = models.DeployedToken

    @staticmethod
    def asdict(token) -> dict:
        return {
            "chain": str(token.chain),
            "symbol": token.symbol,
            "address": token.address,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls.token_class(
            chain=Chain.get_blockchain_by_name(d["chain"]),
            symbol=d["symbol"],
            address=d["address"],
        )
