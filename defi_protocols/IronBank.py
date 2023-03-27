from defi_protocols.functions import get_node, get_contract, get_decimals, last_block, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, OPTIMISM, ZERO_ADDRESS

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
# STAKING REWARDS HELPER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Optimism - Staking Rewards Factory Address
STAKING_REWARDS_HELPER_OPTIMISM = '0x970D6b8c1479ec2bfE5a82dC69caFe4003099bC0'

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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_comptoller_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_comptoller_address(blockchain):
    if blockchain == OPTIMISM:
        return UNITROLLER_OPTIMISM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staking_rewards_factory_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staking_rewards_factory_address(blockchain):
    if blockchain == OPTIMISM:
        return STAKING_REWARDS_FACTORY_OPTIMISM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_veib_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_veib_address(blockchain):
    if blockchain == OPTIMISM:
        return VEIB_OPTIMISM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_ve_dist_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ve_dist_address(blockchain):
    if blockchain == OPTIMISM:
        return VE_DIST_OPTIMISM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_fee_dist_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_fee_dist_address(blockchain):
    if blockchain == OPTIMISM:
        return FEE_DIST_OPTIMISM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_itoken_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'underlying_token' = underlying_token -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_itoken_data(itoken_address, wallet, block, blockchain, web3=None, execution=1, index=0, underlying_token=None):
    """

    :param itoken_address:
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param underlying_token:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        itoken_data = {}

        itoken_data['contract'] = get_contract(itoken_address, blockchain, web3=web3, abi=ABI_ITOKEN, block=block)

        if underlying_token is not None:
            itoken_data['underlying'] = underlying_token
        else:
            try:
                itoken_data['underlying'] = itoken_data['contract'].functions.underlying().call(block_identifier=block)
            except:
                itoken_data['underlying'] = ZERO_ADDRESS

        itoken_data['decimals'] = itoken_data['contract'].functions.decimals().call()
        itoken_data['borrowBalanceStored'] = itoken_data['contract'].functions.borrowBalanceStored(wallet).call(
            block_identifier=block)
        itoken_data['balanceOf'] = itoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)
        itoken_data['exchangeRateStored'] = itoken_data['contract'].functions.exchangeRateStored().call(
            block_identifier=block)

        return itoken_data

    except GetNodeIndexError:
        return get_itoken_data(itoken_address, wallet, block, blockchain, underlying_token=underlying_token, index=0,
                               execution=execution + 1)

    except Exception:
        return get_itoken_data(itoken_address, wallet, block, blockchain, underlying_token=underlying_token,
                               index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'staking_rewards_contract' = staking_rewards_contract -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, itoken, block, blockchain, web3=None, execution=1, index=0, decimals=True,
                    staking_rewards_contract=None):
    '''
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param staking_rewards_factory_contract
    :return:
    '''
    if execution > MAX_EXECUTIONS:
        return None

    all_rewards = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        if staking_rewards_contract == None:
            staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                            web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

            staking_rewards_address = staking_rewards_factory_contract.functions.getStakingRewards(itoken).call(
                block_identifier=block)
            staking_rewards_contract = get_contract(staking_rewards_address, blockchain, web3=web3,
                                                    abi=ABI_STAKING_REWARDS, block=block)

        all_rewards_tokens = staking_rewards_contract.functions.getAllRewardsTokens().call()

        for reward_token in all_rewards_tokens:
            reward_earned = staking_rewards_contract.functions.earned(itoken, wallet).call(block_identifier=block)

            if decimals == True:
                reward_earned = reward_earned / (10 ** (get_decimals(reward_token, blockchain, web3=web3)))

            all_rewards.append([reward_token, reward_earned])

        return all_rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet, itoken, block, blockchain, decimals=decimals,
                               staking_rewards_contract=staking_rewards_contract, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, itoken, block, blockchain, decimals=decimals,
                               staking_rewards_contract=staking_rewards_contract, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def all_rewards(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    '''
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :return:
    '''
    if execution > MAX_EXECUTIONS:
        return None

    result = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                        web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

        staking_rewards_helper_address = ZERO_ADDRESS
        rewards_tokens = []
        for staking_rewards in staking_rewards_factory_contract.functions.getAllStakingRewards().call():
            staking_rewards_contract = get_contract(staking_rewards, blockchain, web3=web3, abi=ABI_STAKING_REWARDS,
                                                    block=block)

            if staking_rewards_helper_address is ZERO_ADDRESS:
                staking_rewards_helper_address = staking_rewards_contract.functions.helperContract().call()

            for rewards_token in staking_rewards_contract.functions.getAllRewardsTokens().call():
                if rewards_token is not [] and rewards_token not in rewards_tokens:
                    rewards_tokens.append(rewards_token)

        if staking_rewards_helper_address is not ZERO_ADDRESS and rewards_tokens is not []:
            staking_rewards_helper_contract = get_contract(staking_rewards_helper_address, blockchain, web3=web3,
                                                           abi=ABI_STAKING_REWARDS_HELPER, block=block)
            user_claimable_rewards = staking_rewards_helper_contract.functions.getUserClaimableRewards(wallet,
                                                                                                       rewards_tokens).call(
                block_identifier=block)

            for user_claimable_reward in user_claimable_rewards:
                if decimals is True:
                    reward_amount = user_claimable_reward[1] / (10 ** user_claimable_reward[0][2])

                result.append([user_claimable_reward[0][0], reward_amount])

        return result

    except GetNodeIndexError:
        return all_rewards(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return all_rewards(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


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
def get_locked(wallet, block, blockchain, nft_id=302, execution=1, web3=None, index=0, reward=False, decimals=True):
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

    balances = []
    result = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        veib_address = get_veib_address(blockchain)
        veib_contract = get_contract(veib_address, blockchain, web3=web3, abi=ABI_VEIB, block=block)
        ib_token = veib_contract.functions.token().call()

        if decimals is True:
            ib_decimals = get_decimals(ib_token, blockchain, web3=web3)
            veib_decimals = veib_contract.functions.decimals().call()
        else:
            ib_decimals = 0
            veib_decimals = 0

        if block == 'latest':
            block = last_block(blockchain, web3=web3)

        veib_balance = veib_contract.functions.balanceOfAtNFT(nft_id, block).call() / (10 ** veib_decimals)

        locked = veib_contract.functions.locked(nft_id).call(block_identifier=block)
        locked_balance = locked[0] / (10 ** ib_decimals)

        balances = [[veib_address, veib_balance], [ib_token, locked_balance]]

        if reward is True:
            ve_dist_contract = get_contract(get_ve_dist_address(blockchain), blockchain, web3=web3, abi=ABI_VE_DIST,
                                            block=block)
            ve_dist_reward_token = ve_dist_contract.functions.token().call()
            ve_dist_claimable_reward = ve_dist_contract.functions.claimable(nft_id).call(block_identifier=block)

            fee_dist_contract = get_contract(get_fee_dist_address(blockchain), blockchain, web3=web3, abi=ABI_VE_DIST,
                                             block=block)
            fee_dist_reward_token = fee_dist_contract.functions.token().call()
            fee_dist_claimable_reward = fee_dist_contract.functions.claimable(nft_id).call(block_identifier=block)

            if decimals is True:
                ve_dist_reward_token_decimals = get_decimals(ve_dist_reward_token, blockchain, web3=web3)
                fee_dist_reward_token_decimals = get_decimals(fee_dist_reward_token, blockchain, web3=web3)
            else:
                ve_dist_reward_token_decimals = 0
                fee_dist_reward_token_decimals = 0

            result.append(balances)
            result.append([[ve_dist_reward_token, ve_dist_claimable_reward / (10 ** ve_dist_reward_token_decimals)],
                           [fee_dist_reward_token, fee_dist_claimable_reward / (10 ** fee_dist_reward_token_decimals)]])
        else:
            result = balances

        return result

    except GetNodeIndexError:
        return get_locked(wallet, block, blockchain, nft_id=nft_id, reward=reward, decimals=decimals, index=0,
                          execution=execution + 1)

    except:
        return get_locked(wallet, block, blockchain, nft_id=nft_id, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, token_address, block, blockchain, web3=None, decimals=True, execution=1, index=0, reward=False):
    """

    :param wallet:
    :para token_address:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
    :param index:
    :param c_token_list:
    :param underlying_token_list:
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
        token_address = web3.to_checksum_address(token_address)

        staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                        web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

        itoken = staking_rewards_factory_contract.functions.getStakingToken(token_address).call()

        if itoken == ZERO_ADDRESS:
            return []

        itoken_data = get_itoken_data(itoken, wallet, block, blockchain, web3=web3, underlying_token=token_address)

        underlying_token_decimals = get_decimals(token_address, block=block, blockchain=blockchain, web3=web3,
                                                 index=index)

        mantissa = 18 - (itoken_data['decimals']) + underlying_token_decimals

        exchange_rate = itoken_data['exchangeRateStored'] / (10 ** mantissa)

        underlying_token_balance = itoken_data['balanceOf'] / (10 ** itoken_data['decimals']) * exchange_rate - \
                                   itoken_data['borrowBalanceStored'] / (10 ** underlying_token_decimals)

        if decimals == False:
            underlying_token_balance = underlying_token_balance * (10 ** underlying_token_decimals)

        staking_rewards_address = staking_rewards_factory_contract.functions.getStakingRewards(itoken).call(
            block_identifier=block)
        staking_rewards_contract = get_contract(staking_rewards_address, blockchain, web3=web3, abi=ABI_STAKING_REWARDS,
                                                block=block)

        staking_rewards_helper_address = staking_rewards_contract.functions.helperContract().call()
        staking_rewards_helper_contract = get_contract(staking_rewards_helper_address, blockchain, web3=web3,
                                                       abi=ABI_STAKING_REWARDS_HELPER, block=block)
        user_staked = staking_rewards_helper_contract.functions.getUserStaked(wallet).call(block_identifier=block)

        itoken_staked_balance = 0
        for itoken_staked_data in user_staked:
            if itoken_staked_data[0] == itoken:
                itoken_staked_balance = itoken_staked_data[1]
                break

        underlying_staked_balance = 0
        if itoken_staked_balance > 0:
            itoken_staked_balance = itoken_staked_balance / (10 ** get_decimals(itoken, blockchain, web3=web3))
            underlying_staked_balance = \
            unwrap(itoken_staked_balance, itoken, block, blockchain, web3=web3, decimals=decimals)[1]

        balances.append([token_address, underlying_token_balance, underlying_staked_balance])

        if reward is True:
            all_rewards = get_all_rewards(wallet, itoken, block, blockchain, web3=web3, decimals=decimals,
                                          staking_rewards_contract=staking_rewards_contract)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying(wallet, token_address, block, blockchain, reward=reward, decimals=decimals, index=0,
                          execution=execution + 1)

    except:
        return underlying(wallet, token_address, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying_all(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
    :param index:
    :param c_token_list:
    :param underlying_token_list:
    :return:
    """

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []
    result = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        unitroller_contract = get_contract(get_comptoller_address(blockchain), blockchain, web3=web3,
                                           abi=ABI_UNITROLLER, block=block)

        staking_rewards_factory_contract = get_contract(get_staking_rewards_factory_address(blockchain), blockchain,
                                                        web3=web3, abi=ABI_STAKING_REWARDS_FACTORY, block=block)

        user_staked = None
        for itoken in unitroller_contract.functions.getAllMarkets().call():

            itoken_data = get_itoken_data(itoken, wallet, block, blockchain, web3=web3)

            underlying_token = itoken_data['underlying']

            underlying_token_balance = 0
            if itoken_data['balanceOf'] > 0:

                if underlying_token is not ZERO_ADDRESS:

                    underlying_token_decimals = get_decimals(underlying_token, block=block, blockchain=blockchain,
                                                             web3=web3, index=index)

                    mantissa = 18 - (itoken_data['decimals']) + underlying_token_decimals

                    exchange_rate = itoken_data['exchangeRateStored'] / (10 ** mantissa)

                    underlying_token_balance = itoken_data['balanceOf'] / (
                                10 ** itoken_data['decimals']) * exchange_rate - itoken_data['borrowBalanceStored'] / (
                                                           10 ** underlying_token_decimals)

                    if decimals == False:
                        underlying_token_balance = underlying_token_balance * (10 ** underlying_token_decimals)

            if user_staked is None:
                staking_rewards_address = staking_rewards_factory_contract.functions.getStakingRewards(itoken).call(
                    block_identifier=block)
                staking_rewards_contract = get_contract(staking_rewards_address, blockchain, web3=web3,
                                                        abi=ABI_STAKING_REWARDS, block=block)

                staking_rewards_helper_address = staking_rewards_contract.functions.helperContract().call()
                staking_rewards_helper_contract = get_contract(staking_rewards_helper_address, blockchain, web3=web3,
                                                               abi=ABI_STAKING_REWARDS_HELPER, block=block)
                user_staked = staking_rewards_helper_contract.functions.getUserStaked(wallet).call(
                    block_identifier=block)

            itoken_staked_balance = 0
            for itoken_staked_data in user_staked:
                if itoken_staked_data[0] == itoken:
                    itoken_staked_balance = itoken_staked_data[1]
                    break

            underlying_staked_balance = 0
            if itoken_staked_balance > 0:
                itoken_staked_balance = itoken_staked_balance / (10 ** get_decimals(itoken, blockchain, web3=web3))
                underlying_staked_balance = \
                unwrap(itoken_staked_balance, itoken, block, blockchain, web3=web3, decimals=decimals)[1]

            if underlying_token_balance > 0 or underlying_staked_balance > 0:
                balances.append([underlying_token, underlying_token_balance, underlying_staked_balance])

        if reward is True:
            rewards = all_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)

            result.append(balances)
            result.append(rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying_all(wallet, block, blockchain, decimals=decimals, reward=reward, index=0,
                              execution=execution + 1)

    except:
        return underlying_all(wallet, block, blockchain, decimals=decimals, reward=reward, index=index + 1,
                              execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(itoken_amount, itoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param itoken_amount:
    :param itoken_address:
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

        itoken_contract = get_contract(itoken_address, blockchain, abi=ABI_ITOKEN, web3=web3, block=block)
        itoken_decimals = itoken_contract.functions.decimals().call()
        exchange_rate = itoken_contract.functions.exchangeRateStored().call(block_identifier=block)

        underlying_token = itoken_contract.functions.underlying().call()
        if decimals == True:
            underlying_token_decimals = get_decimals(underlying_token, blockchain, web3=web3)
        else:
            underlying_token_decimals = 0

        underlying_token_balance = itoken_amount * exchange_rate / (
                    10 ** (18 - itoken_decimals + underlying_token_decimals))

        return [underlying_token, underlying_token_balance]

    except GetNodeIndexError:
        return unwrap(itoken_amount, itoken_address, block, blockchain, decimals=decimals, index=0,
                      execution=execution + 1)

    except:
        return unwrap(itoken_amount, itoken_address, block, blockchain, decimals=decimals, index=index + 1,
                      execution=execution)


''' 
----- Testing -----
'''

# print(underlying_all('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', 'latest', OPTIMISM, reward=True))

# print(underlying('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', '0x7F5c764cBc14f9669B88837ca1490cCa17c31607', 'latest', OPTIMISM, reward=True))
# 0xE173cC94d4755b72eB9196Cf50DbcD2Cba54e348

# print(unwrap(198489.26169641, '0x1d073cf59Ae0C169cbc58B6fdD518822ae89173a', 'latest', OPTIMISM))
# 0x49F4D0222C880D4780b636662F5F18f572f2f88a

# print(underlying('0x49F4D0222C880D4780b636662F5F18f572f2f88a', '0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1', 'latest', OPTIMISM))

# comptroller_contract = get_contract(get_comptoller_address(OPTIMISM), OPTIMISM, abi=ABI_UNITROLLER)

# all_rewards('0x49F4D0222C880D4780b636662F5F18f572f2f88a', 'latest', OPTIMISM)

# print(underlying_all('0x49F4D0222C880D4780b636662F5F18f572f2f88a', 'latest', OPTIMISM, reward=True))

# print(get_locked('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', 'latest', OPTIMISM))
# print(get_locked('0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC', 'latest', OPTIMISM, reward=True))
