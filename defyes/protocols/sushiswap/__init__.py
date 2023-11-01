import json
import logging
import os
from decimal import Decimal
from pathlib import Path
from typing import Union

from web3 import Web3
from web3.exceptions import ABIFunctionNotFound

from defyes.cache import const_call
from defyes.constants import Address, Chain
from defyes.explorer import ChainExplorer
from defyes.functions import get_contract, get_decimals, get_logs_web3, last_block, to_token_amount
from defyes.lazytime import Duration, Time
from defyes.node import get_node
from defyes.prices.prices import get_price

DB_FILE = Path(__file__).parent / "db.json"

logger = logging.getLogger(__name__)

BLOCK_START = {
    "0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd": 10736242,
    "0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d": 12428169,
    "0x0769fd68dFb93167989C6f7254cd0D766Fb2841F": 13911377,
    "0xdDCbf776dF3dE60163066A5ddDF2277cB445E0F3": 16655565,
}

MASTERCHEF_V1 = "0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd"

MASTERCHEF_V2 = "0xEF0881eC094552b2e128Cf945EF17a6752B4Ec5d"

# Polygon - MiniChef Contract Address
MINICHEF_POLYGON = "0x0769fd68dFb93167989C6f7254cd0D766Fb2841F"

# xDAI - MiniChef Contract Address
MINICHEF_GNOSIS = "0xdDCbf776dF3dE60163066A5ddDF2277cB445E0F3"

# Chefs V2 ABI - SUSHI, rewarder, pendingSushi, lpToken, userInfo, poolLength, poolInfo, sushiPerBlock, sushiPerSecond, totalAllocPoint
ABI_CHEF_V2 = '[{"inputs":[],"name":"SUSHI","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rewarder","outputs":[{"internalType":"contract IRewarder","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingSushi","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"lpToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"pools","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint128","name":"accSushiPerShare","type":"uint128"},{"internalType":"uint64","name":"lastRewardBlock","type":"uint64"},{"internalType":"uint64","name":"allocPoint","type":"uint64"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"sushiPerBlock","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"sushiPerSecond","inputs":[]}, {"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Chefs V1 ABI - sushi, rewarder, pendingSushi, poolInfo, userInfo, poolLength, sushiPerBlock, totalAllocPoint
ABI_CHEF_V1 = '[{"inputs":[],"name":"sushi","outputs":[{"internalType":"contract SushiToken","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"rewarder","outputs":[{"internalType":"contract IRewarder","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"_pid","type":"uint256"},{"internalType":"address","name":"_user","type":"address"}],"name":"pendingSushi","outputs":[{"internalType":"uint256","name":"pending","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"contract IERC20","name":"lpToken","type":"address"},{"internalType":"uint256","name":"allocPoint","type":"uint256"},{"internalType":"uint256","name":"lastRewardBlock","type":"uint256"},{"internalType":"uint256","name":"accSushiPerShare","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"address","name":"","type":"address"}],"name":"userInfo","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"int256","name":"rewardDebt","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"sushiPerBlock","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalAllocPoint","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Rewarder ABI - pendingTokens, rewardPerSecond, poolInfo
ABI_REWARDER = '[{"inputs":[{"internalType":"uint256","name":"pid","type":"uint256"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"pendingTokens","outputs":[{"internalType":"contract IERC20[]","name":"rewardTokens","type":"address[]"},{"internalType":"uint256[]","name":"rewardAmounts","type":"uint256[]"}],"stateMutability":"view","type":"function"}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"rewardPerSecond","inputs":[]}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"uint128","name":"accSushiPerShare","type":"uint128"},{"internalType":"uint64","name":"lastRewardBlock","type":"uint64"},{"internalType":"uint64","name":"allocPoint","type":"uint64"}],"stateMutability":"view","type":"function"}]'

# LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast
ABI_LPTOKEN = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Swap Event Signature
SWAP_EVENT_SIGNATURE = "Swap(address,uint256,uint256,uint256,uint256,address)"


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_chef_contract
# **kwargs:
# 'v1' = True -> If blockchain = ETHEREUM retrieves the MASTERCHEF_V1 Contract / 'v1' = False or not passed onto the function -> retrieves the MASTERCHEF_V2 Contract
# Output: chef_contract
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_chef_contract(web3, block, blockchain, v1=False):
    """
    :param web3:
    :param block:
    :param blockchain:
    :param v1:
    :return:
    """
    if blockchain == Chain.ETHEREUM:
        if v1 is False:
            chef_contract = get_contract(MASTERCHEF_V2, blockchain, web3=web3, abi=ABI_CHEF_V2, block=block)
        else:
            chef_contract = get_contract(MASTERCHEF_V1, blockchain, web3=web3, abi=ABI_CHEF_V1, block=block)

    elif blockchain == Chain.POLYGON:
        chef_contract = get_contract(MINICHEF_POLYGON, blockchain, web3=web3, abi=ABI_CHEF_V2, block=block)

    elif blockchain == Chain.GNOSIS:
        chef_contract = get_contract(MINICHEF_GNOSIS, blockchain, web3=web3, abi=ABI_CHEF_V2, block=block)

    return chef_contract


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info
# 'use_db' = True -> uses the /db/sushi_swap.json to improve performance / 'use_db' = False -> fetches all the data on-chain
# Output:
# 1 - Dictionary: result['chef_contract'] = chef_contract
#                 result['pool_info'] = {
#                     'poolId': poolID
#                     'allocPoint': allocPoint
#                 }
#                 result['totalAllocPoint']: totalAllocPoint
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(web3, lptoken_address, block, blockchain, use_db=True):
    """
    :param web3:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param use_db:
    :return:
    """
    result = {}

    if use_db is True:
        with open(DB_FILE) as db_file:
            db_data = json.load(db_file)

        if blockchain == Chain.ETHEREUM:
            try:
                result["chef_contract"] = get_chef_contract(web3, block, blockchain)
                result["pool_info"] = {
                    "poolId": db_data[blockchain]["poolsv2"][lptoken_address],
                    "allocPoint": result["chef_contract"]
                    .functions.poolInfo(db_data[blockchain]["poolsv2"][lptoken_address])
                    .call(block_identifier=block)[2],
                }
                result["totalAllocPoint"] = (
                    result["chef_contract"].functions.totalAllocPoint().call(block_identifier=block)
                )

                return result

            except:
                try:
                    result["chef_contract"] = get_chef_contract(web3, block, blockchain, v1=True)
                    result["pool_info"] = {
                        "poolId": db_data[blockchain]["poolsv1"][lptoken_address],
                        "allocPoint": result["chef_contract"]
                        .functions.poolInfo(db_data[blockchain]["poolsv1"][lptoken_address])
                        .call(block_identifier=block)[1],
                    }
                    result["totalAllocPoint"] = (
                        result["chef_contract"].functions.totalAllocPoint().call(block_identifier=block)
                    )

                    return result

                except:
                    return None

        else:
            try:
                result["chef_contract"] = get_chef_contract(web3, block, blockchain)
                result["pool_info"] = {
                    "poolId": db_data[blockchain]["pools"][lptoken_address],
                    "allocPoint": result["chef_contract"]
                    .functions.poolInfo(db_data[blockchain]["pools"][lptoken_address])
                    .call(block_identifier=block)[2],
                }
                result["totalAllocPoint"] = (
                    result["chef_contract"].functions.totalAllocPoint().call(block_identifier=block)
                )

                return result

            except:
                return None

    else:
        result["chef_contract"] = get_chef_contract(web3, block, blockchain)

        pool_length = result["chef_contract"].functions.poolLength().call(block_identifier=block)

        for pool_id in range(pool_length):
            address = const_call(result["chef_contract"].functions.lpToken(pool_id))

            if address == lptoken_address:
                result["pool_info"] = {
                    "poolId": pool_id,
                    "allocPoint": result["chef_contract"].functions.poolInfo(pool_id).call(block_identifier=block)[2],
                }
                result["totalAllocPoint"] = (
                    result["chef_contract"].functions.totalAllocPoint().call(block_identifier=block)
                )

                return result

        # This section searches if the pool it's a V1 pool (only in Chain.ETHEREUM)
        if blockchain == Chain.ETHEREUM:
            result["chef_contract"] = get_chef_contract(web3, block, blockchain, v1=True)

            pool_length = result["chef_contract"].functions.poolLength().call(block_identifier=block)

            for pool_id in range(pool_length):
                # TODO: determine if const_call can be used
                address = result["chef_contract"].functions.poolInfo(pool_id).call(block_identifier=block)[0]

                if address == lptoken_address:
                    result["pool_info"] = {
                        "poolId": pool_id,
                        "allocPoint": result["chef_contract"]
                        .functions.poolInfo(pool_id)
                        .call(block_identifier=block)[1],
                    }
                    result["totalAllocPoint"] = (
                        result["chef_contract"].functions.totalAllocPoint().call(block_identifier=block)
                    )

                    return result

    # If the lptoken_address doesn't match with a V2 or V1 pool
    return None


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# 'web3' = web3 (Node) -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    """
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_data = {}
    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

    lptoken_data["decimals"] = const_call(lptoken_data["contract"].functions.decimals())
    lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)
    lptoken_data["token0"] = const_call(lptoken_data["contract"].functions.token0())
    lptoken_data["token1"] = const_call(lptoken_data["contract"].functions.token1())
    lptoken_data["reserves"] = lptoken_data["contract"].functions.getReserves().call(block_identifier=block)
    lptoken_data["kLast"] = lptoken_data["contract"].functions.kLast().call(block_identifier=block)

    root_k = (Decimal(lptoken_data["reserves"][0]) * Decimal(lptoken_data["reserves"][1])).sqrt()
    root_k_last = Decimal(lptoken_data["kLast"]).sqrt()

    if root_k > root_k_last:
        lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"] * 6 * root_k / (5 * root_k + root_k_last)
    else:
        lptoken_data["virtualTotalSupply"] = Decimal(lptoken_data["totalSupply"])

    return lptoken_data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_virtual_total_supply
