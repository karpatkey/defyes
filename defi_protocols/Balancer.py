from typing import Union
from datetime import datetime, timedelta

from defi_protocols.functions import get_node, get_contract, get_decimals, block_to_date, date_to_block, balance_of, get_logs, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, ETHEREUM, BAL_ETH, BB_A_USD_OLD_ETH, BB_A_USD_ETH, POLYGON, ARBITRUM, BAL_POL, ZERO_ADDRESS
from defi_protocols.prices.prices import get_price

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BALANCER VAULT
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault Contract Address
VAULT = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LIQUIDITY GAUGE FACTORY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ETHEREUM = '0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC'

# Polygon Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_POLYGON = '0x3b8cA519122CdD8efb272b0D3085453404B25bD0'

# Arbitrum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ARBITRUM = '0xb08E16cFc07C684dAA2f93C70323BAdb2A6CBFd2'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL Contract Address
VEBAL = '0xC128a9954e6c874eA3d62ce62B468bA073093F25'

# veBAL Fee Distributor Contract
VEBAL_FEE_DISTRIBUTOR = '0xD3cf852898b21fc233251427c2DC93d3d604F3BB'
# VEBAL_FEE_DISTRIBUTOR = '0x26743984e3357eFC59f2fd6C1aFDC310335a61c9' #DEPRECATED

# veBAL Reward Tokens - BAL, bb-a-USD old deployment, bb-a-USD
VEBAL_REWARD_TOKENS = [BAL_ETH, BB_A_USD_OLD_ETH, BB_A_USD_ETH]

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault ABI - getPoolTokens, getPool
ABI_VAULT = '[{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPoolTokens","outputs":[{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"enum IVault.PoolSpecialization","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Liquidity Gauge Factory ABI - getPoolGauge
ABI_LIQUIDITY_GAUGE_FACTORY = '[{"inputs":[{"internalType":"address","name":"pool","type":"address"}],"name":"getPoolGauge","outputs":[{"internalType":"contract ILiquidityGauge","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# veBAL ABI - locked, token
ABI_VEBAL = '[{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"locked","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"amount","type":"int128"},{"name":"end","type":"uint256"}]}]}]'

# veBAL Fee Distributor ABI - claimTokens
ABI_VEBAL_FEE_DISTRIBUTOR = '[{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"}],"name":"claimTokens","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"}]'

# LP Token ABI - getPoolId, decimals, getActualSupply, getVirtualSupply, totalSupply, getBptIndex, balanceOf, getSwapFeePercentage
ABI_LPTOKEN = '[{"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getActualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getVirtualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getBptIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getSwapFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Gauge ABI - claimable_tokens, claimable_reward, reward_count, reward_tokens
ABI_GAUGE = '[{"stateMutability":"nonpayable","type":"function","name":"claimable_tokens","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"claimable_reward","inputs":[{"name":"_user","type":"address"},{"name":"_reward_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_tokens","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]}]'

