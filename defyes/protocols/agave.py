"""
Agave is the DeFi lending protocol on Gnosis.

Agave rewards depositors with passive income
and lets them use their deposits as collateral
to borrow and lend digital assets.

Agave is a fork of Aave, built by the
1Hive community and deployed on the Gnosis chain
"""

import logging
from decimal import Decimal
from typing import Dict, List, Union

from defabipedia.tokens import GnosisTokenAddr
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import balance_of, get_contract, to_token_amount

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROTOCOL DATA PROVIDER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Protocol Data Provider - GNOSIS
# PDP_GNOSIS = '0x75e5cF901f3A576F72AB6bCbcf7d81F1619C6a12'
PDP_GNOSIS = "0x24dCbd376Db23e4771375092344f5CbEA3541FC0"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LENDING POOL ADDRESSES PROVIDER REGISTRY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Lending Pool Addresses Provider Registry - GNOSIS
LPAPR_GNOSIS = "0x3673C22153E363B1da69732c4E0aA71872Bbb87F"
# 0x5E15d5E33d318dCEd84Bfe3F4EACe07909bE6d9c

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EXTRA REWARDER CONTRACT
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rewarder contract - GNOSIS
REWARDER_ADDRESS = "0xfa255f5104f129B78f477e9a6D050a02f31A5D86"


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHAINLINK PRICE FEEDS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GNOSIS
# XDAI/USD Price Feed
CHAINLINK_XDAI_USD = "0x678df3415fc31947dA4324eC63212874be5a82f8"


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

REWARDER_ABI = '[{"inputs":[{"internalType":"contract IERC20","name":"rewardToken","type":"address"},{"internalType":"address","name":"emissionManager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":false,"internalType":"uint8","name":"decimals","type":"uint8"},{"indexed":false,"internalType":"uint256","name":"emission","type":"uint256"}],"name":"AssetConfigUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"}],"name":"AssetIndexUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"newBulkClaimer","type":"address"}],"name":"BulkClaimerUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"claimer","type":"address"}],"name":"ClaimerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"newDistributionEnd","type":"uint256"}],"name":"DistributionEndUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token","type":"address"}],"name":"RewardTokenUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardsAccrued","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"address","name":"claimer","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardsClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"vault","type":"address"}],"name":"RewardsVaultUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":false,"internalType":"uint256","name":"index","type":"uint256"}],"name":"UserIndexUpdated","type":"event"},{"inputs":[],"name":"BULK_CLAIMER","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DISTRIBUTION_END","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"EMISSION_MANAGER","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PRECISION","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PROXY_ADMIN","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REWARD_TOKEN","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"assets","outputs":[{"internalType":"uint104","name":"emissionPerSecond","type":"uint104"},{"internalType":"uint104","name":"index","type":"uint104"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"uint8","name":"decimals","type":"uint8"},{"internalType":"bool","name":"disabled","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"to","type":"address"}],"name":"bulkClaimRewardsOnBehalf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"}],"name":"claimRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"to","type":"address"}],"name":"claimRewardsOnBehalf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256[]","name":"emissionsPerSecond","type":"uint256[]"},{"internalType":"uint256[]","name":"assetDecimals","type":"uint256[]"}],"name":"configureAssets","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"}],"name":"disableAssets","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetData","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint8","name":"","type":"uint8"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getClaimer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getDistributionEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address","name":"user","type":"address"}],"name":"getRewardsBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRewardsVault","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"asset","type":"address"}],"name":"getUserAssetData","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_user","type":"address"}],"name":"getUserUnclaimedRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"totalSupply","type":"uint256"},{"internalType":"uint256","name":"userBalance","type":"uint256"}],"name":"handleAction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"rewardsVault","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"newRewardTokenAdjustmentAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"newRewardTokenAdjustmentMultiplier","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"bulkClaimer","type":"address"}],"name":"setBulkClaimer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"caller","type":"address"}],"name":"setClaimer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"distributionEnd","type":"uint256"}],"name":"setDistributionEnd","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"rewardToken","type":"address"}],"name":"setRewardToken","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"RewardTokenAdjustmentMultiplier","type":"bool"},{"internalType":"uint256","name":"RewardTokenAdjustmentAmount","type":"uint256"}],"name":"setRewardTokenAdjustment","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"rewardsVault","type":"address"}],"name":"setRewardsVault","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


