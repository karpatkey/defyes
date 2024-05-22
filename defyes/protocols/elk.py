import logging
from decimal import Decimal
from typing import List, Tuple

import requests
from defabipedia import Chain
from karpatkit.cache import const_call
from karpatkit.constants import ABI_TOKEN_SIMPLIFIED, Address
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, get_decimals, get_logs_web3, to_token_amount

logger = logging.getLogger(__name__)

# API Call - List of the latest pools
API_ELK_POOLS = "https://api.elk.finance/v2/info/latest_pools"

# LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast
ABI_LPTOKEN = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"kLast","inputs":[],"constant":true}]'

# Pool ABI - balanceOf, boosterEarned, boosterToken, earned, rewardsToken, totalSupply, boosterRewardPerToken, rewardPerToken
ABI_POOL = '[{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"account","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"boosterEarned","inputs":[{"type":"address","name":"account","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"boosterToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"earned","inputs":[{"type":"address","name":"account","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"rewardsToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"boosterRewardPerToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"rewardPerToken","inputs":[]}]'

# Swap Event Signature
SWAP_EVENT_SIGNATURE = "Swap(address,uint256,uint256,uint256,uint256,address)"


def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_data = {}

    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

    lptoken_data["decimals"] = const_call(lptoken_data["contract"].functions.decimals())
    lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)
    lptoken_data["token0"] = const_call(lptoken_data["contract"].functions.token0())
    lptoken_data["token1"] = const_call(lptoken_data["contract"].functions.token1())
    lptoken_data["reserves"] = lptoken_data["contract"].functions.getReserves().call(block_identifier=block)
    lptoken_data["kLast"] = lptoken_data["contract"].functions.kLast().call(block_identifier=block)

    # WARNING: Fees are deactivated in Elk
    lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"]

    return lptoken_data


def get_pool_address(web3, token0, token1, block, blockchain):
    # FIXME: no need to use block. Latest can be hardcoded for this function.
    pools = requests.get(API_ELK_POOLS).json()
    symbols = []
    for token in [token0, token1]:
        token_contract = get_contract(token, blockchain, web3=web3, abi=ABI_TOKEN_SIMPLIFIED, block=block)
        symbol = const_call(token_contract.functions.symbol())

        if "wrapped" in const_call(token_contract.functions.name()).lower():
            symbol = symbol[1 : len(symbol)]

        symbol = "XGTV2" if symbol == "XGT" else symbol  # Special Case: symbol = 'XGT' -> XGTV2

        symbols.append(symbol)

    pool_blockchain = blockchain
    if blockchain == Chain.POLYGON:
        pool_blockchain = "matic"
    if blockchain == Chain.GNOSIS:
        pool_blockchain = "xdai"

    pool_ids = ["-".join(symbols), "-".join(symbols[::-1])]
    pool_address = None
    for pool_id in pool_ids:
        try:
            pool_address = pools[pool_blockchain][pool_id]["address"]
            break
        except KeyError:
            pass

    return pool_address


def get_elk_rewards(web3, pool_contract, wallet, block, blockchain, decimals=True):
    """
    Returns:
        Tuple: (elk_token_address, balance)
    """
    elk_token_address = const_call(pool_contract.functions.rewardsToken())
    elk_rewards = pool_contract.functions.earned(wallet).call(block_identifier=block)

    return [elk_token_address, to_token_amount(elk_token_address, elk_rewards, blockchain, web3, decimals)]


def get_booster_rewards(web3, pool_contract, wallet, block, blockchain, decimals=True) -> List[Tuple]:
    """
    Returns:
        List[Tuple]: List of (reward_token_address, balance)
    """
    rewards = []
    booster_token_address = const_call(pool_contract.functions.boosterToken())
    if booster_token_address != Address.ZERO:
        booster_rewards = Decimal(pool_contract.functions.boosterEarned(wallet).call(block_identifier=block))
        rewards = [
            booster_token_address,
            to_token_amount(booster_token_address, booster_rewards, blockchain, web3, decimals),
        ]

    return rewards


def get_all_rewards(
    wallet, lptoken_address, block, blockchain, web3=None, decimals=True, pool_contract=None
) -> List[Tuple]:
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if pool_contract is None:
        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)
        pool_address = get_pool_address(web3, lptoken_data["token0"], lptoken_data["token1"], block, blockchain)
        pool_contract = get_contract(pool_address, blockchain, web3=web3, abi=ABI_POOL, block=block)

    elk_rewards = get_elk_rewards(web3, pool_contract, wallet, block, blockchain, decimals=decimals)
    all_rewards.append(elk_rewards)

    booster_rewards = get_booster_rewards(web3, pool_contract, wallet, block, blockchain, decimals=decimals)
    if booster_rewards:
        all_rewards.append(booster_rewards)

    return all_rewards