# 'web3' = web3 (Node) -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_virtual_total_supply(lptoken_address, block, blockchain, web3=None):
    """

    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_data = {}

    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

    lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)
    lptoken_data["reserves"] = lptoken_data["contract"].functions.getReserves().call(block_identifier=block)
    lptoken_data["kLast"] = lptoken_data["contract"].functions.kLast().call(block_identifier=block)

    root_k = (Decimal(lptoken_data["reserves"][0]) * Decimal(lptoken_data["reserves"][1])).sqrt()
    root_k_last = Decimal(lptoken_data["kLast"]).sqrt()

    return lptoken_data["totalSupply"] * 6 * root_k / (5 * root_k + root_k_last)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewarder_contract
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id):
    """
    :param web3:
    :param block:
    :param blockchain:
    :param chef_contract:
    :param pool_id:
    :return:
    """
    # TODO: determine if const_call can be used
    rewarder_contract_address = chef_contract.functions.rewarder(pool_id).call(block_identifier=block)
    if rewarder_contract_address != Address.ZERO:
        rewarder_contract = get_contract(
            rewarder_contract_address, blockchain, web3=web3, abi=ABI_REWARDER, block=block
        )
    else:
        rewarder_contract = None

    return rewarder_contract


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_sushi_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [sushi_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_sushi_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True):
    """
    :param web3:
    :param wallet:
    :param chef_contract:
    :param pool_id:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    try:
        sushi_address = const_call(chef_contract.functions.SUSHI())
    except ABIFunctionNotFound:
        sushi_address = const_call(chef_contract.functions.sushi())

    sushi_rewards = chef_contract.functions.pendingSushi(pool_id, wallet).call(block_identifier=block)

    return [sushi_address, to_token_amount(sushi_address, sushi_rewards, blockchain, web3, decimals)]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True):
    """
    :param web3:
    :param wallet:
    :param chef_contract:
    :param pool_id:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    rewards = []

    rewarder_contract = get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)

    if rewarder_contract is not None:
        pending_tokens_info = rewarder_contract.functions.pendingTokens(pool_id, wallet, 1).call(block_identifier=block)
        pending_tokens_addresses = pending_tokens_info[0]
        pending_token_amounts = pending_tokens_info[1]

        for i in range(len(pending_tokens_addresses)):
            rewards.append(
                [
                    pending_tokens_addresses[i],
                    to_token_amount(pending_tokens_addresses[i], pending_token_amounts[i], blockchain, web3, decimals),
                ]
            )

    return rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'pool_info' = Dictionary -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, pool_info=None):
    """
    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param pool_info:
    :return:
    """
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if pool_info is None:
        pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

    if pool_info is None:
        logger.error("Incorrect SushiSwap LPToken Address: %s", lptoken_address)
        return None

    pool_id = pool_info["pool_info"]["poolId"]
    chef_contract = pool_info["chef_contract"]

    sushi_rewards = get_sushi_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=decimals)
    all_rewards.append(sushi_rewards)

    if chef_contract.address != MASTERCHEF_V1:
        rewards = get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=decimals)

        if len(rewards) > 0:
            for reward in rewards:
                all_rewards.append(reward)

    return all_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, reward=False):
    """
    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param reward:
    :return:
    """

    result = []
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

    if pool_info is None:
        print("Error: Incorrect SushiSwap LPToken Address: ", lptoken_address)
        return None

    pool_id = pool_info["pool_info"]["poolId"]
    chef_contract = pool_info["chef_contract"]

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    pool_balance_fraction = lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block)
    pool_balance_fraction /= Decimal(lptoken_data["virtualTotalSupply"])

    pool_staked_fraction = chef_contract.functions.userInfo(pool_id, wallet).call(block_identifier=block)[0]
    pool_staked_fraction /= Decimal(lptoken_data["virtualTotalSupply"])

    for n, reserve in enumerate(lptoken_data["reserves"]):
        try:
            getattr(lptoken_data["contract"].functions, "token" + str(n))
        except AttributeError:
            continue

        token_address = lptoken_data["token" + str(n)]
        token_balance = to_token_amount(token_address, reserve, blockchain, web3, decimals)

        balances.append([token_address, token_balance * pool_balance_fraction, token_balance * pool_staked_fraction])

    if reward is True:
        all_rewards = get_all_rewards(
            wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals, pool_info=pool_info
        )

        result.append(balances)
        result.append(all_rewards)

    else:
        result = balances

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 element:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):
    """
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)
    reserves = lptoken_contract.functions.getReserves().call(block_identifier=block)

    for n, reserve in enumerate(reserves):
        func = getattr(lptoken_contract.functions, "token" + str(n), None)
        if func is None:
            continue
        token_address = const_call(func())
        balances.append([token_address, to_token_amount(token_address, reserve, blockchain, web3, decimals)])

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# swap_fees
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):
    """
    :param lptoken_address:
    :param block_start:
    :param block_end:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    result = {}

    if web3 is None:
        web3 = get_node(blockchain, block=block_start)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block_start)

    token0 = const_call(lptoken_contract.functions.token0())
    token1 = const_call(lptoken_contract.functions.token1())
    result["swaps"] = []

    decimals0 = get_decimals(token0, blockchain, web3=web3) if decimals else Decimal("0")
    decimals1 = get_decimals(token1, blockchain, web3=web3) if decimals else Decimal("0")

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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_wallet_by_tx
# 'web3' = web3 (Node) -> Improves performance
# 'signature' = signature of the type of transaction that will be searched for
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_wallet_by_tx(lptoken_address, block, blockchain, web3=None):
    """
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if isinstance(block, str):
        if block == "latest":
            block = last_block(blockchain, web3=web3)

    chef_contract = get_pool_info(web3, lptoken_address, block, blockchain)["chef_contract"]

    if chef_contract is not None:
        tx_hex_bytes = Web3.keccak(text="deposit(uint256,uint256,address)")[0:4].hex()

        lptoken_txs = ChainExplorer(blockchain).get_token_transactions(
            lptoken_address, chef_contract.address, BLOCK_START[chef_contract.address], block
        )
        for lptoken_tx in lptoken_txs:
            txs = ChainExplorer(blockchain).get_transactions(
                lptoken_tx["from"], BLOCK_START[chef_contract.address], block
            )

            for tx in txs:
                if tx["input"][0:10] == tx_hex_bytes:
                    return tx["from"]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards_per_unit
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards_per_unit(lptoken_address, blockchain, web3=None, block="latest"):
    """
    :param lptoken_address:
    :param blockchain:
    :param web3:
    :param block:
    :return:
    """
    result = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

    if pool_info is None:
        print("Error: Incorrect SushiSwap LPToken Address: ", lptoken_address)
        return None

    chef_contract = pool_info["chef_contract"]
    pool_id = pool_info["pool_info"]["poolId"]

    sushi_reward_data = {}

    try:
        sushi_reward_data["sushi_address"] = const_call(chef_contract.functions.SUSHI())
    except ABIFunctionNotFound:
        sushi_reward_data["sushi_address"] = const_call(chef_contract.functions.sushi())

    try:
        sushi_reward_data["sushiPerBlock"] = chef_contract.functions.sushiPerBlock().call(block_identifier=block) * (
            pool_info["pool_info"]["allocPoint"] / Decimal(pool_info["totalAllocPoint"])
        )
    except ABIFunctionNotFound:
        sushi_reward_data["sushiPerSecond"] = chef_contract.functions.sushiPerSecond().call(block_identifier=block) * (
            pool_info["pool_info"]["allocPoint"] / Decimal(pool_info["totalAllocPoint"])
        )

    result.append(sushi_reward_data)

    try:
        reward_data = {}

        rewarder_contract = get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)
        rewarder_pool_info = rewarder_contract.functions.poolInfo(pool_id).call(block_identifier=block)
        rewarder_alloc_point = rewarder_pool_info[2]

        # Rewarder Total Allocation Point Calculation
        rewarder_total_alloc_point = 0
        for i in range(chef_contract.functions.poolLength().call(block_identifier=block)):
            rewarder_total_alloc_point += rewarder_contract.functions.poolInfo(i).call(block_identifier=block)[2]

        reward_data["reward_address"] = rewarder_contract.functions.pendingTokens(pool_id, Address.ZERO, 1).call(
            block_identifier=block
        )[0][0]

        try:
            reward_data["rewardPerSecond"] = rewarder_contract.functions.rewardPerSecond().call(
                block_identifier=block
            ) * (rewarder_alloc_point / Decimal(rewarder_total_alloc_point))
        except:
            reward_data["rewardPerSecond"] = Decimal(0)

        result.append(reward_data)

    except:
        pass

    return result


