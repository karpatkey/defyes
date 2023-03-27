import os
import json
from pathlib import Path

from defi_protocols.functions import get_node, get_decimals, get_contract, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, AURA_ETH, ETHEREUM
from defi_protocols import Balancer

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOSTER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster (Main Deposit Contract) Address
# BOOSTER = '0x7818A1DA7BD1E64c199029E86Ba244a9798eEE10' (Old Version)
BOOSTER = '0xA57b8d98dAE62B26Ec3bcC4a365338157060B234'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AURA LOCKER TOKEN ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AURA locker token address
AURA_LOCKER = '0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AURABAL REWARD CONTRACT ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# auraBAL Reward Contract Address
# AURABAL_REWARDER = '0x5e5ea2048475854a5702f5b8468a51ba1296efcc' (Old Version)
AURABAL_REWARDER = '0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# REWARD POOL DEPOSIT WRAPPER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Reward Pool Deposit Wrapper
REWARD_POOL_DEPOSIT_WRAPPER = '0xB188b1CB84Fb0bA13cb9ee1292769F903A9feC59'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXTRA REWARDS DISTRIBUTOR
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Extra Rewards Distributor
# Extra Rewards are from those that claimed the initial AURA airdrop to their wallet instead of locking it
EXTRA_REWARDS_DISTRIBUTOR = '0xA3739b206097317c72EF416F0E75BB8f58FbD308'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster ABI - poolInfo, poolLength
ABI_BOOSTER = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"address","name":"lptoken","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"gauge","type":"address"},{"internalType":"address","name":"crvRewards","type":"address"},{"internalType":"address","name":"stash","type":"address"},{"internalType":"bool","name":"shutdown","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# REWARDER ABI - balanceOf, earned, extraRewards, extraRewardsLength, rewardToken, rewards, stakingToken, totalSupply
ABI_REWARDER = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"rewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"stakingToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA ABI - EMISSIONS_MAX_SUPPLY, INIT_MINT_AMOUNT, decimals, reductionPerCliff, totalCliffs, totalSupply
ABI_AURA = '[{"inputs":[],"name":"EMISSIONS_MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"INIT_MINT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA LOCKER ABI - balances, claimableRewards
ABI_AURA_LOCKER = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint112","name":"locked","type":"uint112"},{"internalType":"uint32","name":"nextUnlockIndex","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"claimableRewards","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct AuraLocker.EarnedData[]","name":"userRewards","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'

