import json
from decimal import Decimal
from pathlib import Path
from web3 import Web3

from defi_protocols.functions import get_node, get_decimals, get_contract, to_token_amount
from defi_protocols.constants import AURA_ETH, ETHEREUM
from defi_protocols import Balancer

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOSTER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster (Main Deposit Contract) Address
# BOOSTER = '0x7818A1DA7BD1E64c199029E86Ba244a9798eEE10' (Old Version)
BOOSTER = '0xA57b8d98dAE62B26Ec3bcC4a365338157060B234'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STAKED Aura BAL
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
stkauraBAL = '0xfAA2eD111B4F580fCb85C48E6DC6782Dc5FCD7a6'

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

# stkauraBAL ABI - balanceOfUnderlying, underlying, extraRewards, extraRewardsLength
ABI_STKAURABAL = '[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"balanceOfUnderlying","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"underlying","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA ABI - EMISSIONS_MAX_SUPPLY, INIT_MINT_AMOUNT, decimals, reductionPerCliff, totalCliffs, totalSupply
ABI_AURA = '[{"inputs":[],"name":"EMISSIONS_MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"INIT_MINT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA LOCKER ABI - balances, claimableRewards
ABI_AURA_LOCKER = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint112","name":"locked","type":"uint112"},{"internalType":"uint32","name":"nextUnlockIndex","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"claimableRewards","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct AuraLocker.EarnedData[]","name":"userRewards","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'

# EXTRA REWARDS DISTRIBUTOR ABI - claimableRewards
ABI_EXTRA_REWARDS_DISTRIBUTOR = '[{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"address","name":"_token","type":"address"}],"name":"claimableRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