# def get_apr(lptoken_address, blockchain, web3=None, block='latest'):
#     if web3 is None:
#         web3 = get_node(blockchain, block=block)

#     data = get_rewards_per_unit(lptoken_address, blockchain, web3=web3, block=block)

#     sushi_price = Prices.get_price(data[0]['sushi_address'], block, blockchain, web3=web3)
#     sushi_decimals = get_decimals(data[0]['sushi_address'], blockchain, web3=web3)

#     try:
#         sushi_per_block = data[0]['sushiPerBlock']
#         blocks_per_year = get_blocks_per_year(blockchain)
#         sushi_per_year = sushi_per_block * blocks_per_year / (10**sushi_decimals)
#     except:
#         sushi_per_second = data[0]['sushiPerSecond']
#         sushi_per_year = sushi_per_second * (3600 * 24 * 365) / (10**sushi_decimals)

#     try:
#         reward_price = Prices.get_price(data[1]['reward_address'], block, blockchain, web3=web3)
#         reward_decimals = get_decimals(data[1]['reward_address'], blockchain, web3=web3)

#         reward_per_year = data[1]['rewardPerSecond'] * (3600 * 24 * 365) / (10**reward_decimals)
#     except:
#         reward_price = 0
#         reward_per_year = 0

#     balances = pool_balances(lptoken_address, block, blockchain)
#     token_addresses = [balances[i][0] for i in range(len(balances))]
#     token_prices = [Prices.get_price(token_addresses[i], block, blockchain) for i in range(len(token_addresses))]
#     tvl = sum([balances[i][1] * token_prices[i] for i in range(len(token_addresses))])