# EXTRA REWARDS DISTRIBUTOR ABI - claimableRewards
ABI_EXTRA_REWARDS_DISTRIBUTOR = '[{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"address","name":"_token","type":"address"}],"name":"claimableRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info - Retrieves the result of the pool_info method if there is a match for the lptoken_address - Otherwise it returns None
# Output: pool_info method return a list with the following data:
# [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(booster_contract, lptoken_address, block):
    """

    :param booster_contract:
    :param lptoken_address:
    :param block:
    :return:
    """
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Aura_db.json', 'r') as db_file:
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
def get_extra_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param rewarder_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    extra_rewards = []

    extra_rewards_length = rewarder_contract.functions.extraRewardsLength().call(block_identifier=block)

    for i in range(extra_rewards_length):

        extra_reward_contract_address = rewarder_contract.functions.extraRewards(i).call(block_identifier=block)
        extra_reward_contract = get_contract(extra_reward_contract_address, blockchain, web3=web3, abi=ABI_REWARDER,
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
# get_extra_rewards_airdrop
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_extra_rewards_airdrop(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
    :param index:
    :param decimals:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    extra_rewards_airdrop = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        extra_rewards_distributor = get_contract(EXTRA_REWARDS_DISTRIBUTOR, blockchain, web3=web3,
                                                 abi=ABI_EXTRA_REWARDS_DISTRIBUTOR, block=block)

        extra_reward = extra_rewards_distributor.functions.claimableRewards(wallet, AURA_ETH).call(
            block_identifier=block)

        if extra_reward > 0:
            if decimals is True:
                extra_reward_token_decimals = get_decimals(AURA_ETH, blockchain, web3=web3)
            else:
                extra_reward_token_decimals = 0

            extra_reward = extra_reward / (10 ** extra_reward_token_decimals)

            extra_rewards_airdrop = [AURA_ETH, extra_reward]

        return extra_rewards_airdrop

    except GetNodeIndexError:
        return get_extra_rewards_airdrop(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_extra_rewards_airdrop(wallet, block, blockchain, decimals=decimals, index=index + 1,
                                         execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_aura_mint_amount
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [aura_token_address, minted_amount]
# WARNING: Check the amount of AURA retrieved
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_aura_mint_amount(web3, bal_earned, block, blockchain, decimals=True):
    """

    :param web3:
    :param bal_earned:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    aura_amount = 0

    aura_contract = get_contract(AURA_ETH, blockchain, web3=web3, abi=ABI_AURA, block=block)

    aura_total_supply = aura_contract.functions.totalSupply().call(block_identifier=block)
    init_mint_amount = aura_contract.functions.INIT_MINT_AMOUNT().call(block_identifier=block)
    reduction_per_cliff = aura_contract.functions.reductionPerCliff().call(block_identifier=block)

    emissions_minted = aura_total_supply - init_mint_amount
    cliff = emissions_minted / reduction_per_cliff

    total_cliffs = aura_contract.functions.totalCliffs().call(block_identifier=block)

    if cliff < total_cliffs:

        reduction = ((total_cliffs - cliff) * 2.5) + 700

        aura_amount = (bal_earned * reduction) / total_cliffs

        amount_till_max = aura_contract.functions.EMISSIONS_MAX_SUPPLY().call(block_identifier=block) - emissions_minted

        if aura_amount > amount_till_max:
            aura_amount = amount_till_max

    if decimals is False:
        aura_decimals = get_decimals(AURA_ETH, blockchain, web3=web3)
        aura_amount = aura_amount * (10 ** aura_decimals)

    return [AURA_ETH, aura_amount]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'bal_rewards_contract' = bal_rewards_contract -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, execution=1, web3=None, index=0, decimals=True,
                    bal_rewards_contract=None):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
    :param index:
    :param decimals:
    :param bal_rewards_contract:
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

        if bal_rewards_contract is None:
            booster_contract = get_contract(BOOSTER, blockchain, web3=web3, abi=ABI_BOOSTER, block=block)
            pool_info = get_pool_info(booster_contract, lptoken_address, block)

            if pool_info is None:
                print('Error: Incorrect Convex LPToken Address: ', lptoken_address)
                return None

            bal_rewards_address = pool_info[3]
            bal_rewards_contract = get_contract(bal_rewards_address, blockchain, web3=web3, abi=ABI_REWARDER,
                                                block=block)

        bal_rewards = get_rewards(web3, bal_rewards_contract, wallet, block, blockchain, decimals=decimals)
        all_rewards.append(bal_rewards)

        # all_rewards[0][1] = bal_rewards_amount - aura_mint_amount is calculated using the bal_rewards_amount
        if all_rewards[0][1] >= 0:
            aura_mint_amount = get_aura_mint_amount(web3, all_rewards[0][1], block, blockchain, decimals=decimals)

            if (len(aura_mint_amount) > 0):
                all_rewards.append(aura_mint_amount)

        extra_rewards = get_extra_rewards(web3, bal_rewards_contract, wallet, block, blockchain, decimals=decimals)

        if len(extra_rewards) > 0:
            for extra_reward in extra_rewards:
                if extra_reward[0] in [reward[0] for reward in all_rewards]:
                    index = [reward[0] for reward in all_rewards].index(extra_reward[0])
                    all_rewards[index][1] += extra_reward[1]
                else:
                    all_rewards.append(extra_reward)

        return all_rewards


    except GetNodeIndexError:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals=decimals,
                               bal_rewards_contract=bal_rewards_contract, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, decimals=decimals,
                               bal_rewards_contract=bal_rewards_contract, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_locked
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [aura_token_address, locked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_locked(wallet, block, blockchain, execution=1, web3=None, index=0, reward=False, decimals=True):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
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

        aura_locker_contract = get_contract(AURA_LOCKER, blockchain, web3=web3, abi=ABI_AURA_LOCKER, block=block)

        if decimals is True:
            aura_decimals = get_decimals(AURA_ETH, blockchain, web3=web3)
        else:
            aura_decimals = 0

        aura_locker = aura_locker_contract.functions.balances(wallet).call(block_identifier=block)[0] / (
                    10 ** aura_decimals)

        result = [[AURA_ETH, aura_locker]]

        if reward is True:
            rewards = []
            aura_locker_rewards = aura_locker_contract.functions.claimableRewards(wallet).call(block_identifier=block)

            for aura_locker_reward in aura_locker_rewards:

                if aura_locker_reward[1] > 0:

                    if decimals is True:
                        reward_decimals = get_decimals(aura_locker_reward[0], blockchain, web3=web3)
                    else:
                        reward_decimals = 0

                    rewards.append([aura_locker_reward[0], aura_locker_reward[1] / (10 ** reward_decimals)])

            result += rewards

        return result

    except GetNodeIndexError:
        return get_locked(wallet, block, blockchain, reward=reward, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_locked(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staked_aurabal
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [aurabal_token_address, staked_balance]
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

        aurabal_rewarder_contract = get_contract(AURABAL_REWARDER, blockchain, web3=web3, abi=ABI_REWARDER, block=block)

        if decimals is True:
            aurabal_address = aurabal_rewarder_contract.functions.stakingToken().call()
            aurabal_decimals = get_decimals(aurabal_address, blockchain, web3=web3)
        else:
            aurabal_decimals = 0

        aurabal_staked = aurabal_rewarder_contract.functions.balanceOf(wallet).call(block_identifier=block) / (
                    10 ** aurabal_decimals)

        result = [[aurabal_address, aurabal_staked]]

        if reward is True:
            rewards = []

            # BAL Rewards
            rewards.append(get_rewards(web3, aurabal_rewarder_contract, wallet, block, blockchain, decimals=decimals))

            # Extra Rewards
            extra_rewards = get_extra_rewards(web3, aurabal_rewarder_contract, wallet, block, blockchain,
                                              decimals=decimals)
            for n in range(0, len(extra_rewards)):
                rewards.append(extra_rewards[n])

            # AURA Rewards
            if rewards[0][1] > 0:
                rewards.append(get_aura_mint_amount(web3, rewards[0][1], block, blockchain, decimals=decimals))

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
# 'no_balancer_underlying' = True -> retrieves the LP Token balance /
# 'no_balancer_underlying' = False or not passed onto the function -> retrieves the balance of the underlying Balancer tokens
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_balancer_underlying' value
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False,
               no_balancer_underlying=False, decimals=True):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param reward:
    :param no_balancer_underlying:
    :param decimals:
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

        booster_contract = get_contract(BOOSTER, blockchain, web3=web3, abi=ABI_BOOSTER, block=block)

        pool_info = get_pool_info(booster_contract, lptoken_address, block)

        if pool_info is None:
            print('Error: Incorrect Aura LPToken Address: ', lptoken_address)
            return None

        bal_rewards_address = pool_info[3]
        bal_rewards_contract = get_contract(bal_rewards_address, blockchain, web3=web3, abi=ABI_REWARDER, block=block)

        lptoken_staked = bal_rewards_contract.functions.balanceOf(wallet).call(block_identifier=block)

        if no_balancer_underlying is False:
            balancer_data = Balancer.underlying(wallet, lptoken_address, block, blockchain, web3=web3,
                                                decimals=decimals, aura_staked=lptoken_staked)
            balances = [[balancer_data[i][0], balancer_data[i][2]] for i in range(len(balancer_data))]
        else:
            if decimals is True:
                lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
            else:
                lptoken_decimals = 0

            lptoken_staked = lptoken_staked / (10 ** lptoken_decimals)

            balances.append([lptoken_address, lptoken_staked])

        if reward is True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                          bal_rewards_contract=bal_rewards_contract)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying(wallet, lptoken_address, block, blockchain, reward=reward, decimals=decimals,
                          no_balancer_underlying=no_balancer_underlying, index=0, execution=execution + 1)

    except:
        return underlying(wallet, lptoken_address, block, blockchain, reward=reward, decimals=decimals,
                          no_balancer_underlying=no_balancer_underlying, index=index + 1, execution=execution)


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

        balances = Balancer.pool_balances(lptoken_address, block, blockchain, web3=web3, decimals=decimals)

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
        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Aura_db.json', 'r') as db_file:
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

        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Aura_db.json', 'w') as db_file:
            json.dump(db_data, db_file)
