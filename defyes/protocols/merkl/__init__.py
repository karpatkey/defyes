"""
This module gets data about the merkl rewards_data through the Merkl API.
"""

import json
from decimal import Decimal
from typing import Dict, List

import requests
from defabipedia import Chain
from web3 import Web3

from defyes.functions import ensure_a_block_number, get_decimals

CHAINS_ID = {
    Chain.ETHEREUM: Chain.ETHEREUM.chain_id,
    Chain.OPTIMISM: Chain.OPTIMISM.chain_id,
    Chain.GNOSIS: Chain.GNOSIS.chain_id,
    Chain.BINANCE: Chain.BINANCE.chain_id,
    Chain.ARBITRUM: Chain.ARBITRUM.chain_id,
    Chain.BASE: Chain.BASE.chain_id,
}


def get_rewards_from_api(wallet: str, blockchain: str) -> List[dict] | str:
    """Get API results for a given wallet and blockchain.

    This function makes a request to the Merl API to retrieve data for a specific wallet and blockchain.

    Args:
        wallet (str): The wallet address for which to retrieve data.
        blockchain (str): The blockchain name for which to retrieve data.

    Raises:
        ValueError: If the provided blockchain is not supported.

    Returns:
        List[dict] | str: The API results as a list of dictionaries, or an error message as a string.
    """
    try:
        chain_id = CHAINS_ID[blockchain]
    except KeyError:
        raise ValueError(f"Blockchain {blockchain} not supported")

    api_url = f"https://api.angle.money/v2/merkl?user={wallet}&AMMs=uniswapv3&AMMs=pancakeswapv3&AMMs=sushiswapv3&chainIds={chain_id}"

    response = requests.get(api_url)

    if response.status_code == 200:
        data = json.loads(response.text)
    else:
        raise ValueError(f"Request failed with status code {response.status_code}")

    rewards_data = list(data[str(chain_id)]["transactionData"].keys())

    rewards = []

    if len(rewards_data) > 0:
        for rew in rewards_data:
            claimable_reward = data[str(chain_id)]["transactionData"][rew]["claim"]
            rewards.append({"address": rew, "balance": Decimal(claimable_reward)})
        return rewards
    else:
        raise ValueError("Data retrieved is None")


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    block: str = "latest",
    decimals: bool = True,
) -> Dict:
    """Get the data for a wallet for the Merkl protocol.

    Args:
        blockchain (str): The blockchain name for which to retrieve data.
        wallet (str): The wallet address for which to retrieve data.
        block (str): The block number can only be "latest" for now.
        decimals (bool): Whether to return the data with decimals.

    Returns:
        dict: The data for the wallet for the Merkl protocol.
    """
    wallet = Web3.to_checksum_address(wallet)

    if block != "latest":
        raise ValueError("Block number can only be 'latest' for now.")

    block = ensure_a_block_number(block, blockchain)

    rewards_data = get_rewards_from_api(wallet, blockchain)

    if decimals:
        for rew in rewards_data:
            d = get_decimals(rew["address"], blockchain)
            rew["claimable_reward"] = rew["claimable_reward"] / 10**d

    data = {
        "blockchain": blockchain,
        "block": block,
        "protocol": "Merkl",
        "positions_key": None,
        "version": 0,
        "wallet": wallet,
        "decimals": "",
        "positions": {"rewards": rewards_data},
    }

    return data
