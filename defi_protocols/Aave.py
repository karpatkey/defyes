import logging
from typing import Union, Optional

from defi_protocols.constants import ETHEREUM, STKAAVE_ETH, MAX_EXECUTIONS
from defi_protocols.functions import get_contract, get_node, get_decimals, balance_of, GetNodeIndexError


logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROTOCOL DATA PROVIDER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Protocol Data Provider - Ethereum
PDP_ETHEREUM = '0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LENDING POOL ADDRESSES PROVIDER REGISTRY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Lending Pool Addresses Provider Registry - Ethereum
LPAPR_ETHEREUM = '0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STAKED ABPT TOKEN
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
STAKED_ABPT_TOKEN = '0xa1116930326D21fB917d5A27F1E9943A9595fb47'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHAINLINK PRICE FEEDS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETHEREUM
# ETH/USD Price Feed
CHAINLINK_ETH_USD = '0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419'

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
ABI_CHAINLINK_ETH_USD = '[{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Price Oracle ABI - getAssetPrice
ABI_PRICE_ORACLE = '[{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Staked Aave ABI - REWARD_TOKEN, getTotalRewardsBalance, assets, balanceOf
ABI_STKAAVE = '[{"inputs":[],"name":"REWARD_TOKEN","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"getTotalRewardsBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"assets","outputs":[{"internalType":"uint128","name":"emissionPerSecond","type":"uint128"},{"internalType":"uint128","name":"lastUpdateTimestamp","type":"uint128"},{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}]'


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_protocol_data_provider
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_protocol_data_provider(blockchain):
    if blockchain == ETHEREUM:
        return PDP_ETHEREUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lpapr_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lpapr_address(blockchain):
    if blockchain == ETHEREUM:
        return LPAPR_ETHEREUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_stkaave_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_stkaave_address(blockchain):
    if blockchain == ETHEREUM:
        return STKAAVE_ETH


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_reserves_tokens
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_reserves_tokens(pdp_contract, block):
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

        if decimals is True:
            token_decimals = get_decimals(reserves_token, blockchain, web3=web3)
        else:
            token_decimals = 0

        # balance = currentATokenBalance - currentStableDebt - currentVariableDebt
        balance = (user_reserve_data[0] - user_reserve_data[1] - user_reserve_data[2]) / 10 ** token_decimals

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
def get_data(wallet, block, blockchain, execution=1, web3=None, index=0, decimals=True):
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

    aave_data = {}
    collaterals = []
    debts = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lpapr_address = get_lpapr_address(blockchain)
        lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

        lending_pool_address = lpapr_contract.functions.getLendingPool().call()
        lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL,
                                             block=block)

        chainlink_eth_usd_contract = get_contract(CHAINLINK_ETH_USD, blockchain, web3=web3, abi=ABI_CHAINLINK_ETH_USD,
                                                  block=block)
        chainlink_eth_usd_decimals = chainlink_eth_usd_contract.functions.decimals().call()
        eth_usd_price = chainlink_eth_usd_contract.functions.latestAnswer().call(block_identifier=block) / (
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
                    block_identifier=block) / (10 ** 18) * eth_usd_price

                if balance[1] < 0:
                    debts.append(asset)
                else:
                    collaterals.append(asset)

        # getUserAccountData return a list with the following data:
        # [0] = totalCollateralETH, [1] = totalDebtETH, [2] = availableBorrowsETH, [3] = currentLiquidationThreshold, [4] = ltv, [5] = healthFactor 
        user_account_data = lending_pool_contract.functions.getUserAccountData(wallet).call(block_identifier=block)

        # Collateral Ratio
        aave_data['collateral_ratio'] = (user_account_data[0] / user_account_data[1]) * 100

        # Liquidation Ratio
        aave_data['liquidation_ratio'] = (1 / user_account_data[3]) * 1000000

        # Ether price in USD
        aave_data['eth_price_usd'] = eth_usd_price

        # Collaterals Data
        aave_data['collaterals'] = collaterals

        # Debts Data
        aave_data['debts'] = debts

        return aave_data

    except GetNodeIndexError:
        return get_data(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except Exception as e:
        logger.exception(e)
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

        stkaave_address = get_stkaave_address(blockchain)
        if stkaave_address is None:
            return None

        stkaave_contract = get_contract(stkaave_address, blockchain, web3=web3, abi=ABI_STKAAVE, block=block)

        reward_token = stkaave_contract.functions.REWARD_TOKEN().call()

        if decimals is True:
            reward_token_decimals = get_decimals(reward_token, blockchain, web3=web3)
        else:
            reward_token_decimals = 0

        reward_balance = stkaave_contract.functions.getTotalRewardsBalance(wallet).call(block_identifier=block) / (
                    10 ** reward_token_decimals)

        all_rewards.append([reward_token, reward_balance])

        return all_rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except Exception as e:
        logger.exception(e)
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

    except Exception as e:
        logger.exception(e)
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

    except Exception as e:
        logger.exception(e)
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
        stk_aave_address = get_stkaave_address(blockchain)
        stkaave_contract = get_contract(stk_aave_address, blockchain, web3=web3, abi=ABI_STKAAVE, block=block)
        emission_per_second = stkaave_contract.functions.assets(stk_aave_address).call(block_identifier=block)[0]
        aave_token_address = stkaave_contract.functions.REWARD_TOKEN().call()
        current_stakes = balance_of(stk_aave_address, aave_token_address, block, blockchain, web3=web3, decimals=False)

        staking_apr = emission_per_second * seconds_per_year / current_stakes

        if apy is False:
            return [{'metric': 'apr', 'type': 'staking', 'value': staking_apr}]
        else:
            staking_apy = ((1 + (staking_apr / seconds_per_year)) ** seconds_per_year) - 1

            return [{'metric': 'apy', 'type': 'staking', 'value': staking_apy}]

    except GetNodeIndexError:
        return get_staking_apr(block, blockchain, apy=apy, index=0, execution=execution + 1)

    except Exception as e:
        logger.exception(e)
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

        aave_wallet = web3.to_checksum_address(wallet)

        stk_aave_address = get_stkaave_address(blockchain)
        stkaave_contract = get_contract(stk_aave_address, blockchain, web3=web3, abi=ABI_STKAAVE, block=block)
        stkaave_balance = stkaave_contract.functions.balanceOf(aave_wallet).call(block_identifier=block)
        stkaave_decimals = stkaave_contract.functions.decimals().call()

        stkabpt_contract = get_contract(STAKED_ABPT_TOKEN, blockchain, web3=web3, abi=ABI_STKAAVE, block=block)
        stkabpt_balance = stkabpt_contract.functions.balanceOf(aave_wallet).call(block_identifier=block)
        stkabpt_decimals = stkabpt_contract.functions.decimals().call()

        if decimals:
            stkabpt_balance = stkabpt_balance / 10 ** stkabpt_decimals
            stkaave_balance = stkaave_balance / 10 ** stkaave_decimals
        
        balances.append([stk_aave_address,stkaave_balance])
        balances.append([STAKED_ABPT_TOKEN,stkabpt_balance])

        return balances


    except GetNodeIndexError:
        return get_staked(wallet, block, blockchain, web3=web3, index=0, execution=execution + 1)

    except Exception as e:
        logger.exception(e)
    except:
        return get_staked(wallet, block, blockchain, web3=web3, index=index + 1, execution=execution)