def get_reserves_tokens(pdp_contract, block: Union[int, str]) -> List[str]:
    rt = pdp_contract.functions.getAllReservesTokens().call(block_identifier=block)
    return [e[1] for e in rt]


def get_reserves_tokens_balances(
    web3, wallet: str, block: Union[int, str], blockchain: str, decimals: bool = True
) -> List[List]:
    balances = []

    pdp_contract = get_contract(PDP_GNOSIS, blockchain, web3=web3, abi=ABI_PDP, block=block)
    reserves_tokens = get_reserves_tokens(pdp_contract, block)
    cs_wallet = Web3.to_checksum_address(wallet)

    for token in reserves_tokens:
        user_reserve_data = pdp_contract.functions.getUserReserveData(token, cs_wallet).call(block_identifier=block)
        currentATokenBalance, currentStableDebt, currentVariableDebt, *_ = user_reserve_data
        balance = currentATokenBalance - currentStableDebt - currentVariableDebt

        if balance != 0:
            balances.append([token, to_token_amount(token, balance, blockchain, web3, decimals)])

    return balances


def get_data(wallet: str, block: Union[int, str], blockchain: str, web3=None, decimals: bool = True) -> Dict:
    agave_data = {}
    collaterals = []
    debts = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lpapr_contract = get_contract(LPAPR_GNOSIS, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

    lending_pool_address = const_call(lpapr_contract.functions.getLendingPool())
    lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL, block=block)

    chainlink_eth_usd_contract = get_contract(
        CHAINLINK_XDAI_USD, blockchain, web3=web3, abi=ABI_CHAINLINK_XDAI_USD, block=block
    )
    chainlink_eth_usd_decimals = const_call(chainlink_eth_usd_contract.functions.decimals())
    xdai_usd_price = chainlink_eth_usd_contract.functions.latestAnswer().call(block_identifier=block)
    xdai_usd_price = Decimal(xdai_usd_price) / Decimal(10**chainlink_eth_usd_decimals)

    balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)

    if balances:
        price_oracle_address = lpapr_contract.functions.getPriceOracle().call(block_identifier=block)
        price_oracle_contract = get_contract(
            price_oracle_address, blockchain, web3=web3, abi=ABI_PRICE_ORACLE, block=block
        )

        for balance in balances:
            asset = {"token_address": balance[0], "token_amount": abs(balance[1])}

            token_price_usd = price_oracle_contract.functions.getAssetPrice(asset["token_address"]).call(
                block_identifier=block
            )
            asset["token_price_usd"] = Decimal(token_price_usd) / Decimal(10**18) * xdai_usd_price

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
            agave_data["collateral_ratio"] = 100 * total_collateral_ETH / Decimal(total_debt_ETH)
        else:
            agave_data["collateral_ratio"] = Decimal("infinity")
    else:
        agave_data["collateral_ratio"] = Decimal("nan")

    if current_liquidation_th > 0:
        agave_data["liquidation_ratio"] = 1000000 / Decimal(current_liquidation_th)
    else:
        agave_data["liquidation_ratio"] = Decimal("infinity")

    # Ether price in USD
    agave_data["xdai_price_usd"] = xdai_usd_price

    # Collaterals Data
    agave_data["collaterals"] = collaterals

    # Debts Data
    agave_data["debts"] = debts

    return agave_data


def get_all_rewards(
    wallet: str, block: Union[int, str], blockchain: str, web3=None, decimals: bool = True
) -> List[List]:
    """
    Output: List of 2-element lists: [[reward_token_1_address, balance_1], [t2, b2], ... ]
    """

    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    stkagave_contract = get_contract(GnosisTokenAddr.STKAGAVE, blockchain, web3=web3, abi=ABI_STKAGAVE, block=block)

    reward_token = const_call(stkagave_contract.functions.REWARD_TOKEN())

    reward_balance = stkagave_contract.functions.getTotalRewardsBalance(wallet).call(block_identifier=block)

    all_rewards.append([reward_token, to_token_amount(reward_token, reward_balance, blockchain, web3, decimals)])

    return all_rewards


def underlying_all(
    wallet: str, block: Union[int, str], blockchain: str, web3=None, decimals: bool = True, reward: bool = False
) -> List[List]:
    """
    Output: a list of 2-element lists: [[token_1_address, balance_1], [t2, b2], ... ].
    """

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)

    result = balances
    if reward:
        all_rewards = get_all_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)
        result.extend(all_rewards)

    return result


