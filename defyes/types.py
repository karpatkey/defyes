from decimal import Decimal
from functools import cached_property

from defabipedia import Blockchain, Chain
from karpatkit.constants import Address
from web3 import Web3

from .contracts import Erc20

simple_repr = True  # TODO: from environ with default True


class Addr(str):
    # TODO: Maybe move chain to Addr
    def __new__(cls, addr: int | str, *args, **kwargs):
        if isinstance(addr, str):
            cs_addr = Web3.to_checksum_address(addr)
            if cs_addr != addr:
                raise cls.ChecksumError(f"Provided {addr=!r} differs from expected {cs_addr!r}")
            s = addr
        else:
            s = Web3.to_checksum_address(addr)
        return super().__new__(cls, s)

    class ChecksumError(ValueError):
        pass


class Token(Addr):
    """
    Class representing the token.
    Initializes the object with the provided address, blockchain chain, block number.

    Parameters:
        addr (int | str): The address to be initialized with.
        chain (Blockchain): The blockchain chain to be used (default is Chain.ETHEREUM).
        block (int | str): The block number to be used (default is "latest").
        **kwargs: Additional keyword arguments.

    Cached Properties:
        symbol: Returns the symbol of the token.
        contract: Returns the ERC20 contract of the token.
        decimals: Returns the decimals of the token.
    """

    _cache = {}

    def __init__(self, addr: int | str, chain: Blockchain = Chain.ETHEREUM, block: int | str = "latest", **kwargs):
        self.chain = chain
        self.block = block

    def __hash__(self):
        return hash((str(self), self.chain))

    @cached_property
    def symbol(self):
        if self == Address.ZERO or self == Address.E:
            return "ETH"  # TODO: Not true always (MATIC, etc.). It depends on the native coin
        return self.contract.symbol

    def __repr__(self):
        if simple_repr:
            return self.symbol
        return f"{self.__class__.__name__}({str(self)!r}, {self.chain!r}, symbol={self.symbol!r})"

    @cached_property
    def contract(self):  # TODO: could be called deployment, instance, because it's an instance of a contract
        """Get the token ERC20 contract."""
        return Erc20(self.chain, self.block, address=self)
        # TODO: discrimitate contract class as a function of chain (and address)

    @cached_property
    def decimals(self):
        """Get the token decimals."""
        # TODO: It could be implemented in a native class
        if self == Address.ZERO or self == Address.E:
            return 18
        else:
            return self.contract.decimals

    @classmethod
    def get_instance(cls, addr: int | str, chain: Blockchain = Chain.ETHEREUM, block: int | str = "latest"):
        # TODO: stop using "latest. "safe" is better.
        """
        Return the cached token, otherwise create a new instance and cache it.
        """
        try:
            return cls._cache[addr, chain]
            # TODO: Issue: It's using the cache even whan changing for
        except KeyError:
            cls._cache[addr, chain] = (token := cls(addr, chain, block))
            return token

    def __rmul__(self, left_value):
        """Allowing the multiplication of a token by a value."""
        if isinstance(left_value, str):
            value = Decimal(left_value).scaleb(self.decimals)
            if int(value) != value:
                raise ValueError(
                    f"Preventing str precision loss. {left_value} has more decimals than this token ({self.decimals} decimals)."
                )
        elif isinstance(left_value, Decimal):
            value = left_value.scaleb(self.decimals)
            if int(value) != value:
                raise ValueError(
                    f"Preventing Decimal precision loss. {left_value} has more decimals than this token ({self.decimals} decimals)."
                )
        elif isinstance(left_value, int):
            value = left_value * 10**self.decimals
        elif isinstance(left_value, float):
            raise ValueError("Preventing potential float precision loss. Use str, Decimal or int instead.")
        else:
            raise ValueError(f"{type(left_value)} not supported in convention to a TokenAmount value.")
        return TokenAmount.from_teu(value, self)


def format_amount(amount: Decimal) -> str:
    value_str = str(amount)
    if "." in value_str:
        integer_part, decimal_part = value_str.split(".")
        formatted_integer_part = "{:,}".format(int(integer_part)).replace(",", "_")
        formatted_value = f"{formatted_integer_part}.{decimal_part}"
    else:
        formatted_value = "{:,}".format(int(value_str)).replace(",", "_")
    return formatted_value


class TokenAmount:  # Could extend a Quantity class/iterface (value and unit)
    def __init__(self, amount: int | Decimal, token: Token):
        """
        amount is expressed in the Token units
        1 Token = 1e^(token.decimals) teuToken
        """
        self.amount = Decimal(amount)
        self.token = token
        self.teu = Decimal(10**self.token.decimals)
        # TODO: use scaleb instead. TEU is even relative to Token, not to TokenAmount

    @classmethod
    def from_teu(cls, amount: int | Decimal, token: Token):
        amount = Decimal(amount) / Decimal(10**token.decimals)
        return cls(amount=amount, token=token)

    def as_dict(self, not_in_teu: bool = False) -> dict:
        # TODO: This should be part of the serialization proces used by ETL to write tables.
        # We don't need low levels here.
        return {
            "balance": self.balance(not_in_teu),
            "address": str(self.token),
        }

    def balance(self, not_in_teu: bool = False) -> int | Decimal:  # TODO: negative arg is ugly `not_in_teu`
        """Return the balance multiplied by decimals(False) or as it is(True)."""
        return self.amount if not_in_teu else self.amount * self.teu

    def __str__(self):
        return format_amount(self.amount)

    def __repr__(self):
        _, digits, exp = self.amount.as_tuple()
        zeros_in_decimal_part = abs(exp) - len(digits)
        if int(self.amount) == 0 and exp < 0 and zeros_in_decimal_part > 3 and (abs(exp) > self.token.decimals / 2):
            return f"{format_amount(self.amount * self.teu)}*teu{self.token.symbol}"
        else:
            return str(f"{str(self)}*{self.token.symbol}")

    def __eq__(self, other):
        if isinstance(other, TokenAmount):
            return self.amount == other.amount and self.token == other.token
        elif isinstance(other, str):
            return repr(self) == other
        elif other == 0:
            return self.amount == 0
        return False
