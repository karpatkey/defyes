import logging
from decimal import Decimal
from typing import List, Union

from web3 import Web3
from web3.exceptions import ContractLogicError

from defyes.cache import const_call
from defyes.constants import AAVE_ETH, ABPT_ETH, ETHEREUM, STKAAVE_ETH
from defyes.functions import balance_of, get_contract, get_node, to_token_amount

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROTOCOL DATA PROVIDER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Protocol Data Provider - Ethereum
PDP_ETHEREUM = "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LENDING POOL ADDRESSES PROVIDER REGISTRY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Lending Pool Addresses Provider Registry - Ethereum
LPAPR_ETHEREUM = "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STAKED ABPT TOKEN
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
STAKED_ABPT_TOKEN = "0xa1116930326D21fB917d5A27F1E9943A9595fb47"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHAINLINK PRICE FEEDS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETHEREUM
# ETH/USD Price Feed
CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"

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
def get_reserves_tokens_balances(
    web3: Web3, wallet: str, block: int | str, blockchain: str, decimals: bool = True
) -> List:
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
    if pdp_address:
        pdp_contract = get_contract(pdp_address, blockchain, web3=web3, abi=ABI_PDP, block=block)
        reserves_tokens = get_reserves_tokens(pdp_contract, block)

        for reserves_token in reserves_tokens:
            try:
                user_reserve_data = pdp_contract.functions.getUserReserveData(reserves_token, wallet).call(
                    block_identifier=block
                )
            except ContractLogicError:
                continue

            # balance = currentATokenBalance - currentStableDebt - currentVariableDebt
            balance = Decimal(user_reserve_data[0] - user_reserve_data[1] - user_reserve_data[2])

            if balance != 0:
                balances.append([reserves_token, to_token_amount(reserves_token, balance, blockchain, web3, decimals)])

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_data(wallet, block, blockchain, web3=None, decimals=True):
    """
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    aave_data = {}
    collaterals = []
    debts = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lpapr_address = get_lpapr_address(blockchain)
    lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

    lending_pool_address = const_call(lpapr_contract.functions.getLendingPool())
    lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL, block=block)

    chainlink_eth_usd_contract = get_contract(
        CHAINLINK_ETH_USD, blockchain, web3=web3, abi=ABI_CHAINLINK_ETH_USD, block=block
    )
    chainlink_eth_usd_decimals = const_call(chainlink_eth_usd_contract.functions.decimals())
    eth_usd_price = chainlink_eth_usd_contract.functions.latestAnswer().call(block_identifier=block) / Decimal(
        10**chainlink_eth_usd_decimals
    )
    balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)

    if balances:
        price_oracle_address = lpapr_contract.functions.getPriceOracle().call(block_identifier=block)
        price_oracle_contract = get_contract(
            price_oracle_address, blockchain, web3=web3, abi=ABI_PRICE_ORACLE, block=block
        )

        for balance in balances:
            asset = {"token_address": balance[0], "token_amount": abs(balance[1])}

            asset["token_price_usd"] = (
                price_oracle_contract.functions.getAssetPrice(asset["token_address"]).call(block_identifier=block)
                / Decimal(10**18)
                * eth_usd_price
            )

            if balance[1] < 0:
                debts.append(asset)
            else:
                collaterals.append(asset)

    # getUserAccountData return a list with the following data:
    # [0] = totalCollateralETH,
    # [1] = totalDebtETH,
    # [2] = availableBorrowsETH,
    # [3] = currentLiquidationThreshold,
    # [4] = ltv,
    # [5] = healthFactor
    user_account_data = lending_pool_contract.functions.getUserAccountData(wallet).call(block_identifier=block)

    total_collateral_ETH, total_debt_ETH, _, current_liquidation_th, *_ = user_account_data

    if total_collateral_ETH > 0:
        if total_debt_ETH > 0:
            aave_data["collateral_ratio"] = Decimal(100 * total_collateral_ETH / total_debt_ETH)
        else:
            aave_data["collateral_ratio"] = Decimal("infinity")
    else:
        aave_data["collateral_ratio"] = Decimal("nan")

    if current_liquidation_th > 0:
        aave_data["liquidation_ratio"] = 1000000 / Decimal(current_liquidation_th)
    else:
        aave_data["liquidation_ratio"] = Decimal("infinity")

    # Ether price in USD
    aave_data["eth_price_usd"] = eth_usd_price

    # Collaterals Data
    aave_data["collaterals"] = collaterals

    # Debts Data
    aave_data["debts"] = debts

    return aave_data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, block, blockchain, web3=None, decimals=True):
    """
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    stkaave_address = get_stkaave_address(blockchain)
    if stkaave_address:
        stkaave_contract = get_contract(stkaave_address, blockchain, web3=web3, abi=ABI_STKAAVE, block=block)

        reward_token = const_call(stkaave_contract.functions.REWARD_TOKEN())
        reward_balance = stkaave_contract.functions.getTotalRewardsBalance(wallet).call(block_identifier=block)

        all_rewards.append([reward_token, to_token_amount(reward_token, reward_balance, blockchain, web3, decimals)])

    return all_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance], where balance = currentATokenBalance - currentStableDebt - currentStableDebt
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying_all(wallet, block, blockchain, web3=None, decimals=True, reward=False):
    """
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param reward:
    :return:
    """
    result = []
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)
    if balances:
        if reward:
            all_rewards = get_all_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)

            result.append(balances)
            result.append(all_rewards)
        else:
            result = balances

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_apr
# 'web3' = web3 (Node) -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
#             {'metric': 'apr'/'apy', 'type': 'variable_borrow', 'value': borrow_apr/borrow_apy},
#             {'metric': 'apr'/'apy', 'type': 'stable_borrow', 'value': borrow_apr/borrow_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_apr(token_address, block, blockchain, web3=None, apy=False):
    """
    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param apy:
    :return:
    """

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lpapr_address = get_lpapr_address(blockchain)
    lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

    lending_pool_address = const_call(lpapr_contract.functions.getLendingPool())
    lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL, block=block)

    reserve_data = lending_pool_contract.functions.getReserveData(token_address).call(block_identifier=block)

    liquidity_rate = reserve_data[3]
    variable_borrow_rate = reserve_data[4]
    stable_borrow_rate = reserve_data[5]

    ray = Decimal(10**27)
    seconds_per_year = 31536000

    deposit_apr = liquidity_rate / ray
    variable_borrow_apr = variable_borrow_rate / ray
    stable_borrow_apr = stable_borrow_rate / ray

    if apy is False:
        return [
            {"metric": "apr", "type": "supply", "value": deposit_apr},
            {"metric": "apr", "type": "variable_borrow", "value": variable_borrow_apr},
            {"metric": "apr", "type": "stable_borrow", "value": stable_borrow_apr},
        ]
    else:
        deposit_apy = ((1 + (deposit_apr / seconds_per_year)) ** seconds_per_year) - 1
        variable_borrow_apy = ((1 + (variable_borrow_apr / seconds_per_year)) ** seconds_per_year) - 1
        stable_borrow_apy = ((1 + (stable_borrow_apr / seconds_per_year)) ** seconds_per_year) - 1

        return [
            {"metric": "apy", "type": "supply", "value": deposit_apy},
            {"metric": "apy", "type": "variable_borrow", "value": variable_borrow_apy},
            {"metric": "apy", "type": "stable_borrow", "value": stable_borrow_apy},
        ]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staking_apr
