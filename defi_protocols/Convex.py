import json
import os
import logging
from pathlib import Path
from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, to_token_amount
from defi_protocols.constants import ETHEREUM, CVX_ETH, CVXCRV_ETH
from defi_protocols import Curve
from defi_protocols.misc import get_db_filename
from defi_protocols.cache import const_call

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BACKLOG LIST
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rewards when you stake CVX

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOSTER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster (Main Deposit Contract) Address
BOOSTER = '0xF403C135812408BFbE8713b5A23a04b3D48AAE31'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX REWARDS TOKEN ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX rewards token address
CVX_STAKER = '0xCF50b810E57Ac33B91dCF525C6ddd9881B139332'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX LOCKER TOKEN ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX locker token address
CVX_LOCKER = '0x72a19342e8F1838460eBFCCEf09F6585e32db86E'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster ABI - poolInfo, poolLength
ABI_BOOSTER = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"address","name":"lptoken","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"gauge","type":"address"},{"internalType":"address","name":"crvRewards","type":"address"},{"internalType":"address","name":"stash","type":"address"},{"internalType":"bool","name":"shutdown","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Rewards ABI - balanceOf, totalSupply, earned, rewardToken, extraRewardsLength, extraRewards
ABI_REWARDS = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# CVX ABI - reductionPerCliff, totalCliffs, maxSupply, totalSupply
ABI_CVX = '[{"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def get_pool_info(lptoken_address, block):
    """
    Output: pool_info method return a list with the following data:
        [0] lptoken address,
        [1] token address,
        [2] gauge address,
        [3] crvRewards address,
        [4] stash adress,
        [5] shutdown bool
    """
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Convex_db.json', 'r') as db_file:
        # Reading from json file
        db_data = json.load(db_file)

    try:
        pool_info = db_data['pools'][lptoken_address]

        if pool_info['shutdown']:
            return None
        else:
            pool_info = [lptoken_address,
                         pool_info['token'],
                         pool_info['gauge'],
                         pool_info['crvRewards'],
                         pool_info['stash'],
                         pool_info['shutdown']]
            return pool_info

    except KeyError:
        booster_contract = get_contract(BOOSTER, ETHEREUM, abi=ABI_BOOSTER, block=block)

        number_of_pools = booster_contract.functions.poolLength().call(block_identifier=block)

        for pool_id in range(number_of_pools):

            pool_info = booster_contract.functions.poolInfo(pool_id).call(block_identifier=block)
            address = pool_info[0]
            shutdown_status = pool_info[5]

            if address == lptoken_address:
                if shutdown_status is False:
                    return pool_info
                else:
                    return None

    return None


def get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):
    """
    Output:
        Tuples: [token_address, balance]
    """
    reward_token_address = rewarder_contract.functions.rewardToken().call()
    bal_rewards = rewarder_contract.functions.earned(wallet).call(block_identifier=block)

    return [reward_token_address, to_token_amount(reward_token_address, bal_rewards, blockchain, web3, decimals)]


def get_extra_rewards(web3, crv_rewards_contract, wallet, block,
                      blockchain, decimals=True):
    """
    Output: List of Tuples: [reward_token_address, balance]
    """
    extra_rewards = []

    extra_rewards_length = crv_rewards_contract.functions.extraRewardsLength().call(block_identifier=block)

    for i in range(extra_rewards_length):
        extra_reward_contract_address = crv_rewards_contract.functions.extraRewards(i).call(block_identifier=block)
        extra_reward_contract = get_contract(extra_reward_contract_address, blockchain,
                                             web3=web3, abi=ABI_REWARDS, block=block)

        extra_reward_token_address = extra_reward_contract.functions.rewardToken().call()
        extra_reward = extra_reward_contract.functions.earned(wallet).call(block_identifier=block)

        extra_rewards.append([extra_reward_token_address, to_token_amount(extra_reward_token_address, extra_reward, blockchain, web3, decimals)])

    return extra_rewards


def get_cvx_mint_amount(web3, crv_earned, block, blockchain, decimals=True):
    """
    Output:
        Tuple: [cvx_token_address, minted_amount]
    """
    cvx_amount = 0

    cvx_contract = get_contract(CVX_ETH, blockchain, web3=web3, abi=ABI_CVX, block=block)

    cliff_size = cvx_contract.functions.reductionPerCliff().call(block_identifier=block)
    cliff_count = cvx_contract.functions.totalCliffs().call(block_identifier=block)
    max_supply = cvx_contract.functions.maxSupply().call(block_identifier=block)

    cvx_total_supply = cvx_contract.functions.totalSupply().call(block_identifier=block)

    current_cliff = cvx_total_supply / cliff_size

    if (current_cliff < cliff_count):

        remaining = cliff_count - current_cliff
        cvx_amount = crv_earned * Decimal(remaining / cliff_count)
        amount_till_max = max_supply - cvx_total_supply

        if (cvx_amount > amount_till_max):
            cvx_amount = amount_till_max

    return [CVX_ETH, cvx_amount]


