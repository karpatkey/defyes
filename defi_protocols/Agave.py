from defi_protocols.functions import *

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROTOCOL DATA PROVIDER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Protocol Data Provider - XDAI
# PDP_XDAI = '0x75e5cF901f3A576F72AB6bCbcf7d81F1619C6a12'
PDP_XDAI = '0x24dCbd376Db23e4771375092344f5CbEA3541FC0'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LENDING POOL ADDRESSES PROVIDER REGISTRY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Lending Pool Addresses Provider Registry - XDAI
LPAPR_XDAI = '0x3673C22153E363B1da69732c4E0aA71872Bbb87F'
# 0x5E15d5E33d318dCEd84Bfe3F4EACe07909bE6d9c

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHAINLINK PRICE FEEDS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# XDAI
# XDAI/USD Price Feed
CHAINLINK_XDAI_USD = '0x678df3415fc31947dA4324eC63212874be5a82f8'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Protocol Data Provider ABI - getAllReservesTokens, getUserReserveData, getReserveConfigurationData, getReserveTokensAddresses
ABI_PDP = '[{"inputs":[],"name":"getAllReservesTokens","outputs":[{"components":[{"internalType":"string","name":"symbol","type":"string"},{"internalType":"address","name":"tokenAddress","type":"address"}],"internalType":"struct AaveProtocolDataProvider.TokenData[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"getUserReserveData","outputs":[{"internalType":"uint256","name":"currentATokenBalance","type":"uint256"},{"internalType":"uint256","name":"currentStableDebt","type":"uint256"},{"internalType":"uint256","name":"currentVariableDebt","type":"uint256"},{"internalType":"uint256","name":"principalStableDebt","type":"uint256"},{"internalType":"uint256","name":"scaledVariableDebt","type":"uint256"},{"internalType":"uint256","name":"stableBorrowRate","type":"uint256"},{"internalType":"uint256","name":"liquidityRate","type":"uint256"},{"internalType":"uint40","name":"stableRateLastUpdated","type":"uint40"},{"internalType":"bool","name":"usageAsCollateralEnabled","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveConfigurationData","outputs":[{"internalType":"uint256","name":"decimals","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"liquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"liquidationBonus","type":"uint256"},{"internalType":"uint256","name":"reserveFactor","type":"uint256"},{"internalType":"bool","name":"usageAsCollateralEnabled","type":"bool"},{"internalType":"bool","name":"borrowingEnabled","type":"bool"},{"internalType":"bool","name":"stableBorrowRateEnabled","type":"bool"},{"internalType":"bool","name":"isActive","type":"bool"},{"internalType":"bool","name":"isFrozen","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveTokensAddresses","outputs":[{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"}],"stateMutability":"view","type":"function"}]'

# Lending Pool Addresses Provider Registry ABI - getLendingPool, getPriceOracle
ABI_LPAPR = '[{"inputs":[],"name":"getLendingPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getPriceOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# Lending Pool ABI - getUserAccountData, getReserveData
ABI_LENDING_POOL = '[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"internalType":"uint256","name":"totalCollateralETH","type":"uint256"},{"internalType":"uint256","name":"totalDebtETH","type":"uint256"},{"internalType":"uint256","name":"availableBorrowsETH","type":"uint256"},{"internalType":"uint256","name":"currentLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveData","outputs":[{"components":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.ReserveConfigurationMap","name":"configuration","type":"tuple"},{"internalType":"uint128","name":"liquidityIndex","type":"uint128"},{"internalType":"uint128","name":"variableBorrowIndex","type":"uint128"},{"internalType":"uint128","name":"currentLiquidityRate","type":"uint128"},{"internalType":"uint128","name":"currentVariableBorrowRate","type":"uint128"},{"internalType":"uint128","name":"currentStableBorrowRate","type":"uint128"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"},{"internalType":"uint8","name":"id","type":"uint8"}],"internalType":"struct DataTypes.ReserveData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]'