def get_apr(token_address: str, block: Union[int, str], blockchain: str, web3=None, apy: bool = False) -> List[Dict]:
    """
    Output:
        [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
         {'metric': 'apr'/'apy', 'type': 'variable_borrow', 'value': borrow_apr/borrow_apy},
         {'metric': 'apr'/'apy', 'type': 'stable_borrow', 'value': borrow_apr/borrow_apy}]
    """

    if web3 is None:
        web3 = get_node(blockchain)

    lpapr_contract = get_contract(LPAPR_GNOSIS, blockchain, web3=web3, abi=ABI_LPAPR, block=block)

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

    if not apy:
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


def get_staking_apr(block: Union[int, str], blockchain: str, web3=None, apy: bool = False) -> List[Dict]:
    if web3 is None:
        web3 = get_node(blockchain)

    seconds_per_year = 365 * 24 * 60 * 60

    stkagave_contract = get_contract(GnosisTokenAddr.STKAGAVE, blockchain, web3=web3, abi=ABI_STKAGAVE, block=block)
    emission_per_second = stkagave_contract.functions.assets(GnosisTokenAddr.STKAGAVE).call(block_identifier=block)[0]
    agave_token_address = const_call(stkagave_contract.functions.REWARD_TOKEN())
    current_stakes = balance_of(
        GnosisTokenAddr.STKAGAVE, agave_token_address, block, blockchain, web3=web3, decimals=False
    )

    staking_apr = emission_per_second * seconds_per_year / current_stakes
    staking_apy = ((1 + (staking_apr / seconds_per_year)) ** seconds_per_year) - 1

    return [{"metric": "apy" if apy else "apr", "type": "staking", "value": staking_apy if apy else staking_apr}]


def get_staked(
    wallet: str, block: Union[int, str], blockchain: str, stkagve: bool = False, web3=None, decimals: bool = True
) -> List[List]:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    agave_wallet = Web3.to_checksum_address(wallet)

    stkagave_contract = get_contract(GnosisTokenAddr.STKAGAVE, blockchain, web3=web3, abi=ABI_STKAGAVE, block=block)
    stkagave_balance = stkagave_contract.functions.balanceOf(agave_wallet).call(block_identifier=block)

    stkagave_balance = to_token_amount(GnosisTokenAddr.STKAGAVE, stkagave_balance, blockchain, web3, decimals)

    if stkagve:
        balances.append([GnosisTokenAddr.STKAGAVE, stkagave_balance])
    else:
        balances.append([GnosisTokenAddr.AGVE, stkagave_balance])

    return balances


def get_agave_tokens(blockchain: str, block: int | str, web3: Web3 = None) -> dict:
    if web3 is None:
        web3 = get_node(blockchain)

    pdp_contract = get_contract(PDP_GNOSIS, blockchain, web3=web3, abi=ABI_PDP, block=block)
    reserve_tokens = pdp_contract.functions.getAllReservesTokens().call(block_identifier=block)
    agave_tokens = []
    for token in reserve_tokens:
        data = pdp_contract.functions.getReserveTokensAddresses(token[1]).call(block_identifier=block)
        agave_tokens.append(
            {"underlying": token[1], "interest bearing": data[0], "stable debt": data[1], "variable debt": data[2]}
        )
    return agave_tokens


def get_extra_rewards(
    wallet: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True
) -> List[List]:
    if web3 is None:
        web3 = get_node(blockchain)

    rewarder_contract = web3.eth.contract(address=REWARDER_ADDRESS, abi=REWARDER_ABI)
    token_address = rewarder_contract.functions.REWARD_TOKEN().call(block_identifier=block)

    agave_tokens = get_agave_tokens(blockchain, block, web3=web3)

    tokens_accruing_rewards = []
    for element in agave_tokens:
        tokens_accruing_rewards = tokens_accruing_rewards + [element["interest bearing"], element["variable debt"]]

    amount = rewarder_contract.functions.getRewardsBalance(tokens_accruing_rewards, wallet).call(block_identifier=block)
    return [[token_address, to_token_amount(token_address, amount, blockchain, web3=web3, decimals=decimals)]]