#     apr = ((sushi_per_year * sushi_price + reward_per_year * reward_price) / tvl) * 100

#     return apr


def get_swap_fees_APR(
    lptoken_address: str,
    blockchain: str,
    block_end: Union[int, str] = "latest",
    web3=None,
    days: int = 1,
    apy: bool = False,
) -> int:
    chain_explorer = ChainExplorer(blockchain)
    block_start = chain_explorer.block_from_time(Time(chain_explorer.time_from_block(block_end)) - Duration.days(days))
    fees = swap_fees(lptoken_address, block_start, block_end, blockchain, web3)
    token0 = fees["swaps"][0]["token"]
    token0_fees = [0]
    token1_fees = [0]
    for k in fees["swaps"]:
        if k["token"] == token0:
            token0_fees.append(k["amount"])
        elif k["token"] != token0:
            token1 = k["token"]
            token1_fees.append(k["amount"])

    token0_fees_usd = get_price(token0, block_end, blockchain, web3)[0] * sum(token0_fees)
    token1_fees_usd = get_price(token1, block_end, blockchain, web3)[0] * sum(token1_fees)
    token_fees_usd = token0_fees_usd + token1_fees_usd
    pool_contract = get_contract(lptoken_address, blockchain, web3, ABI_LPTOKEN, block_end)
    token0_address = const_call(pool_contract.functions.token0())
    token0_price = get_price(token0_address, block_end, blockchain, web3)[0]
    token0_decimals = get_decimals(token0_address, blockchain, web3=web3, block=block_end)
    token1_address = const_call(pool_contract.functions.token1())
    token1_price = get_price(token1_address, block_end, blockchain, web3)[0]
    token1_decimals = get_decimals(token1_address, blockchain, web3=web3, block=block_end)
    reserves = const_call(pool_contract.functions.getReserves())
    tvl = (reserves[0] / 10**token0_decimals) * token0_price + (reserves[1] / 10**token1_decimals) * token1_price
    apr = token_fees_usd / tvl * (365 / days) * 100
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        apy = (1 + (apr / seconds_per_year)) ** (seconds_per_year) - 1
        return apy
    else:
        return apr


