"""
This module provides a JSONSerializer class for serializing and deserializing objects to and from JSON.

The JSONSerializer class defines methods for converting objects to dictionaries (`asdict`),
creating objects from dictionaries (`fromdict`), and generating objects from a JSON file (`generate_objs`).
"""

import json
import logging
from pathlib import Path
from typing import Iterator

from defabipedia import Chain

from . import portfolio as models

logger = logging.getLogger(__name__)


class JSONSerializer:
    """
    A class for serializing and deserializing objects to and from JSON.
    It is a generic class that must be subclassed to be used.

    This class provides methods to convert an object to a dictionary (`asdict`),
    create an object from a dictionary (`fromdict`), and generate objects from a JSON file (`generate_objs`).

    Attributes:
        filename (str | Path): The name or path of the JSON file to read from.

    Methods:
        asdict(obj): Convert an object to a dictionary. Must be overridden by subclasses.
        fromdict(d): Create an object from a dictionary. Must be overridden by subclasses.
        generate_objs(): Generate objects from a JSON file.
    """

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
    """
    A class for serializing and deserializing Token objects to and from JSON.
    It is an ad_hoc class used for the Token class found in the portfolio module.
    """

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
        Load tokens from a JSON file and replace the existing tokens in the database
        in case the chain and symbol are the same.
        """
        for token in cls.generate_objs():
            cls.token_class.objs.add_or_replace(token)

    @staticmethod
    def orderby(token):
        return token.chain, token.symbol

    @classmethod
    def save(cls):
        """
        Save all objects of the token class to a JSON file.

        This method retrieves all objects of the token class, sorts them according to the `orderby` attribute,
        and converts them to dictionaries using the `asdict` method.
        The dictionaries are then serialized to JSON and written to the file specified by the `filename` attribute.
        """
        token_list = sorted(cls.token_class.objs.all, key=cls.orderby)
        token_dict_list = [cls.asdict(token) for token in token_list]
        json_str = json.dumps(token_dict_list, indent=2)
        with open(f"{cls.filename}", "w") as f:
            f.write(json_str)
            f.write("\n")


class DeployedTokenSerializer(TokenSerializer):
    """Subclass of TokenSerializer for DeployedToken objects."""

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
        Load tokens from a JSON file, replacing existing tokens with the same chain and address,
        but distinguishing tokens with the same chain and symbol.

        This method generates token objects from a JSON file using the `generate_objs` method. For each generated token,
        it checks if a token with the same chain and symbol already exists.
        If such a token exists and its address is different from the generated token's address,
        the method modifies the generated token's symbol by adding a suffix derived from its address.
        This ensures that tokens with the same chain and symbol but different addresses can be distinguished.
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
    """
    Shorten a blockchain address for display purposes.
    Example:
        short_addr("0x1234567890abcdef") -> "345..def"
    """
    return f"{addr[2:5]}..{addr[-3:]}"
