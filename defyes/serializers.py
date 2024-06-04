import json
import logging
from pathlib import Path
from typing import Iterator

from defabipedia import Chain

from . import portfolio as models

logger = logging.getLogger(__name__)


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
        """
        Replace if chain and address is the same.
        """
        for token in cls.generate_objs():
            cls.token_class.objs.add_or_replace(token)

    @staticmethod
    def orderby(token):
        return token.chain, token.symbol

    @classmethod
    def save(cls):
        token_list = sorted(cls.token_class.objs.all, key=cls.orderby)
        token_dict_list = [cls.asdict(token) for token in token_list]
        json_str = json.dumps(token_dict_list, indent=2)
        with open(f"{cls.filename}", "w") as f:
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

    @staticmethod
    def orderby(token):
        return token.chain, token.address

    @classmethod
    def load_replacing_but_distinguishing_symbols(cls):
        """
        Replace if chain and address is the same, but change symbol name, by adding part of the address as a suffix, if
        the chain and symbol is the same to an existing token.
        """
        for token in cls.generate_objs():
            try:
                current_token = cls.token_class.objs.get(chain=token.chain, symbol=token.symbol)
            except LookupError:
                pass
            else:
                if token.address != current_token.address:
                    token.__dict__["symbol"] += f"_{short_addr(token.address)}"
                    logger.warning(
                        f"Changing symbol name {current_token.symbol!r} to {token.symbol!r} ({token.address}) "
                        f"because the token {current_token.address} is aready defined in {current_token.chain} "
                        "with the same symbol name."
                    )
            cls.token_class.objs.add_or_replace(token)


def short_addr(addr: str):
    return f"{addr[2:5]}..{addr[-3:]}"
