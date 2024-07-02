import logging
from dataclasses import dataclass, field
from decimal import Decimal

from defabipedia.tokens import EthereumTokenAddr
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import balance_of, total_supply

logger = logging.getLogger(__name__)

LPTOKENS_DB = {
    "0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9": {
        "name": "Reflexer-FLX/WETH",
        "blockchain": "ethereum",
        "staked_token": "0x353EFAC5CaB823A41BC0d6228d7061e92Cf9Ccb0",
        "tokens": [EthereumTokenAddr.FLX, EthereumTokenAddr.WETH],
    },
}


@dataclass
class LiquidityPool:
    addr: str
    block: int | str = "latest"
    web3: Web3 = None
    blockchain: str = field(init=False)

    def __post_init__(self):
        self.addr = Web3.to_checksum_address(self.addr)
        self.blockchain = LPTOKENS_DB[self.addr]["blockchain"]
        if self.web3 is None:
            self.web3 = get_node(self.blockchain)
        else:
            assert isinstance(self.web3, Web3), "web3 is not a Web3 instance"

    def _underlying(self, amount):
        fraction = Decimal(amount) / total_supply(self.addr, self.block, self.blockchain)
        result = []
        for token in LPTOKENS_DB[self.addr]["tokens"]:
            balance = balance_of(self.addr, token, self.block, self.blockchain)

            result.append([token, balance * fraction])

        return result

    def underlying(self, wallet):
        wallet = Web3.to_checksum_address(wallet)
        amount = balance_of(wallet, LPTOKENS_DB[self.addr]["staked_token"], self.block, self.blockchain)
        return self._underlying(amount)

    def lptoken_underlying(self, wallet):
        wallet = Web3.to_checksum_address(wallet)
        amount = balance_of(wallet, self.addr, self.block, self.blockchain)
        return self._underlying(amount)

    def pool_balances(self):
        amount = total_supply(self.addr, self.block, self.blockchain)
        return self._underlying(amount)


def underlying(wallet, lptoken_address, block, web3=None):
    lp = LiquidityPool(lptoken_address, block, web3)
    return lp.underlying(wallet)


def balance_of_lptoken_underlying(address, lptoken_address, block):
    lp = LiquidityPool(lptoken_address, block)
    return lp.lptoken_underlying(address)


def pool_balance(lptoken_address, block):
    lp = LiquidityPool(lptoken_address, block)
    return lp.pool_balances()
