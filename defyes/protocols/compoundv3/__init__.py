from decimal import Decimal
from typing import List, Union

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from web3 import Web3

from defyes.functions import to_token_amount

from .autogenerated import Comet, CometRewards

# TODO: till 29-4-2023 only cUSDC and cWETH exists, there will be more and then a token list would be nice to fetch from blockchain.
# TODO: the protocol is incomplete since it doesn't have the logic to get the amount of collateral and borrowed tokens.


COMETS = {
    "ethereum": [EthereumTokenAddr.cUSDCv3, EthereumTokenAddr.cWETHv3],
}


class CometRewards(CometRewards):
    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: "0x1B0e765F6224C21223AeA2af16c1C46E38885a40",
    }


def get_protocol_data(blockchain: str, wallet: str, block: int | str = "latest", decimals: bool = True) -> dict:
    """
    TODO: Add documentation
    """
    wallet = Web3.to_checksum_address(wallet)
    positions = {}

    for comet_address in COMETS[blockchain]:
        comet = Comet(blockchain, block, comet_address)
        balance = comet.balance_of(wallet)
        rewards = CometRewards(blockchain, block)
        comet_rewards = rewards.get_reward_owed(comet_address, wallet)

        if balance:
            positions[comet_address] = {
                "liquidity": {
                    "underlyings": [
                        {
                            "address": comet.base_token,
                            "balance": balance / Decimal(10**comet.decimals if decimals else 1),
                        },
                    ]
                }
            }

        if comet_rewards[1] > 0:
            positions[comet_address] = positions.get(comet_address, {})
            positions[comet_address]["unclaimed_rewards"] = [
                {
                    "address": comet_rewards[0],
                    "balance": to_token_amount(comet_rewards[0], comet_rewards[1], blockchain, decimals=decimals),
                }
            ]

    return {
        "protocol": "Compoundv3",
        "blockchain": blockchain,
        "wallet": Web3.to_checksum_address(wallet),
        "block_id": block,
        "positions_key": "commet_address",
        "positions": positions,
        "version": 0,
    }


def underlying(
    wallet: str, comet_address: str, block: Union[str, int], blockchain: str, decimals: bool = True
) -> List[List]:
    """give the underlying token and amounts of this protocol

    Args:
        wallet (str): _description_
        comet_address (str): _description_
        block (Union[str,int]): _description_
        blockchain (str): _description_
        decimals (bool, optional): _description_. Defaults to True.
    """
    balances = []

    wallet = Web3.to_checksum_address(wallet)
    comet_address = Web3.to_checksum_address(comet_address)
    comet = Comet(blockchain, block, comet_address)
    balances.append([comet.base_token, comet.balance_of(wallet) / Decimal(10**comet.decimals if decimals else 1)])

    return balances


def get_all_rewards(
    wallet: str, comet_address: str, block: Union[int, str], blockchain: str, decimals: bool = True
) -> List[List]:
    """_summary_

    Args:
        wallet (str): _description_
        block (Union[int, str]): _description_
        blockchain (str): _description_
        decimals (bool, optional): _description_. Defaults to True.

    Returns:
        List[List]: _description_
    """
    rewards = []
    wallet = Web3.to_checksum_address(wallet)
    comet_address = Web3.to_checksum_address(comet_address)

    comet = CometRewards(blockchain, block)
    comet_rewards = comet.get_reward_owed(comet_address, wallet)
    rewards.append(
        [comet_rewards[0], to_token_amount(comet_rewards[0], comet_rewards[1], blockchain, decimals=decimals)]
    )

    return rewards