# ChainLink: ETH/USD Price Feed ABI - latestAnswer, decimals
ABI_CHAINLINK_XDAI_USD = '[{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Price Oracle ABI - getAssetPrice
ABI_PRICE_ORACLE = '[{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Staked Agave ABI - REWARD_TOKEN, getTotalRewardsBalance, assets
ABI_STKAGAVE = '[{"inputs":[],"name":"REWARD_TOKEN","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"getTotalRewardsBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"assets","outputs":[{"internalType":"uint128","name":"emissionPerSecond","type":"uint128"},{"internalType":"uint128","name":"lastUpdateTimestamp","type":"uint128"},{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"view","type":"function"},\
                                {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}]'


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_protocol_data_provider
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_protocol_data_provider(blockchain):
    if blockchain == XDAI:
        return PDP_XDAI


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lpapr_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lpapr_address(blockchain):
    if blockchain == XDAI:
        return LPAPR_XDAI


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_stkagave_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_stkagave_address(blockchain):
    if blockchain == XDAI:
        return STKAGAVE_XDAI


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_reserves_tokens
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_reserves_tokens(pdp_contract, block):
    """

    :param pdp_contract:
    :return:
    """
    reserves_tokens_addresses = []

    reserves_tokens = pdp_contract.functions.getAllReservesTokens().call(block_identifier=block)

    for reserves_token in reserves_tokens:
        reserves_tokens_addresses.append(reserves_token[1])

    return reserves_tokens_addresses


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_reserves_tokens_balances
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    balances = []

    pdp_address = get_protocol_data_provider(blockchain)
    if pdp_address is None:
        return None

    pdp_contract = get_contract(pdp_address, blockchain, web3=web3, abi=ABI_PDP, block=block)

    reserves_tokens = get_reserves_tokens(pdp_contract, block)

    for reserves_token in reserves_tokens:

        try:
            user_reserve_data = pdp_contract.functions.getUserReserveData(reserves_token, wallet).call(
                block_identifier=block)
        except:
            continue

        if decimals == True:
            token_decimals = get_decimals(reserves_token, blockchain, web3=web3)
        else:
            token_decimals = 0

        # balance = currentATokenBalance - currentStableDebt - currentVariableDebt
        balance = (user_reserve_data[0] - user_reserve_data[1] - user_reserve_data[2]) / (10 ** token_decimals)

        if balance != 0:
            balances.append([reserves_token, balance])

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_data(wallet, block, blockchain, execution=1, web3=None, index=1, decimals=True):
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

    agave_data = {}
    collaterals = []
    debts = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lpapr_address = get_lpapr_address(blockchain)
        if lpapr_address is None:
            return None

        lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

        lending_pool_address = lpapr_contract.functions.getLendingPool().call()
        lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL,
                                             block=block)

        chainlink_eth_usd_contract = get_contract(CHAINLINK_XDAI_USD, blockchain, web3=web3, abi=ABI_CHAINLINK_XDAI_USD,
                                                  block=block)
        chainlink_eth_usd_decimals = chainlink_eth_usd_contract.functions.decimals().call()
        xdai_usd_price = chainlink_eth_usd_contract.functions.latestAnswer().call(block_identifier=block) / (
                    10 ** chainlink_eth_usd_decimals)

        balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)
        if balances is None:
            return None

        if len(balances) > 0:

            price_oracle_address = lpapr_contract.functions.getPriceOracle().call()
            price_oracle_contract = get_contract(price_oracle_address, blockchain, web3=web3, abi=ABI_PRICE_ORACLE,
                                                 block=block)

            for balance in balances:
                asset = {}

                asset['token_address'] = balance[0]
                asset['token_amount'] = abs(balance[1])
                asset['token_price_usd'] = price_oracle_contract.functions.getAssetPrice(asset['token_address']).call(
                    block_identifier=block) / (10 ** 18) * xdai_usd_price

                if balance[1] < 0:
                    debts.append(asset)
                else:
                    collaterals.append(asset)

        # getUserAccountData return a list with the following data:
        # [0] = totalCollateralETH, [1] = totalDebtETH, [2] = availableBorrowsETH, [3] = currentLiquidationThreshold, [4] = ltv, [5] = healthFactor
        user_account_data = lending_pool_contract.functions.getUserAccountData(wallet).call(block_identifier=block)

        # Collateral Ratio
        agave_data['collateral_ratio'] = (user_account_data[0] / user_account_data[1]) * 100

        # Liquidation Ratio
        agave_data['liquidation_ratio'] = (1 / user_account_data[3]) * 1000000

        # Ether price in USD
        agave_data['xdai_price_usd'] = xdai_usd_price

        # Collaterals Data
        agave_data['collaterals'] = collaterals

        # Debts Data
        agave_data['debts'] = debts

        return agave_data


    except GetNodeIndexError:
        return get_data(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_data(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True):
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

    all_rewards = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        stkagave_address = get_stkagave_address(blockchain)
        if stkagave_address is None:
            return None

        stkagave_contract = get_contract(stkagave_address, blockchain, web3=web3, abi=ABI_STKAGAVE, block=block)

        reward_token = stkagave_contract.functions.REWARD_TOKEN().call()

        if decimals is True:
            reward_token_decimals = get_decimals(reward_token, blockchain, web3=web3)
        else:
            reward_token_decimals = 0

        reward_balance = stkagave_contract.functions.getTotalRewardsBalance(wallet).call(block_identifier=block) / (
                    10 ** reward_token_decimals)

        all_rewards.append([reward_token, reward_balance])

        return all_rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance], where balance = currentATokenBalance - currentStableDebt - currentStableDebt
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying_all(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True, reward=False):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param execution:
    :param web3:
    :param index:
    :param decimals:
    :param reward:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    result = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)
        if balances is None:
            return None

        if reward is True:
            all_rewards = get_all_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying_all(wallet, block, blockchain, reward=reward, decimals=decimals, index=0,
                              execution=execution + 1)

    except:
        return underlying_all(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                              execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_apr
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
#             {'metric': 'apr'/'apy', 'type': 'variable_borrow', 'value': borrow_apr/borrow_apy},
#             {'metric': 'apr'/'apy', 'type': 'stable_borrow', 'value': borrow_apr/borrow_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_apr(token_address, block, blockchain, web3=None, execution=1, index=0, apy=False):
    """

    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param apy:
    :return:
    """

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lpapr_address = get_lpapr_address(blockchain)
        lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

        lending_pool_address = lpapr_contract.functions.getLendingPool().call()
        lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL,
                                             block=block)

        reserve_data = lending_pool_contract.functions.getReserveData(token_address).call(block_identifier=block)

        liquidity_rate = reserve_data[3]
        variable_borrow_rate = reserve_data[4]
        stable_borrow_rate = reserve_data[5]

        ray = 10 ** 27
        seconds_per_year = 31536000

        deposit_apr = liquidity_rate / ray
        variable_borrow_apr = variable_borrow_rate / ray
        stable_borrow_apr = stable_borrow_rate / ray

        deposit_apy = ((1 + (deposit_apr / seconds_per_year)) ** seconds_per_year) - 1
        variable_borrow_apy = ((1 + (variable_borrow_apr / seconds_per_year)) ** seconds_per_year) - 1
        stable_borrow_apy = ((1 + (stable_borrow_apr / seconds_per_year)) ** seconds_per_year) - 1

        if apy is False:
            return [{'metric': 'apr', 'type': 'supply', 'value': deposit_apr},
                    {'metric': 'apr', 'type': 'variable_borrow', 'value': variable_borrow_apr},
                    {'metric': 'apr', 'type': 'stable_borrow', 'value': stable_borrow_apr}]
        else:
            deposit_apy = ((1 + (deposit_apr / seconds_per_year)) ** seconds_per_year) - 1
            variable_borrow_apy = ((1 + (variable_borrow_apr / seconds_per_year)) ** seconds_per_year) - 1
            stable_borrow_apy = ((1 + (stable_borrow_apr / seconds_per_year)) ** seconds_per_year) - 1

            return [{'metric': 'apy', 'type': 'supply', 'value': deposit_apy},
                    {'metric': 'apy', 'type': 'variable_borrow', 'value': variable_borrow_apy},
                    {'metric': 'apy', 'type': 'stable_borrow', 'value': stable_borrow_apy}]

    except GetNodeIndexError:
        return get_apr(token_address, block, blockchain, apy=apy, index=0, execution=execution + 1)

    except:
        return get_apr(token_address, block, blockchain, apy=apy, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staking_apr
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'staking', 'value': staking_apr/staking_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staking_apr(block, blockchain, web3=None, execution=1, index=0, apy=False):
    """

    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :return:
    """

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        seconds_per_year = 31536000
        stkagave_address = get_stkagave_address(blockchain)
        if stkagave_address is None:
            return None

        stkagave_contract = get_contract(stkagave_address, blockchain, web3=web3, abi=ABI_STKAGAVE, block=block)
        emission_per_second = stkagave_contract.functions.assets(stkagave_address).call(block_identifier=block)[0]
        agave_token_address = stkagave_contract.functions.REWARD_TOKEN().call()
        current_stakes = balance_of(stkagave_address, agave_token_address, block, blockchain, web3=web3, decimals=False)

        staking_apr = emission_per_second * seconds_per_year / current_stakes

        if apy is False:
            return [{'metric': 'apr', 'type': 'staking', 'value': staking_apr}]
        else:
            staking_apy = ((1 + (staking_apr / seconds_per_year)) ** seconds_per_year) - 1

            return [{'metric': 'apy', 'type': 'staking', 'value': staking_apy}]

    except GetNodeIndexError:
        return get_staking_apr(block, blockchain, apy=apy, index=0, execution=execution + 1)

    except:
        return get_staking_apr(block, blockchain, apy=apy, index=index + 1, execution=execution)

def get_staked(wallet: str, block: Union[int, str], blockchain: str, web3=None, execution: int = 1, index: int = 0, decimals: bool = True) -> list:
    """

    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :return:
    """

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        agave_wallet = web3.to_checksum_address(wallet)

        stk_agave_address = get_stkagave_address(blockchain)
        stkagave_contract = get_contract(stk_agave_address, blockchain, web3=web3, abi=ABI_STKAGAVE, block=block)
        stkagave_balance = stkagave_contract.functions.balanceOf(agave_wallet).call(block_identifier=block)
        stkagave_decimals = stkagave_contract.functions.decimals().call()

        if decimals:
            stkagave_balance = stkagave_balance / 10 ** stkagave_decimals
        
        balances.append([stk_agave_address,stkagave_balance])

        return balances


    except GetNodeIndexError:
        return get_staked(wallet, block, blockchain, web3=web3, index=0, execution=execution + 1)

    except:
        return get_staked(wallet, block, blockchain, web3=web3, index=index + 1, execution=execution)
