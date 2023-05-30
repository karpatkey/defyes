from decimal import Decimal
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defi_protocols.functions import get_node, get_contract, get_decimals, last_block, to_token_amount
from defi_protocols.constants import OPTIMISM, ZERO_ADDRESS
from defi_protocols.cache import const_call

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# UNITROLLER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Optimism - Unitroller Address
UNITROLLER_OPTIMISM = '0xE0B57FEEd45e7D908f2d0DaCd26F113Cf26715BF'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STAKING REWARDS FACTORY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Optimism - Staking Rewards Factory Address
STAKING_REWARDS_FACTORY_OPTIMISM = '0x35F70CE60f049A8c21721C53a1dFCcB5bF4a1Ea8'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veIB
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Optimism - veIB Address
VEIB_OPTIMISM = '0x707648dfbF9dF6b0898F78EdF191B85e327e0e05'

# Optimism - Fee Dist - To retrieve the claimable iUSDC for locking IB
FEE_DIST_OPTIMISM = '0xFdE79c1e8510eE19360B71f2561766Cf2C757Fc7'

# Optimism - ve Dist - To retrieve the claimable IB for locking IB
VE_DIST_OPTIMISM = '0x5402508a800dB6B72792b80623193E38839a9e24'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# iToken ABI - decimals, balanceOf, totalSupply, exchangeRateStored, underlying, borrowBalanceStored
ABI_ITOKEN = '[{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"exchangeRateStored","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"underlying","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"borrowBalanceStored","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Unitroller ABI - getAllMarkets
ABI_UNITROLLER = '[{"constant":true,"inputs":[],"name":"getAllMarkets","outputs":[{"internalType":"contract CToken[]","name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Staking Rewards Factory ABI - getAllStakingRewards, getStakingRewards, getStakingToken
ABI_STAKING_REWARDS_FACTORY = '[{"inputs":[],"name":"getAllStakingRewards","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"stakingToken","type":"address"}],"name":"getStakingRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"underlying","type":"address"}],"name":"getStakingToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# Staking Rewards Helper ABI - getUserClaimableRewards, getUserStaked
ABI_STAKING_REWARDS_HELPER = '[{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"address[]","name":"rewardTokens","type":"address[]"}],"name":"getUserClaimableRewards","outputs":[{"components":[{"components":[{"internalType":"address","name":"rewardTokenAddress","type":"address"},{"internalType":"string","name":"rewardTokenSymbol","type":"string"},{"internalType":"uint8","name":"rewardTokenDecimals","type":"uint8"}],"internalType":"struct StakingRewardsHelper.RewardTokenInfo","name":"rewardToken","type":"tuple"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct StakingRewardsHelper.RewardClaimable[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getUserStaked","outputs":[{"components":[{"internalType":"address","name":"stakingTokenAddress","type":"address"},{"internalType":"uint256","name":"balance","type":"uint256"}],"internalType":"struct StakingRewardsHelper.UserStaked[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'

# Staking Rewards ABI - earned, getAllRewardsTokens, helperContract
ABI_STAKING_REWARDS = '[{"inputs":[{"internalType":"address","name":"_rewardsToken","type":"address"},{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getAllRewardsTokens","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"helperContract","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# veIB ABI - balanceOfAtNFT, locked, token, decimals
ABI_VEIB = '[{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"},{"internalType":"uint256","name":"_block","type":"uint256"}],"name":"balanceOfAtNFT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"locked","outputs":[{"internalType":"int128","name":"amount","type":"int128"},{"internalType":"uint256","name":"end","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Fee Dist ABI - claimable, token
ABI_FEE_DIST = '[{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"claimable","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# ve Dist ABI - claimable, token
ABI_VE_DIST = '[{"inputs":[{"internalType":"uint256","name":"_tokenId","type":"uint256"}],"name":"claimable","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'


def call_contract_method(method, block):
    try:
        return method.call(block_identifier = block)
    except (ContractLogicError, BadFunctionCallOutput):
        return None


def get_comptoller_address(blockchain):
    if blockchain == OPTIMISM:
        return UNITROLLER_OPTIMISM


def get_staking_rewards_factory_address(blockchain):
    if blockchain == OPTIMISM:
        return STAKING_REWARDS_FACTORY_OPTIMISM


def get_veib_address(blockchain):
    if blockchain == OPTIMISM:
        return VEIB_OPTIMISM


def get_ve_dist_address(blockchain):
    if blockchain == OPTIMISM:
        return VE_DIST_OPTIMISM


def get_fee_dist_address(blockchain):
    if blockchain == OPTIMISM:
        return FEE_DIST_OPTIMISM


