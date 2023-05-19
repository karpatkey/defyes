import logging
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Union
from web3 import Web3

from defi_protocols.functions import get_node, balance_of, get_contract, get_decimals

logger = logging.getLogger(__name__)

DERIVS_DB = {
    '0xae78736Cd615f374D3085123A210448E74Fc6393': {
        'name': "Rocket Pool ETH",
        'blockchain': 'ethereum',
        'underlying': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        'eth_value_function': 'getEthValue',
        'eth_value_abi': '[{"inputs":[{"internalType":"uint256","name":"_rethAmount","type":"uint256"}],"name":"getEthValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    },
    '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb': {
        'name': "Ankr Staked ETH",
        'blockchain': 'ethereum',
        'underlying': '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
        'eth_value_function': 'sharesToBonds',
        'eth_value_abi': '[{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sharesToBonds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'
    },
}



@dataclass
class EthDerivative:
    addr: str
    block: Union[int, str] = 'latest'
    web3: Web3 = None
    decimals: bool = True
    blockchain: str = field(init=False)
    eth_value_function: str = field(init=False) 
    eth_value_abi: str = field(init=False)
    
    def __post_init__(self):
        self.addr = Web3.to_checksum_address(self.addr)
        self.blockchain = DERIVS_DB[self.addr]['blockchain']
        if self.web3 is None:
            self.web3 = get_node(self.blockchain, block=self.block)
        self.eth_value_abi = DERIVS_DB[self.addr]['eth_value_abi']
        self.contract_instance = get_contract(self.addr, self.blockchain, abi=self.eth_value_abi)
        self.eth_value_function = DERIVS_DB[self.addr]['eth_value_function']

    def _underlying(self, eth_value, token_decimals):
        result = []
        underlying_amount = eth_value / Decimal(10 ** token_decimals)
        result.append([DERIVS_DB[self.addr]['underlying'], underlying_amount])
        return result

    def underlying(self, wallet):
        wallet = self.web3.to_checksum_address(wallet)
        amount = balance_of(wallet, self.addr, self.block, self.blockchain, decimals=False)
        eth_value = self.contract_instance.functions[self.eth_value_function](amount).call(block_identifier=self.block)
        token_decimals = get_decimals(self.addr,self.blockchain) if self.decimals else 0
        return self._underlying(eth_value, token_decimals)