from typing import Union
from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import get_node, get_contract

# RealT Token Address
TOKEN_CONTRACT_XDAI: str = '0x7349C9eaA538e118725a6130e0f8341509b9f8A0'

# ABIs
# RealT token contract ABI - UNDERLYING_ASSET_ADDRESS, balanceOf, decimals
TOKEN_CONTRACT_ABI = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"address"}],"name":"UNDERLYING_ASSET_ADDRESS","inputs":[]},\
                        {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"user","internalType":"address"}]},\
                        {"type":"function","stateMutability":"view","outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[]}]'


def underlying(wallet: str, block: Union[int,str], blockchain: str,
               web3=None, decimals=True) -> list:

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    token_contract = get_contract(TOKEN_CONTRACT_XDAI, blockchain,
                                  web3, abi=TOKEN_CONTRACT_ABI)
    balance_of = Decimal(token_contract.functions.balanceOf(wallet).call(block_identifier=block))
    token_decimals = token_contract.functions.decimals().call()
    underlying_token = token_contract.functions.UNDERLYING_ASSET_ADDRESS().call()

    balance = balance_of / Decimal(10**(token_decimals if decimals else 0))

    return [[underlying_token, balance]]