# DB
# Format
# { balancerLPcontractAddr: {
#     "poolId": poolId,
#     "token": auraLPtoken,
#     "gauge": balancerLPGauge,
#     "crvRewards": auraBaseRewardPool,
#     "stash": auraExtraRewardStash,
#     "shutdown": bool  # deprecated pool
#     },
# }
DB_FILE = Path(__file__).parent / "db" / "Aura_db.json"


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info - Retrieves the result of the pool_info method if there is a match for the lptoken_address - Otherwise it returns None
# [0] lptoken address, [1] token address, [2] gauge address, [3] crvRewards address, [4] stash adress, [5] shutdown bool
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(booster_contract, lptoken_address, block):

    with open(DB_FILE, 'r') as db_file:
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
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):

    reward_token_address = rewarder_contract.functions.rewardToken().call()
    bal_rewards = rewarder_contract.functions.earned(wallet).call(block_identifier=block)

    return [reward_token_address, to_token_amount(reward_token_address, bal_rewards, blockchain, web3, decimals)]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_extra_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_extra_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):

    extra_rewards = []

    extra_rewards_length = rewarder_contract.functions.extraRewardsLength().call(block_identifier=block)
    for n in range(extra_rewards_length):

        extra_reward_contract_address = rewarder_contract.functions.extraRewards(n).call(block_identifier=block)
        extra_reward_contract = get_contract(extra_reward_contract_address, blockchain, web3=web3, abi=ABI_REWARDER,
                                             block=block)

        extra_reward_token_address = extra_reward_contract.functions.rewardToken().call()
        extra_reward = extra_reward_contract.functions.earned(wallet).call(block_identifier=block)

        extra_rewards.append([extra_reward_token_address, to_token_amount(extra_reward_token_address, extra_reward, blockchain, web3, decimals)])

    return extra_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_extra_rewards_airdrop
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_extra_rewards_airdrop(wallet, block, blockchain, web3=None, decimals=True):

    extra_rewards_airdrop = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    extra_rewards_distributor = get_contract(EXTRA_REWARDS_DISTRIBUTOR, blockchain, web3=web3,
                                             abi=ABI_EXTRA_REWARDS_DISTRIBUTOR, block=block)

    extra_reward = extra_rewards_distributor.functions.claimableRewards(wallet, AURA_ETH).call(
        block_identifier=block)

    if extra_reward > 0:
        extra_rewards_airdrop = [AURA_ETH, to_token_amount(AURA_ETH, extra_reward, blockchain, web3, decimals)]

    return extra_rewards_airdrop


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_aura_mint_amount
# WARNING: Check the amount of AURA retrieved
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_aura_mint_amount(web3, bal_earned, block, blockchain, decimals=True):

    aura_amount = 0

    aura_contract = get_contract(AURA_ETH, blockchain, web3=web3, abi=ABI_AURA, block=block)

    aura_total_supply = aura_contract.functions.totalSupply().call(block_identifier=block)
    init_mint_amount = aura_contract.functions.INIT_MINT_AMOUNT().call(block_identifier=block)
    reduction_per_cliff = aura_contract.functions.reductionPerCliff().call(block_identifier=block)

    emissions_minted = aura_total_supply - init_mint_amount
    cliff = emissions_minted / Decimal(reduction_per_cliff)

    total_cliffs = aura_contract.functions.totalCliffs().call(block_identifier=block)

    if cliff < total_cliffs:

        reduction = ((total_cliffs - cliff) * Decimal(2.5)) + 700

        aura_amount = (bal_earned * reduction) / total_cliffs

        amount_till_max = Decimal(aura_contract.functions.EMISSIONS_MAX_SUPPLY().call(block_identifier=block)) - emissions_minted

        if aura_amount > amount_till_max:
            aura_amount = amount_till_max

    if not decimals:
        aura_decimals = get_decimals(AURA_ETH, blockchain, web3=web3)
        aura_amount = aura_amount * Decimal(10 ** aura_decimals)

    return [AURA_ETH, aura_amount]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, bal_rewards_contract=None):

    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

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

        if len(aura_mint_amount) > 0:
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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_locked
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_locked(wallet, block, blockchain, web3=None, reward=False, decimals=True):
 
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    aura_locker_contract = get_contract(AURA_LOCKER, blockchain, web3=web3, abi=ABI_AURA_LOCKER, block=block)

    aura_locker = aura_locker_contract.functions.balances(wallet).call(block_identifier=block)[0]

    result = [[AURA_ETH, to_token_amount(AURA_ETH, aura_locker, blockchain, web3, decimals)]]

    if reward is True:
        rewards = []
        aura_locker_rewards = aura_locker_contract.functions.claimableRewards(wallet).call(block_identifier=block)
        if aura_locker_rewards:
            for token, balance in aura_locker_rewards:
                rewards.append([token, to_token_amount(token, balance, blockchain, web3, decimals)])

        result += rewards

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staked_aurabal
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staked(wallet, block, blockchain, web3=None, reward=False, decimals=True):

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    aurabal_rewarder_contract = get_contract(AURABAL_REWARDER, blockchain, web3=web3, abi=ABI_REWARDER, block=block)
    aurabal_address = aurabal_rewarder_contract.functions.stakingToken().call()
    aurabal_staked = aurabal_rewarder_contract.functions.balanceOf(wallet).call(block_identifier=block)

    result = [[aurabal_address, to_token_amount(aurabal_address, aurabal_staked, blockchain, web3, decimals)]]

    if reward is True:
        rewards = [get_rewards(web3, aurabal_rewarder_contract, wallet, block, blockchain, decimals=decimals)]

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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_compounded_aurabal
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_compounded(wallet, block, blockchain, web3=None, reward=False, decimals=True):

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    stk_aurabal_contract = get_contract(stkauraBAL, blockchain, web3=web3, abi=ABI_STKAURABAL, block=block)
    aurabal_address = stk_aurabal_contract.functions.underlying().call()
    aurabal_staked = stk_aurabal_contract.functions.balanceOfUnderlying(wallet).call(block_identifier=block)

    result = [[aurabal_address, to_token_amount(aurabal_address, aurabal_staked, blockchain, web3, decimals)]]

    if reward is True:
        rewards = []
        # Extra Rewards
        extra_rewards = get_extra_rewards(web3, stk_aurabal_contract, wallet, block, blockchain, decimals=decimals)
        for n in range(0, len(extra_rewards)):
            rewards.append(extra_rewards[n])
        
        result += rewards

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, reward=False, no_balancer_underlying=False, decimals=True):

    result = []
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    booster_contract = get_contract(BOOSTER, blockchain, web3=web3, abi=ABI_BOOSTER, block=block)

    pool_info = get_pool_info(booster_contract, lptoken_address, block)

    if pool_info:
        bal_rewards_address = pool_info[3]
        bal_rewards_contract = get_contract(bal_rewards_address, blockchain, web3=web3, abi=ABI_REWARDER, block=block)
        lptoken_staked = bal_rewards_contract.functions.balanceOf(wallet).call(block_identifier=block)

        if no_balancer_underlying is False:
            balancer_data = Balancer.underlying(wallet, lptoken_address, block, blockchain, web3=web3,
                                                decimals=decimals, aura_staked=lptoken_staked)
            balances = [[balancer_data[i][0], balancer_data[i][2]] for i in range(len(balancer_data))]
        else:
            balances.append([lptoken_address, to_token_amount(lptoken_address, lptoken_staked, blockchain, web3, decimals)])

        if reward is True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                          bal_rewards_contract=bal_rewards_contract)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    balances = Balancer.pool_balances(lptoken_address, block, blockchain, web3=web3, decimals=decimals)

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_db
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db(output_file=DB_FILE):

    try:
        with open(DB_FILE, 'r') as db_file:
            db_data = json.load(db_file)
    except:
        db_data = {
            'pools': {}
        }

    web3 = get_node(ETHEREUM)

    booster = get_contract(BOOSTER, ETHEREUM, web3=web3, abi=ABI_BOOSTER)
    db_pool_length = len(db_data['pools'])
    pools_delta = booster.functions.poolLength().call() - db_pool_length

    updated = False
    if pools_delta > 0:
        updated = True
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

        with open(output_file, 'w') as db_file:
            json.dump(db_data, db_file)

    return updated
