import logging
from collections import defaultdict
from decimal import Decimal
from typing import List

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import ContractLogicError

from defyes.functions import balance_of, get_contract, get_contract_proxy_abi, to_token_amount

logger = logging.getLogger(__name__)

PROTOCOL_DATA_PROVIDER = {
    Chain.ETHEREUM: "0x057835Ad21a177dbdd3090bB1CAE03EaCF78Fc6d",
    Chain.POLYGON: "0x7551b5D2763519d4e37e8B81929D336De671d46d",
    Chain.AVALANCHE: "0x65285E9dfab318f57051ab2b139ccCf232945451",
}

POOL_ADDRESSES_PROVIDER = {
    Chain.ETHEREUM: "0xB53C1a33016B2DC2fF3653530bfF1848a515c8c5",
    Chain.POLYGON: "0xd05e3E715d945B59290df0ae8eF85c1BdB684744",
    Chain.AVALANCHE: "0xb6A86025F0FE1862B372cb0ca18CE3EDe02A318f",
}

CHAINLINK_NATIVE_USD = {
    Chain.ETHEREUM: "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
    Chain.POLYGON: "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0",
    Chain.AVALANCHE: "0x0A77230d17318075983913bC2145DB16C7366156",
}

STAKED_ABPT_TOKEN = "0xa1116930326D21fB917d5A27F1E9943A9595fb47"

# Contracts to get the unclaimed rewards of stkAAVE
INCETIVES_CONTROLLER = "0xd784927Ff2f95ba542BfC824c8a8a98F3495f6b5"
PROXY_INCENTIVES_CONTROLLER = "0xD9ED413bCF58c266F95fE6BA63B13cf79299CE31"

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


def get_stkaave_address(blockchain):
    if blockchain == Chain.ETHEREUM:
        return EthereumTokenAddr.STKAAVE


def get_incentives_controller_contract(blockchain):
    """This contract has the same functions of the stAAVE one.
    Apparently is the contract that is now used to get the rewards."""
    if blockchain == Chain.ETHEREUM:
        return INCETIVES_CONTROLLER, PROXY_INCENTIVES_CONTROLLER
    else:
        raise ValueError(f"Blockchain {blockchain} is not yet available.")


def get_stkabpt_address(blockchain):
    if blockchain == Chain.ETHEREUM:
        return STAKED_ABPT_TOKEN


def get_reserves_tokens(pdp_contract, block):
    reserves_tokens_addresses = []

    reserves_tokens = pdp_contract.functions.getAllReservesTokens().call(block_identifier=block)

    for reserves_token in reserves_tokens:
        reserves_tokens_addresses.append(reserves_token[1])

    return reserves_tokens_addresses


def get_reserves_tokens_balances(
    web3: Web3, wallet: str, block: int | str, blockchain: str, decimals: bool = True
) -> List:
    balances = []

    pdp_address = PROTOCOL_DATA_PROVIDER[blockchain]
    if pdp_address:
        pdp_contract = get_contract(pdp_address, blockchain, web3=web3, abi=ABI_PDP)
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


def get_data(wallet, block, blockchain, web3=None, decimals=True):
    aave_data = {}
    collaterals = []
    debts = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lpapr_address = POOL_ADDRESSES_PROVIDER[blockchain]
    lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR)

    lending_pool_address = const_call(lpapr_contract.functions.getLendingPool())
    lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL)

    chainlink_eth_usd_contract = get_contract(
        CHAINLINK_NATIVE_USD[blockchain], blockchain, web3=web3, abi=ABI_CHAINLINK_ETH_USD
    )
    chainlink_eth_usd_decimals = const_call(chainlink_eth_usd_contract.functions.decimals())
    eth_usd_price = chainlink_eth_usd_contract.functions.latestAnswer().call(block_identifier=block) / Decimal(
        10**chainlink_eth_usd_decimals
    )
    balances = get_reserves_tokens_balances(web3, wallet, block, blockchain, decimals=decimals)

    if balances:
        price_oracle_address = lpapr_contract.functions.getPriceOracle().call(block_identifier=block)
        price_oracle_contract = get_contract(price_oracle_address, blockchain, web3=web3, abi=ABI_PRICE_ORACLE)

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


