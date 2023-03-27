from defi_protocols.functions import get_node, get_contract, block_to_timestamp, get_decimals, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, ETHEREUM, SNOTE_ETH

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# NPROXY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum - nProxy Address
NPROXY_ETHEREUM = '0x1344A36A1B56144C3Bc62E7757377D288fDE0369'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# nProxy ABI - getAccount, getAccountBalance, getAccountContext, getAccountPortfolio, getActiveMarkets, getActiveMarketsAtBlockTime, getAssetsBitmap, getAuthorizedCallbackContractStatus, getCashGroup, getCashGroupAndAssetRate, getCurrency, getCurrencyAndRates, getCurrencyId, getDepositParameters, getFreeCollateral, getGlobalTransferOperatorStatus, getInitializationParameters, getLendingPool, getLibInfo, getMarket, getMaxCurrencyId, getNTokenAccount, getNTokenPortfolio, getNoteToken, getOwnershipStatus, getRateStorage, getReserveBalance, getReserveBuffer, getSecondaryIncentiveRewarder, getSettlementRate, getTreasuryManager, getfCashNotional, nTokenAddress, nTokenGetClaimableIncentives
ABI_NPROXY = '[{"stateMutability":"nonpayable","type":"fallback"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getAccount","outputs":[{"components":[{"internalType":"uint40","name":"nextSettleTime","type":"uint40"},{"internalType":"bytes1","name":"hasDebt","type":"bytes1"},{"internalType":"uint8","name":"assetArrayLength","type":"uint8"},{"internalType":"uint16","name":"bitmapCurrencyId","type":"uint16"},{"internalType":"bytes18","name":"activeCurrencies","type":"bytes18"}],"internalType":"struct AccountContext","name":"accountContext","type":"tuple"},{"components":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"int256","name":"cashBalance","type":"int256"},{"internalType":"int256","name":"nTokenBalance","type":"int256"},{"internalType":"uint256","name":"lastClaimTime","type":"uint256"},{"internalType":"uint256","name":"accountIncentiveDebt","type":"uint256"}],"internalType":"struct AccountBalance[]","name":"accountBalances","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"currencyId","type":"uint256"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"uint256","name":"assetType","type":"uint256"},{"internalType":"int256","name":"notional","type":"int256"},{"internalType":"uint256","name":"storageSlot","type":"uint256"},{"internalType":"enum AssetStorageState","name":"storageState","type":"uint8"}],"internalType":"struct PortfolioAsset[]","name":"portfolio","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"address","name":"account","type":"address"}],"name":"getAccountBalance","outputs":[{"internalType":"int256","name":"cashBalance","type":"int256"},{"internalType":"int256","name":"nTokenBalance","type":"int256"},{"internalType":"uint256","name":"lastClaimTime","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getAccountContext","outputs":[{"components":[{"internalType":"uint40","name":"nextSettleTime","type":"uint40"},{"internalType":"bytes1","name":"hasDebt","type":"bytes1"},{"internalType":"uint8","name":"assetArrayLength","type":"uint8"},{"internalType":"uint16","name":"bitmapCurrencyId","type":"uint16"},{"internalType":"bytes18","name":"activeCurrencies","type":"bytes18"}],"internalType":"struct AccountContext","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getAccountPortfolio","outputs":[{"components":[{"internalType":"uint256","name":"currencyId","type":"uint256"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"uint256","name":"assetType","type":"uint256"},{"internalType":"int256","name":"notional","type":"int256"},{"internalType":"uint256","name":"storageSlot","type":"uint256"},{"internalType":"enum AssetStorageState","name":"storageState","type":"uint8"}],"internalType":"struct PortfolioAsset[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getActiveMarkets","outputs":[{"components":[{"internalType":"bytes32","name":"storageSlot","type":"bytes32"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"int256","name":"totalfCash","type":"int256"},{"internalType":"int256","name":"totalAssetCash","type":"int256"},{"internalType":"int256","name":"totalLiquidity","type":"int256"},{"internalType":"uint256","name":"lastImpliedRate","type":"uint256"},{"internalType":"uint256","name":"oracleRate","type":"uint256"},{"internalType":"uint256","name":"previousTradeTime","type":"uint256"}],"internalType":"struct MarketParameters[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"uint32","name":"blockTime","type":"uint32"}],"name":"getActiveMarketsAtBlockTime","outputs":[{"components":[{"internalType":"bytes32","name":"storageSlot","type":"bytes32"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"int256","name":"totalfCash","type":"int256"},{"internalType":"int256","name":"totalAssetCash","type":"int256"},{"internalType":"int256","name":"totalLiquidity","type":"int256"},{"internalType":"uint256","name":"lastImpliedRate","type":"uint256"},{"internalType":"uint256","name":"oracleRate","type":"uint256"},{"internalType":"uint256","name":"previousTradeTime","type":"uint256"}],"internalType":"struct MarketParameters[]","name":"","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getAssetsBitmap","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"callback","type":"address"}],"name":"getAuthorizedCallbackContractStatus","outputs":[{"internalType":"bool","name":"isAuthorized","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getCashGroup","outputs":[{"components":[{"internalType":"uint8","name":"maxMarketIndex","type":"uint8"},{"internalType":"uint8","name":"rateOracleTimeWindow5Min","type":"uint8"},{"internalType":"uint8","name":"totalFeeBPS","type":"uint8"},{"internalType":"uint8","name":"reserveFeeShare","type":"uint8"},{"internalType":"uint8","name":"debtBuffer5BPS","type":"uint8"},{"internalType":"uint8","name":"fCashHaircut5BPS","type":"uint8"},{"internalType":"uint8","name":"settlementPenaltyRate5BPS","type":"uint8"},{"internalType":"uint8","name":"liquidationfCashHaircut5BPS","type":"uint8"},{"internalType":"uint8","name":"liquidationDebtBuffer5BPS","type":"uint8"},{"internalType":"uint8[]","name":"liquidityTokenHaircuts","type":"uint8[]"},{"internalType":"uint8[]","name":"rateScalars","type":"uint8[]"}],"internalType":"struct CashGroupSettings","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getCashGroupAndAssetRate","outputs":[{"components":[{"internalType":"uint8","name":"maxMarketIndex","type":"uint8"},{"internalType":"uint8","name":"rateOracleTimeWindow5Min","type":"uint8"},{"internalType":"uint8","name":"totalFeeBPS","type":"uint8"},{"internalType":"uint8","name":"reserveFeeShare","type":"uint8"},{"internalType":"uint8","name":"debtBuffer5BPS","type":"uint8"},{"internalType":"uint8","name":"fCashHaircut5BPS","type":"uint8"},{"internalType":"uint8","name":"settlementPenaltyRate5BPS","type":"uint8"},{"internalType":"uint8","name":"liquidationfCashHaircut5BPS","type":"uint8"},{"internalType":"uint8","name":"liquidationDebtBuffer5BPS","type":"uint8"},{"internalType":"uint8[]","name":"liquidityTokenHaircuts","type":"uint8[]"},{"internalType":"uint8[]","name":"rateScalars","type":"uint8[]"}],"internalType":"struct CashGroupSettings","name":"cashGroup","type":"tuple"},{"components":[{"internalType":"contract AssetRateAdapter","name":"rateOracle","type":"address"},{"internalType":"int256","name":"rate","type":"int256"},{"internalType":"int256","name":"underlyingDecimals","type":"int256"}],"internalType":"struct AssetRateParameters","name":"assetRate","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getCurrency","outputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"bool","name":"hasTransferFee","type":"bool"},{"internalType":"int256","name":"decimals","type":"int256"},{"internalType":"enum TokenType","name":"tokenType","type":"uint8"},{"internalType":"uint256","name":"maxCollateralBalance","type":"uint256"}],"internalType":"struct Token","name":"assetToken","type":"tuple"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"bool","name":"hasTransferFee","type":"bool"},{"internalType":"int256","name":"decimals","type":"int256"},{"internalType":"enum TokenType","name":"tokenType","type":"uint8"},{"internalType":"uint256","name":"maxCollateralBalance","type":"uint256"}],"internalType":"struct Token","name":"underlyingToken","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getCurrencyAndRates","outputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"bool","name":"hasTransferFee","type":"bool"},{"internalType":"int256","name":"decimals","type":"int256"},{"internalType":"enum TokenType","name":"tokenType","type":"uint8"},{"internalType":"uint256","name":"maxCollateralBalance","type":"uint256"}],"internalType":"struct Token","name":"assetToken","type":"tuple"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"bool","name":"hasTransferFee","type":"bool"},{"internalType":"int256","name":"decimals","type":"int256"},{"internalType":"enum TokenType","name":"tokenType","type":"uint8"},{"internalType":"uint256","name":"maxCollateralBalance","type":"uint256"}],"internalType":"struct Token","name":"underlyingToken","type":"tuple"},{"components":[{"internalType":"int256","name":"rateDecimals","type":"int256"},{"internalType":"int256","name":"rate","type":"int256"},{"internalType":"int256","name":"buffer","type":"int256"},{"internalType":"int256","name":"haircut","type":"int256"},{"internalType":"int256","name":"liquidationDiscount","type":"int256"}],"internalType":"struct ETHRate","name":"ethRate","type":"tuple"},{"components":[{"internalType":"contract AssetRateAdapter","name":"rateOracle","type":"address"},{"internalType":"int256","name":"rate","type":"int256"},{"internalType":"int256","name":"underlyingDecimals","type":"int256"}],"internalType":"struct AssetRateParameters","name":"assetRate","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"getCurrencyId","outputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getDepositParameters","outputs":[{"internalType":"int256[]","name":"depositShares","type":"int256[]"},{"internalType":"int256[]","name":"leverageThresholds","type":"int256[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getFreeCollateral","outputs":[{"internalType":"int256","name":"","type":"int256"},{"internalType":"int256[]","name":"","type":"int256[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"operator","type":"address"}],"name":"getGlobalTransferOperatorStatus","outputs":[{"internalType":"bool","name":"isAuthorized","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getInitializationParameters","outputs":[{"internalType":"int256[]","name":"annualizedAnchorRates","type":"int256[]"},{"internalType":"int256[]","name":"proportions","type":"int256[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getLendingPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getLibInfo","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"uint256","name":"settlementDate","type":"uint256"}],"name":"getMarket","outputs":[{"components":[{"internalType":"bytes32","name":"storageSlot","type":"bytes32"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"int256","name":"totalfCash","type":"int256"},{"internalType":"int256","name":"totalAssetCash","type":"int256"},{"internalType":"int256","name":"totalLiquidity","type":"int256"},{"internalType":"uint256","name":"lastImpliedRate","type":"uint256"},{"internalType":"uint256","name":"oracleRate","type":"uint256"},{"internalType":"uint256","name":"previousTradeTime","type":"uint256"}],"internalType":"struct MarketParameters","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getMaxCurrencyId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"getNTokenAccount","outputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"uint256","name":"totalSupply","type":"uint256"},{"internalType":"uint256","name":"incentiveAnnualEmissionRate","type":"uint256"},{"internalType":"uint256","name":"lastInitializedTime","type":"uint256"},{"internalType":"bytes5","name":"nTokenParameters","type":"bytes5"},{"internalType":"int256","name":"cashBalance","type":"int256"},{"internalType":"uint256","name":"accumulatedNOTEPerNToken","type":"uint256"},{"internalType":"uint256","name":"lastAccumulatedTime","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"getNTokenPortfolio","outputs":[{"components":[{"internalType":"uint256","name":"currencyId","type":"uint256"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"uint256","name":"assetType","type":"uint256"},{"internalType":"int256","name":"notional","type":"int256"},{"internalType":"uint256","name":"storageSlot","type":"uint256"},{"internalType":"enum AssetStorageState","name":"storageState","type":"uint8"}],"internalType":"struct PortfolioAsset[]","name":"liquidityTokens","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"currencyId","type":"uint256"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"uint256","name":"assetType","type":"uint256"},{"internalType":"int256","name":"notional","type":"int256"},{"internalType":"uint256","name":"storageSlot","type":"uint256"},{"internalType":"enum AssetStorageState","name":"storageState","type":"uint8"}],"internalType":"struct PortfolioAsset[]","name":"netfCashAssets","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getNoteToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"}, {"inputs":[],"name":"getOwnershipStatus","outputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"pendingOwner","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getRateStorage","outputs":[{"components":[{"internalType":"contract AggregatorV2V3Interface","name":"rateOracle","type":"address"},{"internalType":"uint8","name":"rateDecimalPlaces","type":"uint8"},{"internalType":"bool","name":"mustInvert","type":"bool"},{"internalType":"uint8","name":"buffer","type":"uint8"},{"internalType":"uint8","name":"haircut","type":"uint8"},{"internalType":"uint8","name":"liquidationDiscount","type":"uint8"}],"internalType":"struct ETHRateStorage","name":"ethRate","type":"tuple"},{"components":[{"internalType":"contract AssetRateAdapter","name":"rateOracle","type":"address"},{"internalType":"uint8","name":"underlyingDecimalPlaces","type":"uint8"}],"internalType":"struct AssetRateStorage","name":"assetRate","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getReserveBalance","outputs":[{"internalType":"int256","name":"reserveBalance","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getReserveBuffer","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getSecondaryIncentiveRewarder","outputs":[{"internalType":"address","name":"rewarder","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"uint40","name":"maturity","type":"uint40"}],"name":"getSettlementRate","outputs":[{"components":[{"internalType":"contract AssetRateAdapter","name":"rateOracle","type":"address"},{"internalType":"int256","name":"rate","type":"int256"},{"internalType":"int256","name":"underlyingDecimals","type":"int256"}],"internalType":"struct AssetRateParameters","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getTreasuryManager","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"uint256","name":"maturity","type":"uint256"}],"name":"getfCashNotional","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"nTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockTime","type":"uint256"}],"name":"nTokenGetClaimableIncentives","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# nToken ABI - decimals, getPresentValueUnderlyingDenominated, totalSupply
ABI_NTOKEN = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getPresentValueUnderlyingDenominated","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# sNote ABI - NOTE, WETH, tokenClaimOf
ABI_SNOTE = '[{"inputs":[],"name":"NOTE","outputs":[{"internalType":"contract ERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"WETH","outputs":[{"internalType":"contract ERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"tokenClaimOf","outputs":[{"internalType":"uint256","name":"wethBalance","type":"uint256"},{"internalType":"uint256","name":"noteBalance","type":"uint256"}],"stateMutability":"view","type":"function"}]'


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_nproxy_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_nproxy_address(blockchain):
    if blockchain == ETHEREUM:
        return NPROXY_ETHEREUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_snote_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_snote_address(blockchain):
    if blockchain == ETHEREUM:
        return SNOTE_ETH


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_markets_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'nproxy_contract' = nproxy_contract -> Improves performance
# 'token_address' = token_address -> retrieves the data of an specific token
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_markets_data(block, blockchain, web3=None, decimals=True, execution=1, index=0, nproxy_contract=None,
                     token_address=None):
    """

    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        markets_data = []

        if nproxy_contract is None:
            nproxy_address = get_nproxy_address(blockchain)
            nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

        for i in range(nproxy_contract.functions.getMaxCurrencyId().call(block_identifier=block)):
            market_data = {}

            currency_rates = nproxy_contract.functions.getCurrencyAndRates(i + 1).call(block_identifier=block)

            if token_address != None and currency_rates[1][0] != token_address:
                continue

            market_data['currencyId'] = i + 1
            market_data['underlyingToken'] = {
                'address': currency_rates[1][0],
                # in 10^decimals format
                'decimals': currency_rates[1][2]
            }
            market_data['cToken'] = {
                'address': currency_rates[0][0],
                # in 10^decimals format
                'decimals': currency_rates[0][2],
                'rate': currency_rates[3][1] / (1000000000000000000 * currency_rates[1][2] / currency_rates[0][2])
            }

            ntoken_address = nproxy_contract.functions.nTokenAddress(i + 1).call()
            ntoken_contract = get_contract(ntoken_address, blockchain, web3=web3, abi=ABI_NTOKEN, block=block)
            market_data['nToken'] = {
                'address': ntoken_address,
                # in 10^decimals format
                'decimals': 10 ** ntoken_contract.functions.decimals().call(),
                'rate': ntoken_contract.functions.getPresentValueUnderlyingDenominated().call(
                    block_identifier=block) / ntoken_contract.functions.totalSupply().call(block_identifier=block)
            }

            markets_data.append(market_data)

            if token_address != None:
                break

        return markets_data

    except GetNodeIndexError:
        return get_markets_data(block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_markets_data(block, blockchain, decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# all_note_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'nproxy_contract' = nproxy_contract -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def all_note_rewards(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, nproxy_contract=None):
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

    all_rewards = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        if nproxy_contract is None:
            nproxy_address = get_nproxy_address(blockchain)
            nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

        note_token_address = nproxy_contract.functions.getNoteToken().call()

        if decimals == True:
            note_rewards = nproxy_contract.functions.nTokenGetClaimableIncentives(wallet, block_to_timestamp(block,
                                                                                                             blockchain)).call() / (
                                       10 ** (get_decimals(note_token_address, blockchain, web3=web3)))

        all_rewards.append([note_token_address, note_rewards])

        return all_rewards

    except GetNodeIndexError:
        return all_note_rewards(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return all_note_rewards(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staked
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staked(wallet, block, blockchain, web3=None, decimals=True, execution=1, index=0, reward=False):
    """

    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param execution:
    :param index:
    :param reward:
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

        nproxy_address = get_nproxy_address(blockchain)
        nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

        snote_token_address = get_snote_address(blockchain)
        snote_contract = get_contract(snote_token_address, blockchain, web3=web3, abi=ABI_SNOTE, block=block)

        staked_tokens_amounts = snote_contract.functions.tokenClaimOf(wallet).call(block_identifier=block)

        weth_address = snote_contract.functions.WETH().call()
        note_address = snote_contract.functions.NOTE().call()

        if decimals == True:
            staked_tokens_amounts[0] = staked_tokens_amounts[0] / (
                        10 ** get_decimals(weth_address, blockchain, web3=web3))
            staked_tokens_amounts[1] = staked_tokens_amounts[1] / (
                        10 ** get_decimals(note_address, blockchain, web3=web3))

        balances.append([weth_address, staked_tokens_amounts[0]])
        balances.append([note_address, staked_tokens_amounts[1]])

        if reward is True:
            all_rewards = all_note_rewards(wallet, block, blockchain, web3=web3, decimals=decimals,
                                           nproxy_contract=nproxy_contract)
            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return get_staked(wallet, block, blockchain, decimals=decimals, reward=reward, index=0, execution=execution + 1)

    except:
        return get_staked(wallet, block, blockchain, decimals=decimals, reward=reward, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying_all(wallet, block, blockchain, web3=None, decimals=True, execution=1, index=0, reward=False):
    """

    :param wallet:
    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param execution:
    :param index:
    :param reward:
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

        nproxy_address = get_nproxy_address(blockchain)
        nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

        markets_data = get_markets_data(block, blockchain, web3=web3, nproxy_contract=nproxy_contract)

        account_data = nproxy_contract.functions.getAccount(wallet).call(block_identifier=block)

        for market_data in markets_data:
            underlying_balance = 0
            for account_balance in account_data[1]:
                if account_balance[0] == market_data['currencyId']:
                    underlying_balance = underlying_balance + account_balance[1] * market_data['cToken']['rate'] * \
                                         market_data['underlyingToken']['decimals'] / market_data['cToken']['decimals']
                    underlying_balance = underlying_balance + account_balance[2] * market_data['nToken']['rate'] * \
                                         market_data['underlyingToken']['decimals'] / market_data['nToken']['decimals']

            for portfolio_item in account_data[2]:
                if portfolio_item[0] == market_data['currencyId']:
                    underlying_balance = underlying_balance + portfolio_item[3] * market_data['underlyingToken'][
                        'decimals'] / (10 ** 8)

            if underlying_balance != 0:
                if decimals == True:
                    underlying_balance = underlying_balance / market_data['underlyingToken']['decimals']

                balances.append([market_data['underlyingToken']['address'], underlying_balance])

        if reward is True:
            all_rewards = all_note_rewards(wallet, block, blockchain, web3=web3, decimals=decimals,
                                           nproxy_contract=nproxy_contract)
            result.append(balances)
            result.append(all_rewards)

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
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 elements:
# 1 - List of Tuples: [token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, token_address, block, blockchain, web3=None, decimals=True, execution=1, index=0):
    """

    :param wallet:
    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param execution:
    :param index:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        token_address = web3.to_checksum_address(token_address)

        nproxy_address = get_nproxy_address(blockchain)
        nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

        markets_data = get_markets_data(block, blockchain, web3=web3, nproxy_contract=nproxy_contract,
                                        token_address=token_address)

        account_data = nproxy_contract.functions.getAccount(wallet).call(block_identifier=block)

        for market_data in markets_data:
            underlying_balance = 0
            for account_balance in account_data[1]:
                if account_balance[0] == market_data['currencyId']:
                    underlying_balance = underlying_balance + account_balance[1] * market_data['cToken']['rate'] * \
                                         market_data['underlyingToken']['decimals'] / market_data['cToken']['decimals']
                    underlying_balance = underlying_balance + account_balance[2] * market_data['nToken']['rate'] * \
                                         market_data['underlyingToken']['decimals'] / market_data['nToken']['decimals']

            for portfolio_item in account_data[2]:
                if portfolio_item[0] == market_data['currencyId']:
                    underlying_balance = underlying_balance + portfolio_item[3] * market_data['underlyingToken'][
                        'decimals'] / (10 ** 8)

            if underlying_balance != 0:
                if decimals == True:
                    underlying_balance = underlying_balance / market_data['underlyingToken']['decimals']

                balances.append([market_data['underlyingToken']['address'], underlying_balance])

        return balances

    except GetNodeIndexError:
        return underlying(wallet, token_address, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, token_address, block, blockchain, decimals=decimals, index=index + 1,
                          execution=execution)

# print(underlying_all('0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C', 'latest', ETHEREUM, reward=True))
# print(get_market_data('latest', ETHEREUM))

# print(get_staked('0x2A254687F5056EA5235d41f218D7E3BB946DAdFf', 'latest', ETHEREUM, reward=True))
# print(underlying_all('0x2A254687F5056EA5235d41f218D7E3BB946DAdFf', 'latest', ETHEREUM))

# print(get_staked('0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C', 'latest', ETHEREUM, reward=True))
# print(underlying_all('0x5853eD4f26A3fceA565b3FBC698bb19cdF6DEB85', 'latest', ETHEREUM))
# print(underlying_all('0x668d775dc3EE120510e76Fe0476BB943E8b756DE', 'latest', ETHEREUM, reward=True))

# print(underlying('0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C', DAI_ETH, 'latest', ETHEREUM))
# print(underlying('0x5853eD4f26A3fceA565b3FBC698bb19cdF6DEB85', ZERO_ADDRESS, 'latest', ETHEREUM))


# ndai = get_contract("0x6EbcE2453398af200c688C7c4eBD479171231818", ETHEREUM)
# ndai_id = ndai.functions.currencyId().call()
# view = get_contract("0x1344A36A1B56144C3Bc62E7757377D288fDE0369", ETHEREUM, abi=ABI_NPROXY)
# currency1 = view.functions.getAccountBalance(3, '0x5853eD4f26A3fceA565b3FBC698bb19cdF6DEB85').call()
# currency2 = view.functions.getAccountPortfolio('0x5853eD4f26A3fceA565b3FBC698bb19cdF6DEB85').call()
# collateral = view.functions.getFreeCollateral('0x668d775dc3EE120510e76Fe0476BB943E8b756DE').call()
# currency = view.functions.getCurrency(2).call()
# currency1 = view.functions.getAccount('0x5853eD4f26A3fceA565b3FBC698bb19cdF6DEB85').call()
# currency2 = view.functions.getAccount('0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C').call()
# rate = view.functions.getCurrencyAndRates(2).call()
# ntoken = view.functions.getNTokenAccount('0x6EbcE2453398af200c688C7c4eBD479171231818').call()
# init = view.functions.getInitializationParameters(ndai_id).call()
# balance = view.functions.getReserveBalance(ndai_id).call()
# ntoken_portfolio = view.functions.getNTokenPortfolio('0x6EbcE2453398af200c688C7c4eBD479171231818').call()
# #currency = view.functions.getAccount('0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C').call()
# market = view.functions.getActiveMarkets(1).call()
# rewarder = view.functions.nTokenGetClaimableIncentives('0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C', 1677268561).call()
# print(collateral)
# print(currency1)
# print(currency2)