# 'web3' = web3 (Node) -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'staking', 'value': staking_apr/staking_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staking_apr(block, blockchain, web3=None, apy=False):
    """
    :param block:
    :param blockchain:
    :param web3:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    seconds_per_year = 31536000
    stk_aave_address = get_stkaave_address(blockchain)
    stkaave_contract = get_contract(stk_aave_address, blockchain, web3=web3, abi=ABI_STKAAVE, block=block)
    aave_token_address = const_call(stkaave_contract.functions.REWARD_TOKEN())
    current_stakes = balance_of(stk_aave_address, aave_token_address, block, blockchain, web3=web3, decimals=False)

    emission_per_second = stkaave_contract.functions.assets(stk_aave_address).call(block_identifier=block)[0]

    staking_apr = emission_per_second * seconds_per_year / current_stakes

    if apy is False:
        return [{"metric": "apr", "type": "staking", "value": staking_apr}]
    else:
        staking_apy = ((1 + (staking_apr / seconds_per_year)) ** seconds_per_year) - 1

        return [{"metric": "apy", "type": "staking", "value": staking_apy}]


def get_staked(
    wallet: str, block: Union[int, str], blockchain: str, stkaave: bool = False, web3=None, decimals: bool = True
) -> list:
    """
    :param block:
    :param blockchain:
    :param web3:
    :return:
    """

    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    aave_wallet = Web3.to_checksum_address(wallet)

    stkabpt_balance = balance_of(aave_wallet, STAKED_ABPT_TOKEN, block, blockchain, web3, decimals)

    stk_aave_address = get_stkaave_address(blockchain)
    stkaave_balance = balance_of(aave_wallet, stk_aave_address, block, blockchain, web3, decimals)

    if stkaave:
        balances.append([STKAAVE_ETH, stkaave_balance])
        balances.append([STAKED_ABPT_TOKEN, stkabpt_balance])
    else:
        balances.append([AAVE_ETH, stkaave_balance])
        balances.append([ABPT_ETH, stkabpt_balance])

    return balances
