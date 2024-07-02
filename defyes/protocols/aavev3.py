import logging
from decimal import Decimal
from typing import List

from defabipedia import Chain
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import ContractLogicError

from defyes.functions import get_contract, last_block, to_token_amount

logger = logging.getLogger(__name__)

PROTOCOL_DATA_PROVIDER = {
    Chain.ETHEREUM: "0x7B4EB56E7CD4b454BA8ff71E4518426369a138a3",
    Chain.OPTIMISM: "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    Chain.ARBITRUM: "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    Chain.POLYGON: "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    Chain.FANTOM: "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    Chain.AVALANCHE: "0x69FA688f1Dc47d4B5d8029D5a35FB7a548310654",
    Chain.GNOSIS: "0x501B4c19dd9C2e06E94dA7b6D5Ed4ddA013EC741",
    Chain.BASE: "0x2d8A3C5677189723C4cB8873CfC9C8976FDF38Ac",
    Chain.METIS: "0x99411FC17Ad1B56f49719E3850B2CDcc0f9bBFd8",
}

POOL_ADDRESSES_PROVIDER = {
    Chain.ETHEREUM: "0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e",
    Chain.OPTIMISM: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    Chain.ARBITRUM: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    Chain.POLYGON: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    Chain.FANTOM: "0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb",
    Chain.AVALANCHE: "0x770ef9f4fe897e59daCc474EF11238303F9552b6",
    Chain.GNOSIS: "0x36616cf17557639614c1cdDb356b1B83fc0B2132",
    Chain.BASE: "0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D",
    Chain.METIS: "0xB9FABd7500B2C6781c35Dd48d54f81fc2299D7AF",
}

CHAINLINK_NATIVE_USD = {
    Chain.ETHEREUM: "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
    Chain.OPTIMISM: "0x13e3Ee699D1909E989722E753853AE30b17e08c5",
    Chain.ARBITRUM: "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612",
    Chain.POLYGON: "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0",
    Chain.FANTOM: "0xf4766552D15AE4d256Ad41B6cf2933482B0680dc",
    Chain.AVALANCHE: "0x0A77230d17318075983913bC2145DB16C7366156",
    Chain.GNOSIS: "0x678df3415fc31947dA4324eC63212874be5a82f8",
    Chain.BASE: "0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70",
    Chain.METIS: "0xD4a5Bb03B5D66d9bf81507379302Ac2C2DFDFa6D",
}

# These are the contracts used to manage all rewards : https://docs.aave.com/developers/periphery-contracts/rewardscontroller
REWARDS_CONTROLLER = {
    Chain.ETHEREUM: "0x8164Cc65827dcFe994AB23944CBC90e0aa80bFcb",
    Chain.OPTIMISM: "0x929EC64c34a17401F460460D4B9390518E5B473e",
    Chain.ARBITRUM: "0x929EC64c34a17401F460460D4B9390518E5B473e",
    Chain.POLYGON: "0x929EC64c34a17401F460460D4B9390518E5B473e",
    Chain.FANTOM: "0x929EC64c34a17401F460460D4B9390518E5B473e",
    Chain.AVALANCHE: "0x929EC64c34a17401F460460D4B9390518E5B473e",
    Chain.GNOSIS: "0xaD4F91D26254B6B0C6346b390dDA2991FDE2F20d",
    Chain.BASE: "0xf9cc4F0D883F1a1eb2c253bdb46c254Ca51E1F44",
    Chain.METIS: "0x30C1b8F0490fa0908863d6Cbd2E36400b4310A6B",
}

# ETH/USD Price Feed
CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"

# Protocol Data Provider ABI - getAllReservesTokens, getUserReserveData, getReserveConfigurationData, getReserveTokensAddresses
ABI_PDP = '[{"inputs":[],"name":"getAllReservesTokens","outputs":[{"components":[{"internalType":"string","name":"symbol","type":"string"},{"internalType":"address","name":"tokenAddress","type":"address"}],"internalType":"struct AaveProtocolDataProvider.TokenData[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"getUserReserveData","outputs":[{"internalType":"uint256","name":"currentATokenBalance","type":"uint256"},{"internalType":"uint256","name":"currentStableDebt","type":"uint256"},{"internalType":"uint256","name":"currentVariableDebt","type":"uint256"},{"internalType":"uint256","name":"principalStableDebt","type":"uint256"},{"internalType":"uint256","name":"scaledVariableDebt","type":"uint256"},{"internalType":"uint256","name":"stableBorrowRate","type":"uint256"},{"internalType":"uint256","name":"liquidityRate","type":"uint256"},{"internalType":"uint40","name":"stableRateLastUpdated","type":"uint40"},{"internalType":"bool","name":"usageAsCollateralEnabled","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveConfigurationData","outputs":[{"internalType":"uint256","name":"decimals","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"liquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"liquidationBonus","type":"uint256"},{"internalType":"uint256","name":"reserveFactor","type":"uint256"},{"internalType":"bool","name":"usageAsCollateralEnabled","type":"bool"},{"internalType":"bool","name":"borrowingEnabled","type":"bool"},{"internalType":"bool","name":"stableBorrowRateEnabled","type":"bool"},{"internalType":"bool","name":"isActive","type":"bool"},{"internalType":"bool","name":"isFrozen","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveTokensAddresses","outputs":[{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"}],"stateMutability":"view","type":"function"}]'

