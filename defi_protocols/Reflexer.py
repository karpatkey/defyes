from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union
from web3 import Web3

from defi_protocols.functions import get_node, balance_of, total_supply
from defi_protocols.constants import ETHTokenAddr


LPTOKENS_DB = {
    '0xd6F3768E62Ef92a9798E5A8cEdD2b78907cEceF9': {
        'name': "Reflexer-FLX/WETH",
        'blockchain': 'ethereum',
        'staked_token': '0x353EFAC5CaB823A41BC0d6228d7061e92Cf9Ccb0',
        'tokens': [ETHTokenAddr.FLX, ETHTokenAddr.WETH]
    },
}


@dataclass
class LiquidityPool:
    addr: str
    block: Union[int, str] = 'latest'
    web3: Web3 = None
    blockchain: str = field(init=False)

    def __post_init__(self):
        if not self.addr.lower() in ' '.join(LPTOKENS_DB.keys()).lower():
            raise ValueError("LP token address not in DB.")
        self.blockchain = LPTOKENS_DB[self.addr]['blockchain']
        if self.web3 is None:
            self.web3 = get_node(self.blockchain, block=self.block)
        else:
            assert self.web3.isinstance(Web3), "web3 is not a Web3 instance"
        self.addr = self.web3.to_checksum_address(self.addr)

    def _underlying(self, amount):
        fraction = Decimal(amount) / Decimal(total_supply(self.addr, self.block, self.blockchain))
        result = []
        for token in LPTOKENS_DB[self.addr]['tokens']:
            balance = balance_of(self.addr, token, self.block, self.blockchain)

            result.append([token, Decimal(balance) * fraction])

        return result

    def underlying(self, wallet):
        wallet = self.web3.to_checksum_address(wallet)
        amount = balance_of(wallet, LPTOKENS_DB[self.addr]['staked_token'], self.block, self.blockchain)
        return self._underlying(amount)

    def lptoken_underlying(self, wallet):
        wallet = self.web3.to_checksum_address(wallet)
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
