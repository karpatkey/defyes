from web3 import Web3

from defyes.functions import ensure_a_block_number
from defyes.protocols.opus_pool.autogenerated import EthVault
from defyes.types import Address


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    position_identifier: str,
    block: int | str = "latest",
    decimals: bool = True,
):
    """Get the data for the Opus Pool protocol. Currently there's just one vault that is supported. ETH vault.

    Args:
        position_identifier (str): The address of the vault you want to get data from.
    """
    wallet = Web3.to_checksum_address(wallet)
    position_identifier = Web3.to_checksum_address(position_identifier)
    block = ensure_a_block_number(block, blockchain)

    eth_vault = EthVault(blockchain, block, position_identifier)

    shares_amount = eth_vault.get_shares(wallet)

    ETH_amount = eth_vault.convert_to_assets(shares_amount)

    if decimals:
        ETH_amount = ETH_amount / 10**18

    data_dict = {
        "blockchain": blockchain,
        "block": block,
        "protocol": "Opus Pool",
        "positions_key": "token_vault",
        "version": 0,
        "wallet": wallet,
        "decimals": "",
        "positions": {
            "ETH": {
                "underlyings": [{"address": Address.ZERO, "balance": ETH_amount}],
            },
        },
    }

    return data_dict