def get_itoken_data(itoken_address, wallet, block, blockchain, web3=None, underlying_token=None):

    if not web3:
        web3 = get_node(blockchain, block=block)

    itoken_data = {}

    itoken_data['contract'] = get_contract(itoken_address, blockchain, web3=web3, abi=ABI_ITOKEN, block=block)

    if underlying_token:
        itoken_data['underlying'] = underlying_token
    else:
        try:
            itoken_data['underlying'] = itoken_data['contract'].functions.underlying().call(block_identifier=block)
        except Exception as e:
            print(f'{e}')
            itoken_data['underlying'] = ZERO_ADDRESS

    itoken_data['decimals'] = const_call(itoken_data['contract'].functions.decimals())
    itoken_data['borrowBalanceStored'] = itoken_data['contract'].functions.borrowBalanceStored(wallet).call(
        block_identifier=block)
    itoken_data['balanceOf'] = itoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)
    itoken_data['exchangeRateStored'] = itoken_data['contract'].functions.exchangeRateStored().call(
        block_identifier=block)

    return itoken_data


def get_all_rewards(wallet, itoken, block, blockchain, web3=None, decimals=True,
                    staking_rewards_contract=None):

    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    if staking_rewards_contract is None:
        staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                        web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

        staking_rewards_address = staking_rewards_factory_contract.functions.getStakingRewards(itoken).call(block_identifier=block)
        staking_rewards_contract = get_contract(staking_rewards_address, blockchain, web3=web3,
                                                abi=ABI_STAKING_REWARDS, block=block)

    all_rewards_tokens = staking_rewards_contract.functions.getAllRewardsTokens().call()

    for reward_token in all_rewards_tokens:
        reward_earned = staking_rewards_contract.functions.earned(itoken, wallet).call(block_identifier=block)
        all_rewards.append([reward_token, to_token_amount(reward_token, reward_earned, blockchain, web3, decimals)])

    return all_rewards


def all_rewards(wallet, block, blockchain, web3=None, decimals=True):

    result = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                    web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

    staking_rewards_helper_address = ZERO_ADDRESS
    rewards_tokens = []

    all_staking_rewards = staking_rewards_factory_contract.functions.getAllStakingRewards().call()
    for staking_rewards in all_staking_rewards:
        staking_rewards_contract = get_contract(staking_rewards, blockchain, web3=web3, abi=ABI_STAKING_REWARDS,
                                                block=block)

        if staking_rewards_helper_address is ZERO_ADDRESS:
            staking_rewards_helper_address = const_call(staking_rewards_contract.functions.helperContract())

        all_rewards_tokens = staking_rewards_contract.functions.getAllRewardsTokens().call()
        for rewards_token in all_rewards_tokens:
            if rewards_token is not [] and rewards_token not in rewards_tokens:
                rewards_tokens.append(rewards_token)

    if staking_rewards_helper_address is not ZERO_ADDRESS and rewards_tokens is not []:
        staking_rewards_helper_contract = get_contract(staking_rewards_helper_address, blockchain, web3=web3,
                                                       abi=ABI_STAKING_REWARDS_HELPER, block=block)

        user_claimable_rewards = call_contract_method(staking_rewards_helper_contract.functions.getUserClaimableRewards(wallet,
                                                                    rewards_tokens), block)
        if user_claimable_rewards is None:
            for reward_token in rewards_tokens:
                result.append([reward_token, Decimal('0')])

            return result

        for user_claimable_reward in user_claimable_rewards:
            rew_decs = user_claimable_reward[0][2] if decimals else 0
            reward_amount = Decimal(user_claimable_reward[1]) / Decimal(10 ** rew_decs)
            result.append([user_claimable_reward[0][0], reward_amount])

    return result


def get_locked(wallet, block, blockchain, nft_id=302, web3=None, reward=False, decimals=True):

    if not web3:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    veib_address = get_veib_address(blockchain)
    veib_contract = get_contract(veib_address, blockchain, web3=web3, abi=ABI_VEIB, block=block)
    ib_token = const_call(veib_contract.functions.token())

    if block == 'latest':
        block = last_block(blockchain, web3=web3)

    veib_balance = call_contract_method(veib_contract.functions.balanceOfAtNFT(nft_id, block), block)
    locked_balance = call_contract_method(veib_contract.functions.locked(nft_id), block)

    balances = [[veib_address, to_token_amount(veib_address, veib_balance, blockchain, web3, decimals)],
                [ib_token, to_token_amount(ib_token, locked_balance[0], blockchain, web3, decimals)]]

    result = balances
    if reward:
        ve_dist_contract = get_contract(get_ve_dist_address(blockchain),
                                        blockchain,
                                        web3=web3,
                                        abi=ABI_VE_DIST,
                                        block=block)
        ve_dist_reward_token = const_call(ve_dist_contract.functions.token())
        ve_dist_claimable_reward = call_contract_method(ve_dist_contract.functions.claimable(nft_id), block)
        ve_dist_claimable_reward = ve_dist_claimable_reward if ve_dist_claimable_reward else Decimal(0)

        fee_dist_contract = get_contract(get_fee_dist_address(blockchain),
                                         blockchain,
                                         web3=web3,
                                         abi=ABI_VE_DIST,
                                         block=block)
        fee_dist_reward_token = fee_dist_contract.functions.token().call()
        fee_dist_claimable_reward = call_contract_method(fee_dist_contract.functions.claimable(nft_id), block)
        fee_dist_claimable_reward = fee_dist_claimable_reward if fee_dist_claimable_reward else Decimal(0)

        result.extend([[ve_dist_reward_token,
                        to_token_amount(ve_dist_reward_token, ve_dist_claimable_reward, blockchain, web3, decimals)],
                       [fee_dist_reward_token,
                        to_token_amount(fee_dist_reward_token, fee_dist_claimable_reward, blockchain, web3, decimals)]])

    return result


# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
def underlying(wallet, token_address, block, blockchain, web3=None, decimals=True, reward=False):

    if not web3:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    token_address = Web3.to_checksum_address(token_address)

    staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                    web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

    itoken = const_call(staking_rewards_factory_contract.functions.getStakingToken(token_address))

    if itoken == ZERO_ADDRESS:
        return []

    itoken_data = get_itoken_data(itoken, wallet, block, blockchain, web3=web3, underlying_token=token_address)

    underlying_token_decimals = get_decimals(token_address, block=block, blockchain=blockchain, web3=web3)
    mantissa = 18 - (itoken_data['decimals']) + underlying_token_decimals

    exchange_rate = Decimal(itoken_data['exchangeRateStored']) / Decimal(10 ** mantissa)

    underlying_token_balance = Decimal(itoken_data['balanceOf']) / Decimal(10 ** itoken_data['decimals']) * exchange_rate - \
                               Decimal(itoken_data['borrowBalanceStored']) / Decimal(10 ** underlying_token_decimals)

    if not decimals:
        underlying_token_balance = underlying_token_balance * Decimal(10 ** underlying_token_decimals)

    staking_rewards_address = const_call(staking_rewards_factory_contract.functions.getStakingRewards(itoken))
    staking_rewards_contract = get_contract(staking_rewards_address, blockchain, web3=web3, abi=ABI_STAKING_REWARDS,
                                            block=block)

    staking_rewards_helper_address = const_call(staking_rewards_contract.functions.helperContract())
    staking_rewards_helper_contract = get_contract(staking_rewards_helper_address, blockchain, web3=web3,
                                                   abi=ABI_STAKING_REWARDS_HELPER, block=block)
    user_staked = call_contract_method(staking_rewards_helper_contract.functions.getUserStaked(wallet), block)
    user_staked = user_staked if user_staked else []

    itoken_staked_balance = 0
    for itoken_staked_data in user_staked:
        if itoken_staked_data[0] == itoken:
            itoken_staked_balance = itoken_staked_data[1]
            break

    underlying_staked_balance = 0
    if itoken_staked_balance > 0:
        itoken_staked_balance = Decimal(itoken_staked_balance) / Decimal(10 ** get_decimals(itoken, blockchain, web3=web3))
        underlying_staked_balance = \
        unwrap(itoken_staked_balance, itoken, block, blockchain, web3=web3, decimals=decimals)[1]

    result = [[token_address, underlying_token_balance, underlying_staked_balance]]
    if reward:
        all_rewards = get_all_rewards(wallet, itoken, block, blockchain, web3=web3, decimals=decimals,
                                      staking_rewards_contract=staking_rewards_contract)
        result.extend(all_rewards)

    return result


# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
def underlying_all(wallet, block, blockchain, web3=None, decimals=True, reward=False):
    balances = []

    if not web3:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    unitroller_contract = get_contract(get_comptoller_address(blockchain), blockchain, web3=web3,
                                       abi=ABI_UNITROLLER, block=block)

    staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                    web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

    user_staked = []
    all_markets = unitroller_contract.functions.getAllMarkets().call()
    for itoken in all_markets:

        itoken_data = get_itoken_data(itoken, wallet, block, blockchain, web3=web3)

        underlying_token = itoken_data['underlying']

        underlying_token_balance = 0
        if itoken_data['balanceOf'] > 0 or itoken_data['borrowBalanceStored'] > 0:

            if underlying_token is not ZERO_ADDRESS:

                underlying_token_decimals = get_decimals(underlying_token, block=block, blockchain=blockchain,
                                                         web3=web3)

                mantissa = 18 - (itoken_data['decimals']) + underlying_token_decimals

                exchange_rate = Decimal(itoken_data['exchangeRateStored']) / Decimal(10 ** mantissa)

                underlying_token_balance = Decimal(itoken_data['balanceOf']) / \
                                           Decimal(10 ** itoken_data['decimals']) * exchange_rate - \
                                           Decimal(itoken_data['borrowBalanceStored']) / Decimal(10 ** underlying_token_decimals)

                if not decimals:
                    underlying_token_balance = underlying_token_balance * Decimal(10 ** underlying_token_decimals)

        if user_staked == []:
            staking_rewards_address = const_call(staking_rewards_factory_contract.functions.getStakingRewards(itoken))
            staking_rewards_contract = get_contract(staking_rewards_address, blockchain, web3=web3,
                                                    abi=ABI_STAKING_REWARDS, block=block)

            staking_rewards_helper_address = const_call(staking_rewards_contract.functions.helperContract())
            staking_rewards_helper_contract = get_contract(staking_rewards_helper_address, blockchain, web3=web3,
                                                           abi=ABI_STAKING_REWARDS_HELPER, block=block)
            user_staked = call_contract_method(staking_rewards_helper_contract.functions.getUserStaked(wallet), block)
            user_staked = user_staked if user_staked else []

        itoken_staked_balance = 0
        for itoken_staked_data in user_staked:
            if itoken_staked_data[0] == itoken:
                itoken_staked_balance = itoken_staked_data[1]
                break

        underlying_staked_balance = 0
        if itoken_staked_balance > 0:
            itoken_staked_balance = Decimal(itoken_staked_balance) / Decimal(10 ** get_decimals(itoken, blockchain, web3=web3))
            underlying_staked_balance = \
            unwrap(itoken_staked_balance, itoken, block, blockchain, web3=web3, decimals=decimals)[1]

        if underlying_token_balance != 0 or underlying_staked_balance > 0:
            balances.append([underlying_token, underlying_token_balance, underlying_staked_balance])

    result = balances
    if reward:
        rewards = all_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)

        result.extend(rewards)

    return result


# 1 - List of Tuples: [liquidity_token_address, balance]
def unwrap(itoken_amount, itoken_address, block, blockchain, web3=None, decimals=True):

    if not web3:
        web3 = get_node(blockchain, block=block)

    itoken_contract = get_contract(itoken_address, blockchain, abi=ABI_ITOKEN, web3=web3, block=block)
    itoken_decimals = const_call(itoken_contract.functions.decimals())
    exchange_rate = itoken_contract.functions.exchangeRateStored().call(block_identifier=block)

    underlying_token = itoken_contract.functions.underlying().call()
    underlying_token_decimals = get_decimals(underlying_token, blockchain, web3=web3) if decimals else 0

    underlying_token_balance = itoken_amount * Decimal(exchange_rate) / Decimal(10 ** (18 - itoken_decimals + underlying_token_decimals))

    return [underlying_token, underlying_token_balance]



# print(underlying_all('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', 'latest', OPTIMISM, reward=True))
# print(underlying_all('0x1a4c5e704b65b3406e5432ea2a1136461a60b174', 'latest', OPTIMISM, reward=True))
# print(underlying('0x1a4c5e704b65b3406e5432ea2a1136461a60b174', '0x4200000000000000000000000000000000000042', 'latest', OPTIMISM, reward=True))

# print(underlying('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', '0x7F5c764cBc14f9669B88837ca1490cCa17c31607', 'latest', OPTIMISM, reward=True))
# 0xE173cC94d4755b72eB9196Cf50DbcD2Cba54e348

# print(unwrap(198489.26169641, '0x1d073cf59Ae0C169cbc58B6fdD518822ae89173a', 'latest', OPTIMISM))
# 0x49F4D0222C880D4780b636662F5F18f572f2f88a

# print(underlying('0x49F4D0222C880D4780b636662F5F18f572f2f88a', '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1', 'latest', OPTIMISM))

# comptroller_contract = get_contract(get_comptoller_address(OPTIMISM), OPTIMISM, abi=ABI_UNITROLLER)

# all_rewards('0x49F4D0222C880D4780b636662F5F18f572f2f88a', 'latest', OPTIMISM)

#print(underlying_all('0x49F4D0222C880D4780b636662F5F18f572f2f88a', 'latest', OPTIMISM, reward=True))

# block = date_to_block('2022-02-10 15:00:00', 'optimism')
# print(get_locked('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', 'latest', OPTIMISM))
# print(get_locked('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', 'latest', OPTIMISM, reward=True))

# block = date_to_block('2023-02-10 15:00:00', 'optimism')
# x = underlying(
#     wallet='0x5ed64f02588c8b75582f2f8efd7a5521e3f897cc',
#     token_address='0x7F5c764cBc14f9669B88837ca1490cCa17c31607',
#     block=block,
#     blockchain='optimism',
#     reward=True
# )
# print(x)
