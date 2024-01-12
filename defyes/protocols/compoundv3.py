from typing import List, Union

from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, to_token_amount

CUSDCV3_ADDRESS = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"
CWETHV3_ADDRESS = "0xA17581A9E3356d9A858b789D68B4d866e593aE94"

REWARDS_ADDRESS = "0x1B0e765F6224C21223AeA2af16c1C46E38885a40"

COMET_ABI = '[{"inputs":[],"name":"baseToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userBasic","outputs":[{"internalType":"int104","name":"principal","type":"int104"},{"internalType":"uint64","name":"baseTrackingIndex","type":"uint64"},{"internalType":"uint64","name":"baseTrackingAccrued","type":"uint64"},{"internalType":"uint16","name":"assetsIn","type":"uint16"},{"internalType":"uint8","name":"_reserved","type":"uint8"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

COMET_REWARDS_ABI = '[{"inputs":[{"internalType":"address","name":"comet","type":"address"},{"internalType":"address","name":"account","type":"address"}],"name":"getRewardOwed","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"owed","type":"uint256"}],"internalType":"struct CometRewards.RewardOwed","name":"","type":"tuple"}],"stateMutability":"nonpayable","type":"function"}]'

# TODO: till 29-4-2023 only cUSDC and cWETH exists, there will be more and then a token list would be nice to fetch from blockchain.
# TODO: the protocol is incomplete since it doesn't have the logic to get the amount of collateral and borrowed tokens.


def underlying(
    wallet: str, comet_address: str, block: Union[str, int], blockchain: str, web3: object = None, decimals: bool = True
) -> List[List]:
    """give the underlying token and amounts of this protocol

    Args:
        wallet (str): _description_
        comet_address (str): _description_
        block (Union[str,int]): _description_
        blockchain (str): _description_
        web3 (_type_, optional): _description_. Defaults to None.
        decimals (bool, optional): _description_. Defaults to True.
    """
    balances = []
    web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    comet_address = Web3.to_checksum_address(comet_address)

    comet_instance = get_contract(comet_address, blockchain, abi=COMET_ABI, web3=web3, block=block)
    comet_balance = comet_instance.functions.balanceOf(wallet).call(block_identifier=block)
    base_token = const_call(comet_instance.functions.baseToken())
    balances.append([base_token, to_token_amount(base_token, comet_balance, blockchain, web3, decimals)])

    return balances


def get_all_rewards(
    wallet: str, comet_address: str, block: Union[int, str], blockchain: str, web3=None, decimals: bool = True
) -> List[List]:
    """_summary_

    Args:
        wallet (str): _description_
        block (Union[int, str]): _description_
        blockchain (str): _description_
        web3 (_type_, optional): _description_. Defaults to None.
        decimals (bool, optional): _description_. Defaults to True.

    Returns:
        List[List]: _description_
    """
    rewards = []
    web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    comet_address = Web3.to_checksum_address(comet_address)

    comet_instance = get_contract(REWARDS_ADDRESS, blockchain, abi=COMET_REWARDS_ABI, web3=web3, block=block)
    comet_rewards = comet_instance.functions.getRewardOwed(comet_address, wallet).call(block_identifier=block)

    rewards.append([comet_rewards[0], to_token_amount(comet_rewards[0], comet_rewards[1], blockchain, web3, decimals)])

    return rewards
