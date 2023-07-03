from typing import List, Union

from web3 import Web3

from defyes.cache import const_call
from defyes.constants import ETHTokenAddr
from defyes.functions import get_contract, get_node, to_token_amount

CUSDCV3_ADDRESS = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"
CWETHV3_ADDRESS = "0xA17581A9E3356d9A858b789D68B4d866e593aE94"

REWARDS_ADDRESS = "0x1B0e765F6224C21223AeA2af16c1C46E38885a40"

CTOKEN_ABI = '[{"inputs":[],"name":"baseToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"userBasic","outputs":[{"internalType":"int104","name":"principal","type":"int104"},{"internalType":"uint64","name":"baseTrackingIndex","type":"uint64"},{"internalType":"uint64","name":"baseTrackingAccrued","type":"uint64"},{"internalType":"uint16","name":"assetsIn","type":"uint16"},{"internalType":"uint8","name":"_reserved","type":"uint8"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

CTOKEN_REWARDS_ABI = '[{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"rewardsClaimed","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# TODO: till 29-4-2023 only cUSDC and cWETH exists, there will be more and then a token list would be nice to fetch from blockchain.


def underlying(
    wallet: str, token_address: str, block: Union[str, int], blockchain: str, web3: object = None, decimals: bool = True
) -> List[List]:
    """give the underlying token and amounts of this protocol

    Args:
        wallet (str): _description_
        token_address (str): _description_
        block (Union[str,int]): _description_
        blockchain (str): _description_
        web3 (_type_, optional): _description_. Defaults to None.
        decimals (bool, optional): _description_. Defaults to True.
    """
    balances = []
    web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    token_address = Web3.to_checksum_address(token_address)

    cToken_instance = get_contract(token_address, blockchain, abi=CTOKEN_ABI, web3=web3, block=block)
    cToken_balance = cToken_instance.functions.balanceOf(wallet).call(block_identifier=block)
    base_token = const_call(cToken_instance.functions.baseToken())
    balances.append([base_token, to_token_amount(base_token, cToken_balance, blockchain, web3, decimals)])

    return balances


def get_all_rewards(
    wallet: str, token_address: str, block: Union[int, str], blockchain: str, web3=None, decimals: bool = True
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
    web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    token_address = Web3.to_checksum_address(token_address)

    cToken_instance = get_contract(REWARDS_ADDRESS, blockchain, abi=CTOKEN_REWARDS_ABI, web3=web3, block=block)
    cToken_rewards = cToken_instance.functions.rewardsClaimed(token_address, wallet).call(block_identifier=block)

    rewards.append([ETHTokenAddr.COMP, to_token_amount(ETHTokenAddr.COMP, cToken_rewards, blockchain, web3, decimals)])

    return rewards
