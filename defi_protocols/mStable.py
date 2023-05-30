from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import get_node, get_contract

BASIC_META_VAULT = '0x6d68f5b8c22a549334ca85960978f9de4deba2d3'

BASIC_META_VAULT_ABI = '[{"inputs":[],"name":"asset","outputs":[{"internalType":"address","name":"assetTokenAddress","type":"address"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"assetPoolIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"assetScale","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint256","name":"shares","type":"uint256"}],"name":"convertToAssets","outputs":[{"internalType":"uint256","name":"assets","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"decimals_","type":"uint8"}],"stateMutability":"view","type":"function"}]'


def underlying(token_address: str, wallet: str, block: int, blockchain: str, web3=None, decimals=True) -> list:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    token_address = Web3.to_checksum_address(token_address)
    meta_vault_contract = get_contract(token_address,blockchain,web3=web3,abi=BASIC_META_VAULT_ABI,block=block)
    balance_of_vault = meta_vault_contract.functions.balanceOf(wallet).call(block_identifier=block)
    underlying_asset = meta_vault_contract.functions.asset().call()
    asset_scale = meta_vault_contract.functions.assetScale().call() if decimals else Decimal('1')
    balance_of_assets = meta_vault_contract.functions.convertToAssets(balance_of_vault).call(block_identifier=block)

    balances.append([underlying_asset, balance_of_assets / Decimal(asset_scale)])
    return balances