def get_all_rewards(wallet, lptoken_address, block, blockchain,
                    web3=None, decimals=True, crv_rewards_contract=None):
    """
    Output:
        List of Tuples: [reward_token_address, balance]
    """
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if crv_rewards_contract is None:
        pool_info = get_pool_info(lptoken_address, block)

        if pool_info is None:
            print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
            return None

        crv_rewards_address = pool_info[3]
        crv_rewards_contract = get_contract(crv_rewards_address, blockchain,
                                            web3=web3, abi=ABI_REWARDS,
                                            block=block)

    crv_rewards = get_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals=decimals)
    all_rewards.append(crv_rewards)

    # all_rewards[0][1] = crv_rewards_amount - cvx_mint_amount is calculated using the crv_rewards_amount
    if all_rewards[0][1] >= 0:
        cvx_mint_amount = get_cvx_mint_amount(web3, all_rewards[0][1], block, blockchain, decimals=decimals)

        if (len(cvx_mint_amount) > 0):
            all_rewards.append(cvx_mint_amount)

    extra_rewards = get_extra_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals=decimals)

    if len(extra_rewards) > 0:
        for extra_reward in extra_rewards:
            all_rewards.append(extra_reward)

    return all_rewards


def get_locked(wallet, block, blockchain, web3=None,
               reward=False, decimals=True):
    """
    Output:
    1 - List of Tuples: [cvx_token_address, locked_balance]
    2 - List of Tuples: [reward_token_address, balance]
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    cvx_locker_contract = get_contract(CVX_LOCKER, blockchain, web3=web3, block=block)
    cvx_locker = cvx_locker_contract.functions.balances(wallet).call(block_identifier=block)[0]

    result = [[CVX_ETH, to_token_amount(CVX_ETH, cvx_locker, blockchain, web3, decimals)]]

    if reward:
        rewards = []
        cvx_locker_rewards = cvx_locker_contract.functions.claimableRewards(wallet).call(block_identifier=block)

        for cvx_locker_reward in cvx_locker_rewards:
            if cvx_locker_reward[1] > 0:
                rewards.append([cvx_locker_reward[0], to_token_amount(cvx_locker_contract[0], cvx_locker_reward[1], blockchain, web3, decimals)])

        result += rewards

    return result


def get_staked(wallet, block, blockchain, web3=None,
               reward=False, decimals=True):
    """
    Output:
    1 - List of Tuples: [cvx_token_address, staked_balance]
    2 - List of Tuples: [reward_token_address, balance]
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    cvx_staking_contract = get_contract(CVX_STAKER, blockchain, web3=web3, block=block)
    cvx_staked = cvx_staking_contract.functions.balanceOf(wallet).call(block_identifier=block)

    result = [[CVX_ETH, to_token_amount(CVX_ETH, cvx_staked, blockchain, web3, decimals)]]

    if reward:
        rewards = []
        cvx_staked_rewards = cvx_staking_contract.functions.earned(wallet).call(block_identifier=block)

        if cvx_staked_rewards > 0:
            rewards.append([CVXCRV_ETH, to_token_amount(CVXCRV_ETH, cvx_staked_rewards, blockchain, web3, decimals)])

        result += rewards

    return result


def underlying(wallet, lptoken_address, block, blockchain, web3=None,
               reward=False, decimals=True, no_curve_underlying=False):
    """
    'no_curve_underlying' = True -> retrieves the LP Token balance /
    'no_curve_underlying' = False or not passed onto the function -> retrieves the balance of the underlying Curve tokens
    Output: a list with 2 elements:
    1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_curve_underlying' value
    2 - List of Tuples: [reward_token_address, balance]
    """

    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    pool_info = get_pool_info(lptoken_address, block)

    if pool_info is None:
        print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
        return None

    crv_rewards_address = pool_info[3]
    crv_rewards_contract = get_contract(crv_rewards_address, blockchain, web3=web3, abi=ABI_REWARDS, block=block)

    lptoken_staked = crv_rewards_contract.functions.balanceOf(wallet).call(block_identifier=block)

    if no_curve_underlying is False:
        balances = Curve.underlying(wallet, lptoken_address, block, blockchain,
                                    web3=web3, decimals=decimals,
                                    convex_staked=lptoken_staked)
    else:
        balances.append([lptoken_address, to_token_amount(lptoken_address, lptoken_staked, blockchain, web3, decimals)])

    result = balances
    if reward:
        all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain,
                                      web3=web3, decimals=decimals,
                                      crv_rewards_contract=crv_rewards_contract)
        result.extend(all_rewards)

    return result


def pool_balances(lptoken_address, block, blockchain, web3=None,
                  decimals=True):
    """
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    balances = Curve.pool_balances(lptoken_address, block, blockchain, web3=web3, decimals=decimals)

    return balances


def update_db(db_path=None, save_to=None):
    if db_path is None:
        db_path = get_db_filename("Convex")
    if save_to is None:
        save_to = db_path

    try:
        with open(db_path, 'r') as db_file:
            # Reading from json file
            db_data = json.load(db_file)
    # FIXME: use specific exception
    except:
        db_data = {
            'pools': {}
        }

    web3 = get_node(ETHEREUM)

    booster = get_contract(BOOSTER, ETHEREUM, web3=web3, abi=ABI_BOOSTER)
    db_pool_length = len(db_data['pools'])

    pools_delta = booster.functions.poolLength().call() - db_pool_length

    if pools_delta > 0:
        for i in range(pools_delta):
            pool_info = const_call(booster.functions.poolInfo(db_pool_length + i))
            db_data['pools'][pool_info[0]] = {
                'poolId': db_pool_length + i,
                'token': pool_info[1],
                'gauge': pool_info[2],
                'crvRewards': pool_info[3],
                'stash': pool_info[4],
                'shutdown': pool_info[5]
            }

    with open(save_to, 'w') as db_file:
        json.dump(db_data, db_file)
    return db_data