# Lending Pool Addresses Provider Registry ABI - getPool, getPriceOracle
ABI_LPAPR = '[{"inputs":[],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPriceOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# Lending Pool ABI - getUserAccountData, getReserveData
ABI_LENDING_POOL = '[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getUserAccountData","outputs":[{"internalType":"uint256","name":"totalCollateralETH","type":"uint256"},{"internalType":"uint256","name":"totalDebtETH","type":"uint256"},{"internalType":"uint256","name":"availableBorrowsETH","type":"uint256"},{"internalType":"uint256","name":"currentLiquidationThreshold","type":"uint256"},{"internalType":"uint256","name":"ltv","type":"uint256"},{"internalType":"uint256","name":"healthFactor","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getReserveData","outputs":[{"components":[{"components":[{"internalType":"uint256","name":"data","type":"uint256"}],"internalType":"struct DataTypes.ReserveConfigurationMap","name":"configuration","type":"tuple"},{"internalType":"uint128","name":"liquidityIndex","type":"uint128"},{"internalType":"uint128","name":"variableBorrowIndex","type":"uint128"},{"internalType":"uint128","name":"currentLiquidityRate","type":"uint128"},{"internalType":"uint128","name":"currentVariableBorrowRate","type":"uint128"},{"internalType":"uint128","name":"currentStableBorrowRate","type":"uint128"},{"internalType":"uint40","name":"lastUpdateTimestamp","type":"uint40"},{"internalType":"address","name":"aTokenAddress","type":"address"},{"internalType":"address","name":"stableDebtTokenAddress","type":"address"},{"internalType":"address","name":"variableDebtTokenAddress","type":"address"},{"internalType":"address","name":"interestRateStrategyAddress","type":"address"},{"internalType":"uint8","name":"id","type":"uint8"}],"internalType":"struct DataTypes.ReserveData","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]'

# ChainLink: ETH/USD Price Feed ABI - latestAnswer, decimals
ABI_CHAINLINK_ETH_USD = '[{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Price Oracle ABI - getAssetPrice, BASE_CURRENCY_UNIT
ABI_PRICE_ORACLE = '[{"inputs":[],"name":"BASE_CURRENCY_UNIT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Staked Aave ABI - REWARD_TOKEN, getTotalRewardsBalance, assets, balanceOf
ABI_STKAAVE = '[{"inputs":[],"name":"REWARD_TOKEN","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"staker","type":"address"}],"name":"getTotalRewardsBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"assets","outputs":[{"internalType":"uint128","name":"emissionPerSecond","type":"uint128"},{"internalType":"uint128","name":"lastUpdateTimestamp","type":"uint128"},{"internalType":"uint256","name":"index","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}]'