def underlying(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, reward=False):
    """
    Returns:
        List[List[Tuple]]: List of [List(liquidity_token_address, balance, staked_balance), List(reward_token_address, balance)]
    """
    result = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)
    pool_address = get_pool_address(web3, lptoken_data["token0"], lptoken_data["token1"], block, blockchain)

    if pool_address is None:
        logging.warning(f"Cannot find Elk Pool Address for LPToken Address: {lptoken_address}")
        return None

    pool_contract = get_contract(pool_address, blockchain, web3=web3, abi=ABI_POOL, block=block)

    # WARNING: Fees are deactivated in Elk
    pool_balance_fraction = (
        lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block) / lptoken_data["totalSupply"]
    )
    pool_staked_fraction = (
        pool_contract.functions.balanceOf(wallet).call(block_identifier=block) / lptoken_data["totalSupply"]
    )

    for token, reserve in zip([lptoken_data["token0"], lptoken_data["token1"]], lptoken_data["reserves"]):
        balance = to_token_amount(token, reserve, blockchain, web3, decimals)
        result.append([token, balance * Decimal(pool_balance_fraction), balance * Decimal(pool_staked_fraction)])
    # FIXME: This exists only to keep compatibility with production
    result = [result]

    if reward is True:
        all_rewards = get_all_rewards(
            wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals, pool_contract=pool_contract
        )
        result.append(all_rewards)

    return result


def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):
    """
    Returns:
        List[Tuple] : (liquidity_token_address, balance)
    """
    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)
    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

    reserves = lptoken_contract.functions.getReserves().call(block_identifier=block)[:2]
    for token, reserve in zip(["token0", "token1"], reserves):
        func = getattr(lptoken_contract.functions, token)
        token_address = const_call(func())
        balances.append([token_address, to_token_amount(token_address, reserve, blockchain, web3, decimals)])

    return balances


def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):
    result = {}

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block_start)

    token0 = const_call(lptoken_contract.functions.token0())
    token1 = const_call(lptoken_contract.functions.token1())
    result["swaps"] = []

    decimals0 = get_decimals(token0, blockchain, web3=web3) if decimals else 0
    decimals1 = get_decimals(token1, blockchain, web3=web3) if decimals else 0

    swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()
    swap_logs = get_logs_web3(
        blockchain=blockchain,
        address=lptoken_address,
        block_start=block_start,
        block_end=block_end,
        topics=[swap_event],
    )

    for swap_log in swap_logs:
        if int(swap_log["data"].hex()[2:66], 16) == 0:
            token = token1
            amount = Decimal(0.003 * int(swap_log["data"].hex()[67:130], 16)) / Decimal(10**decimals1)
        else:
            token = token0
            amount = Decimal(0.003 * int(swap_log["data"].hex()[2:66], 16)) / Decimal(10**decimals0)

        swap_data = {"block": swap_log["blockNumber"], "token": token, "amount": amount}

        result["swaps"].append(swap_data)

    return result


# #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_apr(lptoken_address, blockchain, block, web3=None, index=0):
#     if web3 is None:
#         web3 = get_node(blockchain)

#     lptoken_address = Web3.to_checksum_address(lptoken_address)
#     lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

#     pool_address = get_pool_address(web3, lptoken_data['token0'], lptoken_data['token1'], block, blockchain)

#     if pool_address is None:
#         print('Error: Cannot find Elk Pool Address for LPToken Address: ', lptoken_address)
#         return None

#     pool_contract = get_contract(pool_address, blockchain, web3=web3, abi=ABI_POOL, block=block)

#     booster_token = pool_contract.functions.boosterToken().call()
#     if booster_token is not None and booster_token != Address.ZERO:
#         booster_token_decimals = get_decimals(booster_token, blockchain, web3=web3)
#         booster_reward_per_token = pool_contract.functions.boosterRewardPerToken().call(block_identifier=block) / (10**booster_token_decimals)
#         booster_token_price = Prices.get_price(booster_token, block, blockchain)
#     else:
#         booster_reward_per_token = 0
#         booster_token_price = 0

#     rewards_token = pool_contract.functions.rewardsToken().call()
#     rewards_token_decimals = get_decimals(rewards_token, blockchain, web3=web3)
#     reward_per_token = pool_contract.functions.rewardPerToken().call(block_identifier=block) / (10**rewards_token_decimals)
#     rewards_token_price = Prices.get_price(rewards_token, block, blockchain)

#     total_rewards = (booster_reward_per_token * booster_token_price + reward_per_token * rewards_token_price) * (lptoken_data['totalSupply'] / (10**lptoken_data['decimals']))

#     balances = pool_balances(lptoken_address, block, blockchain)
#     token_addresses = [balances[i][0] for i in range(len(balances))]
#     token_prices = [Prices.get_price(token_addresses[i], block, blockchain) for i in range(len(token_addresses))]
#     tvl = sum([balances[i][1] * token_prices[i] for i in range(len(token_addresses))])

#     apr = ((total_rewards) / tvl) * 100

#     return apr