# #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # update_db
# #----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db():
    update = False

    try:
        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/db/SushiSwap_db.json", "r") as db_file:
            # Reading from json file
            db_data = json.load(db_file)
    except:
        db_data = {
            Chain.ETHEREUM: {"poolsv2": {}, "poolsv1": {}},
            Chain.POLYGON: {"pools": {}},
            Chain.GNOSIS: {"pools": {}},
        }

    web3 = get_node(Chain.ETHEREUM)

    master_chefv2 = get_chef_contract(web3, "latest", Chain.ETHEREUM)
    db_pool_length = len(db_data[Chain.ETHEREUM]["poolsv2"])
    pools_delta = master_chefv2.functions.poolLength().call(block_identifier="latest") - db_pool_length

    if pools_delta > 0:
        update = True

        for i in range(pools_delta):
            lptoken_address = master_chefv2.functions.lpToken(db_pool_length + i).call(block_identifier="latest")
            db_data[Chain.ETHEREUM]["poolsv2"][lptoken_address] = db_pool_length + i

    master_chefv1 = get_chef_contract(web3, "latest", Chain.ETHEREUM, v1=True)
    db_pool_length = len(db_data[Chain.ETHEREUM]["poolsv1"])
    pools_delta = master_chefv1.functions.poolLength().call(block_identifier="latest") - db_pool_length

    if pools_delta > 0:
        update = True

        for i in range(pools_delta):
            lptoken_address = master_chefv1.functions.poolInfo(db_pool_length + i).call(block_identifier="latest")[0]
            db_data[Chain.ETHEREUM]["poolsv1"][lptoken_address] = db_pool_length + i

    web3 = get_node(Chain.POLYGON)

    mini_chef = get_chef_contract(web3, "latest", Chain.POLYGON)
    db_pool_length = len(db_data[Chain.POLYGON]["pools"])
    pools_delta = mini_chef.functions.poolLength().call(block_identifier="latest") - db_pool_length

    if pools_delta > 0:
        update = True

        for i in range(pools_delta):
            lptoken_address = mini_chef.functions.lpToken(db_pool_length + i).call(block_identifier="latest")
            db_data[Chain.POLYGON]["pools"][lptoken_address] = db_pool_length + i

    web3 = get_node(Chain.GNOSIS)

    mini_chef = get_chef_contract(web3, "latest", Chain.GNOSIS)
    db_pool_length = len(db_data[Chain.GNOSIS]["pools"])
    pools_delta = mini_chef.functions.poolLength().call(block_identifier="latest") - db_pool_length

    if pools_delta > 0:
        update = True

        for i in range(pools_delta):
            lptoken_address = mini_chef.functions.lpToken(db_pool_length + i).call(block_identifier="latest")
            db_data[Chain.GNOSIS]["pools"][lptoken_address] = db_pool_length + i

    if update is True:
        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/db/SushiSwap_db.json", "w") as db_file:
            json.dump(db_data, db_file)