def get_all_rewards(wallet, block, blockchain, web3=None, decimals=True):
    """Function to get all the rewards of the user.
    As this is an old version of aave (v2). The rewards are now retrevied from another contract. (for mainnet at least)
    """
    rewards = defaultdict(list)

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    for stk_address in [
        get_incentives_controller_contract(blockchain),
        get_stkabpt_address(blockchain),
        get_stkaave_address(blockchain),
    ]:
        if stk_address:
            if isinstance(stk_address, tuple):
                contract = get_contract_proxy_abi(stk_address[0], stk_address[1], blockchain, web3=web3)
                reward_balance = contract.functions.getUserUnclaimedRewards(wallet).call(block_identifier=block)
            else:
                contract = get_contract(stk_address, blockchain, web3=web3, abi=ABI_STKAAVE)
                reward_balance = contract.functions.getTotalRewardsBalance(wallet).call(block_identifier=block)

            reward_token = const_call(contract.functions.REWARD_TOKEN())
            # Just cast it to AAVE in case is stkAAVE
            reward_token = EthereumTokenAddr.AAVE if reward_token == EthereumTokenAddr.stkAAVE else reward_token
            rewards[reward_token].append(to_token_amount(reward_token, reward_balance, blockchain, web3, decimals))

    all_rewards = [[token, sum(amounts)] for token, amounts in rewards.items()]
    return all_rewards


def underlying_all(wallet, block, blockchain, web3=None, decimals=True, reward=False):
    """Get all the underlying tokens of your position.

    Args:
        reward (bool, optional): True if you want to get also the reward. Defaults to False.

    Returns:
        List: [token_address, balance], where balance = currentATokenBalance - currentStableDebt - currentStableDebt
              [reward_token_address, balance]
    """
    result = []
    if web3 is None:
        web3 = get_node(blockchain)

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


def get_apr(token_address, block, blockchain, web3=None, apy=False):
    """Get APR for a token

    Args:
        token_address (str):
        apy (bool, optional): if True returns APY else APR. Defaults to False.

    Returns:
        Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
             {'metric': 'apr'/'apy', 'type': 'variable_borrow', 'value': borrow_apr/borrow_apy},
             {'metric': 'apr'/'apy', 'type': 'stable_borrow', 'value': borrow_apr/borrow_apy}]
    """

    if web3 is None:
        web3 = get_node(blockchain)

    lpapr_address = POOL_ADDRESSES_PROVIDER[blockchain]
    lpapr_contract = get_contract(lpapr_address, blockchain, web3=web3, abi=ABI_LPAPR)

    lending_pool_address = const_call(lpapr_contract.functions.getLendingPool())
    lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL)

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


def get_staking_apr(block, blockchain, web3=None, apy=False):
    """Get staking APR.

    Args:
        apy (bool, optional): if True returns APY else APR. Defaults to False.

    Returns:
        :  [{'metric': 'apr'/'apy', 'type': 'staking', 'value': staking_apr/staking_apy}]
    """
    if web3 is None:
        web3 = get_node(blockchain)

    seconds_per_year = 31536000
    stk_aave_address = get_stkaave_address(blockchain)
    stkaave_contract = get_contract(stk_aave_address, blockchain, web3=web3, abi=ABI_STKAAVE)
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
    wallet: str, block: int | str, blockchain: str, stkaave: bool = False, web3=None, decimals: bool = True
) -> list:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    aave_wallet = Web3.to_checksum_address(wallet)

    stkabpt_balance = balance_of(aave_wallet, STAKED_ABPT_TOKEN, block, blockchain, web3, decimals)

    stk_aave_address = get_stkaave_address(blockchain)
    stkaave_balance = balance_of(aave_wallet, stk_aave_address, block, blockchain, web3, decimals)

    if stkaave:
        balances.append([EthereumTokenAddr.STKAAVE, stkaave_balance])
        balances.append([STAKED_ABPT_TOKEN, stkabpt_balance])
    else:
        balances.append([EthereumTokenAddr.AAVE, stkaave_balance])
        balances.append([EthereumTokenAddr.ABPT, stkabpt_balance])

    return balances
