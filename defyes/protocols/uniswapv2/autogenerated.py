"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import LpToken

# Optionally
class LpToken(LpToken):
    ...
"""

from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class LpToken:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "lp_token.json"))

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)

    @property
    def get_reserves(self) -> tuple[int, int, int]:
        """
        Output: _reserve0, _reserve1, _blockTimestampLast
        """
        return self.contract.functions.getReserves().call(block_identifier=self.block)

    def balance_of(self, arg0: str) -> int:
        return self.contract.functions.balanceOf(arg0).call(block_identifier=self.block)

    @property
    def token0(self) -> str:
        return const_call(self.contract.functions.token0())

    @property
    def token1(self) -> str:
        return const_call(self.contract.functions.token1())

    @property
    def k_last(self) -> int:
        return self.contract.functions.kLast().call(block_identifier=self.block)

    @property
    def swap_fee(self) -> int:
        return self.contract.functions.swapFee().call(block_identifier=self.block)