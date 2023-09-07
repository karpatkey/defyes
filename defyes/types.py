from decimal import Decimal
from functools import cached_property

from web3 import Web3

from .cache import cache_token
from .constants import Address, Chain
from .contracts import Erc20

simple_repr = True


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
    def __init__(self, addr: int | str, chain: Chain = Chain.ETHEREUM, **kwargs):
        self.chain = chain

    def __hash__(self):
        return hash((str(self), self.chain))

    @cached_property
    def symbol(self):
        return self.contract.symbol

    def __repr__(self):
        if simple_repr:
            return self.symbol
        else:
            return f"{self.__class__.__name__}({str(self)!r}, {self.chain!r}, symbol={self.symbol!r})"

    @cached_property
    def contract(self):
        return Erc20(self.chain, "latest", self)  # TODO: "latest" or a fixed block_id

    @cached_property
    def decimals(self):
        if self == Address.ZERO or self == Address.E:
            return 18
        else:
            return self.contract.decimals

    @classmethod
    def get_instance(cls, addr: int | str, chain: Chain = Chain.ETHEREUM):
        """
        Return the cached token, otherwise create a new instance and cache it.
        """
        try:
            return cache_token[addr, chain]
        except KeyError:
            cache_token[addr, chain] = (token := cls(addr, chain))
            return token

    def __rmul__(self, left_value):
        return TokenAmount(left_value, self)


class TokenAmount:
    def __init__(self, amount: int | str | Decimal, token: Token):
        # amount is expressed in the Token units
        # 1 Token = 10**(token.decimals) teuToken
        self.amount = Decimal(amount)
        self.token = token

    @property
    def decimal_teu_amount(self) -> Decimal:
        """
        Return a Decimal instance of the amount expressed as teu unit.
        """
        return self.amount.scaleb(self.token.decimals)

    @property
    def teu_amount(self) -> int:
        """
        Return and integer amount in teu just if it hasn't precision loss on convertion, otherwise raises a ValueError.
        """
        teu_amount = int(decimal_teu_amount := self.decimal_teu_amount)
        if teu_amount != decimal_teu_amount:
            raise ValueError(
                f"Avoiding precision loss as the teu value {decimal_teu_amount} still has non zero decimals."
            )
        return teu_amount

    @property
    def teu_rounded(self) -> "TokenAmount":
        """
        Return a new TokenAmount instance which is rounded at 1 teu. This is the way to explicity lost precision.
        """
        return self.__class__(round(self.amount, self.token.decimals), self.token)

    @classmethod
    def from_teu(cls, amount: int | str | Decimal, token: Token):
        if int(amount) != (decimal_amount := Decimal(amount)):
            raise ValueError("{amount=} must be an integer value.")
        return cls(amount=decimal_amount.scaleb(-token.decimals), token=token)

    def as_dict(self, decimal: bool = False) -> dict:
        teu_amount = self.teu_amount  # It also asserts taht the amount hasn't fractional teu
        return {
            "balance": self.amount if decimal else teu_amount,
            "address": str(self.token),
        }

    def __str__(self):
        abs_amount = abs(self.amount)
        if abs_amount < Decimal("1e-6"):
            return self.amount.to_eng_string().replace("E", "e")
        elif abs_amount < Decimal("1e-3"):
            return f"{self.amount.scaleb(6):f}e-6"
        else:
            return format(self.amount, ",").replace(",", "_")

    def __repr__(self):
        return f"{str(self)!r}*{self.token.symbol}"

    def __eq__(self, other):
        if isinstance(other, TokenAmount):
            return self.amount == other.amount and self.token == other.token
        elif isinstance(other, str):
            return repr(self) == other
        return False
