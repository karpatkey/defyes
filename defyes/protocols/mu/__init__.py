"""This module contains the functions to interact with the mu protocol.
The main function is `get_protocol_data_for` that returns the data for a wallet for mu exchange.
for more info on the mu exchange protocol, see https://docs.mu.exchange/staking/usdmsdai-vault.
"""

from defyes.types import Addr
from defyes.functions import ensure_a_block_number
from web3 import Web3
from defyes.protocols.mu import TradingVault


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    lptoken_address: str,
    block: int | str = "latest",
) -> dict:
    """Get the data for a wallet for mu exchange. Currently there's just one vault that is supported.
    msDAI vault is the only one."""
    wallet = Addr(Web3.to_checksum_address(wallet))
    lptoken_address = Web3.to_checksum_address(lptoken_address)
    block_id = ensure_a_block_number(block, blockchain)

    # Get the trading vault with the msDAI balance info
    tv = TradingVault(blockchain, block_id, lptoken_address)

    holdings_amount = tv.balance_of(wallet)

    position_data = [{"address": "0x0d80D7f7719407523A09ee2ef7eD573e0eA3487a", "balance": holdings_amount}]
    underlying_data = [{"address": tv.standard_token, "balance": holdings_amount}]

    data = {
        "blockchain": blockchain,
        "block_id": block_id,
        "protocol": "Mu Exchange",
        "version": 0,
        "wallet": wallet,
        "decimals": tv.decimals,
        "positions": {
            "0x0d80D7f7719407523A09ee2ef7eD573e0eA3487a": {
                "holdings": position_data,
                "underlyings": underlying_data,
            }
        },
    }

    return data


if __name__ == "__main__":
    get_protocol_data_for(
        "gnosis", "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f", "0x0d80D7f7719407523A09ee2ef7eD573e0eA3487a"
    )