ABI_REWARDS_CONTROLLER = '[{"inputs":[{"internalType":"address","name":"emissionManager","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":true,"internalType":"address","name":"reward","type":"address"},{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint256","name":"assetIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"userIndex","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"rewardsAccrued","type":"uint256"}],"name":"Accrued","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"asset","type":"address"},{"indexed":true,"internalType":"address","name":"reward","type":"address"},{"indexed":false,"internalType":"uint256","name":"oldEmission","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newEmission","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"oldDistributionEnd","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"newDistributionEnd","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"assetIndex","type":"uint256"}],"name":"AssetConfigUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"claimer","type":"address"}],"name":"ClaimerSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"reward","type":"address"},{"indexed":true,"internalType":"address","name":"rewardOracle","type":"address"}],"name":"RewardOracleUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"user","type":"address"},{"indexed":true,"internalType":"address","name":"reward","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"address","name":"claimer","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardsClaimed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"reward","type":"address"},{"indexed":true,"internalType":"address","name":"transferStrategy","type":"address"}],"name":"TransferStrategyInstalled","type":"event"},{"inputs":[],"name":"EMISSION_MANAGER","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"REVISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address","name":"to","type":"address"}],"name":"claimAllRewards","outputs":[{"internalType":"address[]","name":"rewardsList","type":"address[]"},{"internalType":"uint256[]","name":"claimedAmounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"to","type":"address"}],"name":"claimAllRewardsOnBehalf","outputs":[{"internalType":"address[]","name":"rewardsList","type":"address[]"},{"internalType":"uint256[]","name":"claimedAmounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"}],"name":"claimAllRewardsToSelf","outputs":[{"internalType":"address[]","name":"rewardsList","type":"address[]"},{"internalType":"uint256[]","name":"claimedAmounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"claimRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"claimRewardsOnBehalf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"address","name":"reward","type":"address"}],"name":"claimRewardsToSelf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint88","name":"emissionPerSecond","type":"uint88"},{"internalType":"uint256","name":"totalSupply","type":"uint256"},{"internalType":"uint32","name":"distributionEnd","type":"uint32"},{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"reward","type":"address"},{"internalType":"contract ITransferStrategyBase","name":"transferStrategy","type":"address"},{"internalType":"contract IEACAggregatorProxy","name":"rewardOracle","type":"address"}],"internalType":"struct RewardsDataTypes.RewardsConfigInput[]","name":"config","type":"tuple[]"}],"name":"configureAssets","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address","name":"user","type":"address"}],"name":"getAllUserRewards","outputs":[{"internalType":"address[]","name":"rewardsList","type":"address[]"},{"internalType":"uint256[]","name":"unclaimedAmounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getAssetDecimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"getAssetIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getClaimer","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"getDistributionEnd","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getEmissionManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"reward","type":"address"}],"name":"getRewardOracle","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getRewardsByAsset","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"getRewardsData","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getRewardsList","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"reward","type":"address"}],"name":"getTransferStrategy","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"getUserAccruedRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"getUserAssetIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address[]","name":"assets","type":"address[]"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"reward","type":"address"}],"name":"getUserRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"totalSupply","type":"uint256"},{"internalType":"uint256","name":"userBalance","type":"uint256"}],"name":"handleAction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"caller","type":"address"}],"name":"setClaimer","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"reward","type":"address"},{"internalType":"uint32","name":"newDistributionEnd","type":"uint32"}],"name":"setDistributionEnd","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address[]","name":"rewards","type":"address[]"},{"internalType":"uint88[]","name":"newEmissionsPerSecond","type":"uint88[]"}],"name":"setEmissionPerSecond","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"reward","type":"address"},{"internalType":"contract IEACAggregatorProxy","name":"rewardOracle","type":"address"}],"name":"setRewardOracle","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"reward","type":"address"},{"internalType":"contract ITransferStrategyBase","name":"transferStrategy","type":"address"}],"name":"setTransferStrategy","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


def get_aave_v3_tokens(blockchain: str, block: int | str, web3: Web3 = None) -> dict:
    if web3 is None:
        web3 = get_node(blockchain)

    pdp_contract = get_contract(PROTOCOL_DATA_PROVIDER[blockchain], blockchain, web3=web3, abi=ABI_PDP)
    reserve_tokens = pdp_contract.functions.getAllReservesTokens().call(block_identifier=block)
    aave_tokens = []
    for token in reserve_tokens:
        data = pdp_contract.functions.getReserveTokensAddresses(token[1]).call(block_identifier=block)
        aave_tokens.append(
            {"underlying": token[1], "interest bearing": data[0], "stable debt": data[1], "variable debt": data[2]}
        )
    return aave_tokens


# TODO This function deals with staking AAVE and ABPT, which is included in Aave v2, remove it?
def get_all_rewards(wallet: str, block: int | str, blockchain: str, web3=None, decimals: bool = True) -> List[List]:
    """
    Output: List of 2-element lists: [[reward_token_1_address, balance_1], [t2, b2], ... ]
    """
    try:
        rewards_address = REWARDS_CONTROLLER[blockchain]
    except KeyError:
        raise ValueError(f"{blockchain} not supported yet")

    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    rewards_controller_contract = get_contract(rewards_address, blockchain, web3=web3, abi=ABI_REWARDS_CONTROLLER)

    reward_tokens = const_call(rewards_controller_contract.functions.getRewardsList())

    for token_address in reward_tokens:
        reward_balance = rewards_controller_contract.functions.getUserAccruedRewards(wallet, token_address).call(
            block_identifier=block
        )

        all_rewards.append([token_address, to_token_amount(token_address, reward_balance, blockchain, web3, decimals)])

    return all_rewards