# ABI - Pool Tokens - decimals, getRate
ABI_POOL_TOKENS_BALANCER = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getMainToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EVENT SIGNATURES
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Swap Event Signature
SWAP_EVENT_SIGNATURE = 'Swap(bytes32,address,address,uint256,uint256)'


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_gauge_factory_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_gauge_factory_address(blockchain):
    if blockchain == ETHEREUM:
        return LIQUIDITY_GAUGE_FACTORY_ETHEREUM

    elif blockchain == POLYGON:
        return LIQUIDITY_GAUGE_FACTORY_POLYGON

    elif blockchain == ARBITRUM:
        return LIQUIDITY_GAUGE_FACTORY_ARBITRUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lptoken_data = {}

        lptoken_data['contract'] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)
        lptoken_data['poolId'] = lptoken_data['contract'].functions.getPoolId().call()
        lptoken_data['decimals'] = lptoken_data['contract'].functions.decimals().call()

        try:
            lptoken_data['totalSupply'] = lptoken_data['contract'].functions.getActualSupply().call(
                block_identifier=block)
            lptoken_data['isBoosted'] = True
        except:
            try:
                lptoken_data['totalSupply'] = lptoken_data['contract'].functions.getVirtualSupply().call(
                    block_identifier=block)
                lptoken_data['isBoosted'] = True
            except:
                lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(
                    block_identifier=block)
                lptoken_data['isBoosted'] = False

        if lptoken_data['isBoosted'] == True:
            try:
                lptoken_data['bptIndex'] = lptoken_data['contract'].functions.getBptIndex().call()
            except:
                lptoken_data['isBoosted'] = False
                lptoken_data['bptIndex'] = None
        else:
            lptoken_data['bptIndex'] = None

        return lptoken_data

    except GetNodeIndexError:
        return get_lptoken_data(lptoken_address, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_lptoken_data(lptoken_address, block, blockchain, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_address(blockchain):
    if blockchain == ETHEREUM:
        return BAL_ETH
    elif blockchain == POLYGON:
        return BAL_POL


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuples: [bal_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_rewards(web3, gauge_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param gauge_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    bal_address = get_bal_address(blockchain)

    if decimals is True:
        bal_decimals = get_decimals(bal_address, blockchain, web3=web3)
    else:
        bal_decimals = 0

    if blockchain == ETHEREUM:
        bal_rewards = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block) / (
                    10 ** bal_decimals)
    else:
        bal_rewards = gauge_contract.functions.claimable_reward(wallet, bal_address).call(block_identifier=block) / (
                    10 ** bal_decimals)

    return [bal_address, bal_rewards]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, gauge_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param gauge_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    rewards = []

    for i in range(gauge_contract.functions.reward_count().call()):

        token_address = gauge_contract.functions.reward_tokens(i).call()
        token_rewards = gauge_contract.functions.claimable_reward(wallet, token_address).call(block_identifier=block)

        if decimals == True:
            token_decimals = get_decimals(token_address, blockchain, web3=web3)
        else:
            token_decimals = 0

        token_rewards = token_rewards / (10 ** token_decimals)

        rewards.append([token_address, token_rewards])

    return rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vebal_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vebal_rewards(web3, wallet, block, blockchain, decimals=True):
    vebal_rewards = []

    fee_distributor_contract = get_contract(VEBAL_FEE_DISTRIBUTOR, blockchain, web3=web3, abi=ABI_VEBAL_FEE_DISTRIBUTOR,
                                            block=block)
    claim_tokens = fee_distributor_contract.functions.claimTokens(wallet, VEBAL_REWARD_TOKENS).call(
        block_identifier=block)

    for i in range(len(VEBAL_REWARD_TOKENS)):
        token_address = VEBAL_REWARD_TOKENS[i]
        token_rewards = claim_tokens[i]

        if decimals == True:
            token_decimals = get_decimals(token_address, blockchain, web3=web3)
        else:
            token_decimals = 0

        token_rewards = token_rewards / (10 ** token_decimals)

        vebal_rewards.append([token_address, token_rewards])

    return vebal_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'gauge_address' = gauge_address -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True,
                    gauge_address=None):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param gauge_address:
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

        if gauge_address is None:
            gauge_factory_address = get_gauge_factory_address(blockchain)
            gauge_factory_contract = get_contract(gauge_factory_address, blockchain, web3=web3,
                                                  abi=ABI_LIQUIDITY_GAUGE_FACTORY, block=block)
            gauge_address = gauge_factory_contract.functions.getPoolGauge(lptoken_address).call()

        # veBAL Rewards
        if blockchain == ETHEREUM:
            vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

            if (lptoken_address == vebal_contract.functions.token().call()):
                vebal_rewards = get_vebal_rewards(web3, wallet, block, blockchain, decimals=decimals)

                if len(vebal_rewards) > 0:
                    for vebal_reward in vebal_rewards:
                        all_rewards.append(vebal_reward)

        if gauge_address != ZERO_ADDRESS:
            gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)

            bal_rewards = get_bal_rewards(web3, gauge_contract, wallet, block, blockchain)
            all_rewards.append(bal_rewards)

            rewards = get_rewards(web3, gauge_contract, wallet, block, blockchain)

            if len(rewards) > 0:
                for reward in rewards:
                    all_rewards.append(reward)

        return all_rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, gauge_address=gauge_address,
                               decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, gauge_address=gauge_address,
                               decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'aura_staked' = Staked LP Token Balance in Aura
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance, locked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False,
               aura_staked=None, decimals=True):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param reward:
    :param aura_staked:
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

        vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

        gauge_factory_address = get_gauge_factory_address(blockchain)
        gauge_factory_contract = get_contract(gauge_factory_address, blockchain, web3=web3,
                                              abi=ABI_LIQUIDITY_GAUGE_FACTORY, block=block)

        gauge_address = gauge_factory_contract.functions.getPoolGauge(lptoken_address).call()

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

        lptoken_data['balanceOf'] = lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)

        if gauge_address != ZERO_ADDRESS:
            lptoken_data['staked'] = balance_of(wallet, gauge_address, block, blockchain, web3=web3, decimals=False)
        else:
            lptoken_data['staked'] = 0

        lptoken_data['locked'] = 0
        if blockchain == ETHEREUM:
            vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

            if (lptoken_address == vebal_contract.functions.token().call()):
                try:
                    lptoken_data['locked'] = vebal_contract.functions.locked(wallet).call(block_identifier=block)[0]
                except:
                    lptoken_data['locked'] = 0

        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = pool_tokens_data[1]

        pool_balance_fraction = lptoken_data['balanceOf'] / lptoken_data['totalSupply']
        pool_staked_fraction = lptoken_data['staked'] / lptoken_data['totalSupply']
        pool_locked_fraction = lptoken_data['locked'] / lptoken_data['totalSupply']

        for i in range(len(pool_tokens)):

            if i == lptoken_data['bptIndex']:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER,
                                          block=block)

            if decimals is True:
                token_decimals = token_contract.functions.decimals().call()
            else:
                token_decimals = 0

            if lptoken_data['isBoosted'] is True:
                token_rate = token_contract.functions.getRate().call(block_identifier=block) / (
                            10 ** token_contract.functions.decimals().call())
            else:
                token_rate = 1

            token_balance = pool_balances[i] / (10 ** token_decimals) * pool_balance_fraction * token_rate

            if aura_staked is None:
                token_staked = pool_balances[i] / (10 ** token_decimals) * pool_staked_fraction * token_rate
            else:
                aura_pool_fraction = aura_staked / lptoken_data['totalSupply']
                token_staked = pool_balances[i] / (10 ** token_decimals) * aura_pool_fraction

            token_locked = pool_balances[i] / (10 ** token_decimals) * pool_locked_fraction * token_rate

            if lptoken_data['isBoosted'] is True:
                balances.append(
                    [token_contract.functions.getMainToken().call(), token_balance, token_staked, token_locked])
            else:
                balances.append([pool_tokens[i], token_balance, token_staked, token_locked])

        if reward is True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                          gauge_address=gauge_address)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying(wallet, lptoken_address, block, blockchain, reward=reward, aura_staked=aura_staked,
                          decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, lptoken_address, block, blockchain, reward=reward, aura_staked=aura_staked,
                          decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 element:
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

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3, index=index)

        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = pool_tokens_data[1]

        for i in range(len(pool_tokens)):

            if i == lptoken_data['bptIndex']:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER,
                                          block=block)

            if decimals is True:
                token_decimals = token_contract.functions.decimals().call()
            else:
                token_decimals = 0

            if lptoken_data['isBoosted'] is True:
                token_rate = token_contract.functions.getRate().call(block_identifier=block) / (10 ** token_decimals)
            else:
                token_rate = 1

            token_balance = pool_balances[i] / (10 ** token_decimals) * token_rate

            if lptoken_data['isBoosted'] is True:
                balances.append([token_contract.functions.getMainToken().call(), token_balance])
            else:
                balances.append([pool_tokens[i], token_balance])

        return balances

    except GetNodeIndexError:
        return pool_balances(lptoken_address, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return pool_balances(lptoken_address, block, blockchain, decimals=decimals, index=index + 1,
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
def unwrap(lptoken_amount, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param lptoken_amount:
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

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = pool_tokens_data[1]

        pool_balance_fraction = lptoken_amount * (10 ** lptoken_data['decimals']) / lptoken_data['totalSupply']

        for i in range(len(pool_tokens)):

            if i == lptoken_data['bptIndex']:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER,
                                          block=block)

            if decimals is True:
                token_decimals = token_contract.functions.decimals().call()
            else:
                token_decimals = 0

            if lptoken_data['isBoosted'] is True:
                token_rate = token_contract.functions.getRate().call(block_identifier=block) / (
                            10 ** token_contract.functions.decimals().call())
            else:
                token_rate = 1

            token_balance = pool_balances[i] / (10 ** token_decimals) * pool_balance_fraction * token_rate

            if lptoken_data['isBoosted'] is True:
                balances.append(
                    [token_contract.functions.getMainToken().call(), token_balance])
            else:
                balances.append([pool_tokens[i], token_balance])

        return balances

    except GetNodeIndexError:
        return unwrap(lptoken_amount, lptoken_address, block, blockchain, decimals=decimals, index=0,
                      execution=execution + 1)

    except:
        return unwrap(lptoken_amount, lptoken_address, block, blockchain, decimals=decimals, index=index + 1,
                      execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# swap_fees
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param lptoken_address:
    :param block_start:
    :param block_end:
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

    result = {}
    hash_overlap = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block_start, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

        pool_id = '0x' + lptoken_contract.functions.getPoolId().call().hex()
        result['swaps'] = []

        get_logs_bool = True
        block_from = block_start
        block_to = block_end

        swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()

        while get_logs_bool:
            swap_logs = get_logs(block_from, block_to, VAULT, swap_event, blockchain, topic1=pool_id)

            log_count = len(swap_logs)

            if log_count != 0:
                last_block = int(
                    swap_logs[log_count - 1]['blockNumber'][2:len(swap_logs[log_count - 1]['blockNumber'])], 16)

                for swap_log in swap_logs:
                    block_number = int(swap_log['blockNumber'][2:len(swap_log['blockNumber'])], 16)

                    if swap_log['transactionHash'] in swap_log:
                        continue

                    if block_number == last_block:
                        hash_overlap.append(swap_log['transactionHash'])

                    token_in = web3.to_checksum_address('0x' + swap_log['topics'][2][-40:])
                    token_in_decimals = get_decimals(token_in, blockchain, web3=web3)

                    lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
                    swap_fee = lptoken_contract.functions.getSwapFeePercentage().call(block_identifier=block_number) / (
                                10 ** lptoken_decimals)

                    swap_data = {
                        'block': block_number,
                        'tokenIn': token_in,
                        'amountIn': swap_fee * int(swap_log['data'][2:66], 16) / (10 ** token_in_decimals)
                    }

                    result['swaps'].append(swap_data)

            if log_count < 1000:
                get_logs_bool = False

            else:
                block_from = block_number

        return result

    except GetNodeIndexError:
        return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals=decimals, index=0,
                         execution=execution + 1)

    except:
        return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals=decimals, index=index + 1,
                         execution=execution)


def get_swap_fees_APR(lptoken_address: str, blockchain: str, block_end: Union[int, str] = 'latest', web3=None,
                      days: int = 1, apy: bool = False, execution: int = 1, index: int = 0) -> int:
    block_start = date_to_block(datetime.strftime(
        datetime.strptime(block_to_date(block_end, blockchain), '%Y-%m-%d %H:%M:%S') - timedelta(days=days),
        '%Y-%m-%d %H:%M:%S'), blockchain)
    fees = swap_fees(lptoken_address, block_start, block_end, blockchain, web3)
    # create a dictionary to store the total amountIn for each tokenIn
    totals_dict = {}

    for swap in fees['swaps']:
        token_in = swap['tokenIn']
        amount_in = swap['amountIn']
        if token_in in totals_dict:
            totals_dict[token_in] += amount_in
        else:
            totals_dict[token_in] = amount_in

    totals_list = [(token_in, amount_in) for token_in, amount_in in totals_dict.items()]

    fee = 0
    for k in totals_list:
        fee += k[1] * get_price(k[0], block_end, blockchain, web3)[0]
    pool_balance = pool_balances(lptoken_address, block_end, blockchain)
    tvl = 0
    for l in pool_balance:
        tvl += l[1] * get_price(l[0], block_end, blockchain, web3)[0]

    rate = fee / tvl
    apr = (((1 + rate) ** (365 / days) - 1) * 100) / 2
    seconds_per_year = 365 * 24 * 60 * 60
    if apy == True:
        apy = (1 + (apr / seconds_per_year)) ** (seconds_per_year) - 1
        return apy
    else:
        return apr

    # blockchain = ETHEREUM
# lptoken = '0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56'
# blockstart = date_to_block('2023-02-20 18:24:00',blockchain)
# blockend = date_to_block('2023-03-03 00:00:00',blockchain)

# # balances = pool_balances(lptoken,blockend,blockchain)
# # print(balances)
# feess = get_swap_fees_APR(lptoken,blockchain,blockend)
# print(feess)
