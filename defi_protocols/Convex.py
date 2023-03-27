import json
import os
from pathlib import Path

from defi_protocols.functions import get_node, get_contract, get_decimals, GetNodeIndexError
from defi_protocols.constants import ETHEREUM, MAX_EXECUTIONS, CVX_ETH, CVXCRV_ETH
from defi_protocols import Curve

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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info - Retrieves the result of the pool_info method if there is a match for the lptoken_address - Otherwise it returns None
# Output: pool_info method return a list with the following data:
# [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(lptoken_address, block):
    """

    :param lptoken_address:
    :param block:
    :return:
    """
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Convex_db.json', 'r') as db_file:
        # Reading from json file
        db_data = json.load(db_file)

    try:
        pool_info = db_data['pools'][lptoken_address]

        if pool_info['shutdown'] is False:
            pool_info = [lptoken_address, pool_info['token'], pool_info['gauge'], pool_info['crvRewards'],
                         pool_info['stash'], pool_info['shutdown']]

            return pool_info
        else:
            return None

    except:
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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuples: [token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param rewarder_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    reward_token_address = rewarder_contract.functions.rewardToken().call()

    if decimals is True:
        reward_token_decimals = get_decimals(reward_token_address, blockchain, web3=web3)
    else:
        reward_token_decimals = 0

    bal_rewards = rewarder_contract.functions.earned(wallet).call(block_identifier=block) / (
                10 ** reward_token_decimals)

    return [reward_token_address, bal_rewards]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_extra_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_extra_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param crv_rewards_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    extra_rewards = []

    extra_rewards_length = crv_rewards_contract.functions.extraRewardsLength().call(block_identifier=block)

    for i in range(extra_rewards_length):
        extra_reward_contract_address = crv_rewards_contract.functions.extraRewards(i).call(block_identifier=block)
        extra_reward_contract = get_contract(extra_reward_contract_address, blockchain, web3=web3, abi=ABI_REWARDS,
                                             block=block)

        extra_reward_token_address = extra_reward_contract.functions.rewardToken().call()

        if decimals is True:
            extra_reward_token_decimals = get_decimals(extra_reward_token_address, blockchain, web3=web3)
        else:
            extra_reward_token_decimals = 0

        extra_reward = extra_reward_contract.functions.earned(wallet).call(block_identifier=block) / (
                    10 ** extra_reward_token_decimals)

        extra_rewards.append([extra_reward_token_address, extra_reward])

    return extra_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cvx_mint_amount
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [cvx_token_address, minted_amount]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cvx_mint_amount(web3, crv_earned, block, blockchain, decimals=True):
    """

    :param web3:
    :param crv_earned:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
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
        cvx_amount = crv_earned * remaining / cliff_count
        amount_till_max = max_supply - cvx_total_supply

        if (cvx_amount > amount_till_max):
            cvx_amount = amount_till_max

    if decimals is False:
        cvx_decimals = get_decimals(CVX_ETH, blockchain, web3=web3)
        cvx_amount = cvx_amount * (10 ** cvx_decimals)

    return [CVX_ETH, cvx_amount]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'crv_rewards_contract' = crv_rewards_contract -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True,
                    crv_rewards_contract=None):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param crv_rewards_contract:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    all_rewards = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        if crv_rewards_contract is None:
            pool_info = get_pool_info(lptoken_address, block)

            if pool_info is None:
                print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
                return None

            crv_rewards_address = pool_info[3]
            crv_rewards_contract = get_contract(crv_rewards_address, blockchain, web3=web3, abi=ABI_REWARDS,
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

    except GetNodeIndexError:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, crv_rewards_contract=crv_rewards_contract,
                               decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, crv_rewards_contract=crv_rewards_contract,
                               decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cvx_locked
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [cvx_token_address, locked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_locked(wallet, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param reward:
    :param decimals:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        cvx_locker_contract = get_contract(CVX_LOCKER, blockchain, web3=web3, block=block)

        if decimals is True:
            cvx_decimals = get_decimals(CVX_ETH, blockchain, web3=web3)
        else:
            cvx_decimals = 0

        cvx_locker = cvx_locker_contract.functions.balances(wallet).call(block_identifier=block)[0] / (
                    10 ** cvx_decimals)

        result = [[CVX_ETH, cvx_locker]]

        if reward is True:
            rewards = []
            cvx_locker_rewards = cvx_locker_contract.functions.claimableRewards(wallet).call(block_identifier=block)

            for cvx_locker_reward in cvx_locker_rewards:

                if cvx_locker_reward[1] > 0:

                    if decimals is True:
                        reward_decimals = get_decimals(cvx_locker_reward[0], blockchain, web3=web3)
                    else:
                        reward_decimals = 0

                    rewards.append([cvx_locker_reward[0], cvx_locker_reward[1] / (10 ** reward_decimals)])

            result += rewards

        return result

    except GetNodeIndexError:
        return get_locked(wallet, block, blockchain, reward=reward, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_locked(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staked
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [cvx_token_address, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staked(wallet, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param reward:
    :param decimals:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        cvx_staking_contract = get_contract(CVX_STAKER, blockchain, web3=web3, block=block)

        if decimals is True:
            cvx_decimals = get_decimals(CVX_ETH, blockchain, web3=web3)
        else:
            cvx_decimals = 0

        cvx_staked = cvx_staking_contract.functions.balanceOf(wallet).call(block_identifier=block) / (
                    10 ** cvx_decimals)

        result = [[CVX_ETH, cvx_staked]]

        if reward is True:
            rewards = []
            cvx_staked_rewards = cvx_staking_contract.functions.earned(wallet).call(block_identifier=block)

            if cvx_staked_rewards > 0:

                if decimals is True:

                    reward_decimals = get_decimals(CVXCRV_ETH, blockchain, web3=web3)

                else:
                    reward_decimals = 0

            rewards.append([CVXCRV_ETH, cvx_staked_rewards / (10 ** reward_decimals)])

            result += rewards

        return result

    except GetNodeIndexError:
        return get_staked(wallet, block, blockchain, reward=reward, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_staked(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'no_curve_underlying' = True -> retrieves the LP Token balance /
# 'no_curve_underlying' = False or not passed onto the function -> retrieves the balance of the underlying Curve tokens
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_curve_underlying' value
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True,
               no_curve_underlying=False):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param reward:
    :param decimals:
    :param no_curve_underlying:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    result = []
    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        pool_info = get_pool_info(lptoken_address, block)

        if pool_info is None:
            print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
            return None

        crv_rewards_address = pool_info[3]
        crv_rewards_contract = get_contract(crv_rewards_address, blockchain, web3=web3, abi=ABI_REWARDS, block=block)

        lptoken_staked = crv_rewards_contract.functions.balanceOf(wallet).call(block_identifier=block)

        if no_curve_underlying is False:
            balances = Curve.underlying(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                        convex_staked=lptoken_staked)
        else:
            if decimals is True:
                lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
            else:
                lptoken_decimals = 0

            lptoken_staked = lptoken_staked / (10 ** lptoken_decimals)

            balances.append([lptoken_address, lptoken_staked])

        if reward is True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                          crv_rewards_contract=crv_rewards_contract)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying(wallet, lptoken_address, block, blockchain, reward=reward, decimals=decimals,
                          no_curve_underlying=no_curve_underlying, index=0, execution=execution + 1)

    except:
        return underlying(wallet, lptoken_address, block, blockchain, reward=reward, decimals=decimals,
                          no_curve_underlying=no_curve_underlying, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        balances = Curve.pool_balances(lptoken_address, block, blockchain, web3=web3, decimals=decimals)

        return balances

    except GetNodeIndexError:
        return pool_balances(lptoken_address, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return pool_balances(lptoken_address, block, blockchain, decimals=decimals, index=index + 1,
                             execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_db
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db():
    """

    :return:
    """
    try:
        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Convex_db.json', 'r') as db_file:
            # Reading from json file
            db_data = json.load(db_file)
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
            pool_info = booster.functions.poolInfo(db_pool_length + i).call()
            db_data['pools'][pool_info[0]] = {
                'poolId': db_pool_length + i,
                'token': pool_info[1],
                'gauge': pool_info[2],
                'crvRewards': pool_info[3],
                'stash': pool_info[4],
                'shutdown': pool_info[5]
            }

        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Convex_db.json', 'w') as db_file:
            json.dump(db_data, db_file)