def underlying_all(wallet: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True) -> dict:
    if web3 is None:
        web3 = get_node(blockchain)

    protocol_data_provider_contract = get_contract(
        PROTOCOL_DATA_PROVIDER[blockchain], blockchain, web3=web3, abi=ABI_PDP
    )

    aave_v3_tokens = get_aave_v3_tokens(blockchain, block, web3=web3)

    if isinstance(block, str):
        block_result = last_block(blockchain)
    else:
        block_result = block

    result = {
        "blockchain": blockchain,
        "block": block_result,
        "protocol": "Aave v3",
        "positions_key": "underlying_token_address",
        "decimals": decimals,
        "version": 0,
        "wallet": wallet,
        "positions": {},
    }

    for element in aave_v3_tokens:
        # getUserReserveData returns a list with the following data:
        # [0] = currentATokenBalance,
        # [1] = currentStableDebt,
        # [2] = currentVariableDebt,
        # etc.
        user_reserve_data = protocol_data_provider_contract.functions.getUserReserveData(
            element["underlying"], wallet
        ).call(block_identifier=block)

        # We are only including those positions where the wallet is holding funds
        if user_reserve_data[0:3] != [0, 0, 0]:
            result["positions"][element["underlying"]] = {
                "holdings": [
                    {
                        # Should we include zero balances?
                        "address": element["interest bearing"],
                        "balance": to_token_amount(
                            element["interest bearing"], user_reserve_data[0], blockchain, web3=web3, decimals=decimals
                        ),
                    },
                    {
                        "address": element["stable debt"],
                        "balance": to_token_amount(
                            element["stable debt"], user_reserve_data[1], blockchain, web3=web3, decimals=decimals
                        ),
                    },
                    {
                        "address": element["variable debt"],
                        "balance": to_token_amount(
                            element["variable debt"], user_reserve_data[2], blockchain, web3=web3, decimals=decimals
                        ),
                    },
                ],
                "underlying": [
                    {
                        "address": element["underlying"],
                        "balance": to_token_amount(
                            element["variable debt"],
                            user_reserve_data[0] - user_reserve_data[1] - user_reserve_data[2],
                            blockchain,
                            web3=web3,
                            decimals=decimals,
                        ),
                    }
                ],
            }
    return result


def get_reserves_tokens_balances(
    web3: Web3, wallet: str, block: int | str, blockchain: str, decimals: bool = True
) -> List:
    balances = []

    pdp_contract = get_contract(PROTOCOL_DATA_PROVIDER[blockchain], blockchain, web3=web3, abi=ABI_PDP)

    aave_v3_tokens = get_aave_v3_tokens(blockchain, block, web3=web3)

    for element in aave_v3_tokens:
        token = element["underlying"]
        try:
            user_reserve_data = pdp_contract.functions.getUserReserveData(token, wallet).call(block_identifier=block)
        except ContractLogicError:
            continue

        # balance = currentATokenBalance - currentStableDebt - currentVariableDebt
        balance = Decimal(user_reserve_data[0] - user_reserve_data[1] - user_reserve_data[2])

        if balance != 0:
            balances.append([token, to_token_amount(token, balance, blockchain, web3, decimals)])

    return balances


# TODO: This function should be removed and its functionality added as financial metrics in the underlying_all function
def get_data(wallet, block, blockchain, web3=None, decimals=True):
    """
    Output: Dict with the following structure:
    """
    aave_data = {}
    collaterals = []
    debts = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    pool_addresses_provider_contract = get_contract(
        POOL_ADDRESSES_PROVIDER[blockchain], blockchain, web3=web3, abi=ABI_LPAPR
    )

    lending_pool_address = const_call(pool_addresses_provider_contract.functions.getPool())
    lending_pool_contract = get_contract(lending_pool_address, blockchain, web3=web3, abi=ABI_LENDING_POOL)

    chainlink_native_usd_contract = get_contract(
        CHAINLINK_NATIVE_USD[blockchain], blockchain, web3=web3, abi=ABI_CHAINLINK_ETH_USD
    )
    chainlink_native_usd_decimals = const_call(chainlink_native_usd_contract.functions.decimals())
    eth_usd_price = chainlink_native_usd_contract.functions.latestAnswer().call(block_identifier=block) / Decimal(
        10**chainlink_native_usd_decimals
    )

    data = underlying_all(wallet, block, blockchain, web3=web3, decimals=decimals)["positions"]
    underlying_tokens = list(data.keys())

    price_oracle_address = pool_addresses_provider_contract.functions.getPriceOracle().call(block_identifier=block)
    price_oracle_contract = get_contract(price_oracle_address, blockchain, web3=web3, abi=ABI_PRICE_ORACLE)

    for element in underlying_tokens:
        asset = {"token_address": element, "token_amount": abs(data[element]["underlying"][0]["balance"])}

        currency_unit = price_oracle_contract.functions.BASE_CURRENCY_UNIT().call(block_identifier=block)
        asset["token_price_usd"] = price_oracle_contract.functions.getAssetPrice(asset["token_address"]).call(
            block_identifier=block
        ) / Decimal(currency_unit)

        if data[element]["underlying"][0]["balance"] < 0:
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
    aave_data["native_token_price_usd"] = eth_usd_price

    # Collaterals Data
    aave_data["collaterals"] = collaterals

    # Debts Data
    aave_data["debts"] = debts

    return aave_data
