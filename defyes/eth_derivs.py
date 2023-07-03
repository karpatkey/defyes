import logging
from dataclasses import dataclass
from decimal import Decimal

from web3 import Web3

from defyes.functions import balance_of, get_decimals, to_token_amount

logger = logging.getLogger(__name__)


@dataclass
class EthDerivative:
    protocol: str
    description: str
    addr: str
    blockchain: str
    underlying_token: str
    eth_value_function: str
    eth_value_abi: str

    def unwrap(self, amount: Decimal | int | float, block: int | str, web3: Web3) -> Decimal:
        token_decimals = get_decimals(self.addr, blockchain=self.blockchain, web3=web3)
        amount = int(Decimal(amount) * Decimal(10**token_decimals))
        # The 'sharesToBonds' function in ankrETH is only present in the proxy implementation contract from block 16476340 onwards
        # Some proxy implementations:
        # AETH_R16: 0x1E5e5CF3652989A57736901D95749A326F5Cb60F
        # AETH_R17: 0x89632e27427109d64fFe1CdD98027139477E020F
        # AETH_R18: 0x3eD1DFBCCF893b7d2D730EAd3e5eDBF1f8f95a48
        if isinstance(block, str):
            contract = web3.eth.contract(address=self.addr, abi=self.eth_value_abi)
            eth_value = contract.functions[self.eth_value_function](amount).call(block_identifier=block)
        else:
            if self.addr == "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb" and block < 16476340:
                contract = web3.eth.contract(
                    address=self.addr,
                    abi='[{"inputs":[],"name":"ratio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]',
                )
                eth_value = int(
                    Decimal(amount * (10**18)) / Decimal(contract.functions.ratio().call(block_identifier=block))
                )
            else:
                contract = web3.eth.contract(address=self.addr, abi=self.eth_value_abi)
                eth_value = contract.functions[self.eth_value_function](amount).call(block_identifier=block)
        eth_value = Decimal(eth_value) / Decimal(10**token_decimals)
        return to_token_amount(self.addr, amount=eth_value, blockchain=self.blockchain, web3=web3, decimals=True)

    def underlying(self, wallet: str, block: int | str, decimals: bool, web3: Web3, unwrapped: bool = True) -> Decimal:
        wallet = web3.to_checksum_address(wallet)
        amount = balance_of(wallet, self.addr, block, self.blockchain, decimals=False)
        if unwrapped:
            return self.unwrap(amount, block, web3)
        else:
            return to_token_amount(self.addr, amount=amount, blockchain=self.blockchain, web3=web3, decimals=decimals)
