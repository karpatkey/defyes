from decimal import Decimal

from web3 import Web3

from defyes.cache import const_call
from defyes.constants import ETHEREUM, SNOTE_ETH
from defyes.functions import block_to_timestamp, get_contract, get_node, to_token_amount

NPROXY_ETHEREUM = "0x1344A36A1B56144C3Bc62E7757377D288fDE0369"

# nProxy ABI - getAccount, getCurrencyAndRates, getMaxCurrencyId, getNoteToken, nTokenAddress, nTokenGetClaimableIncentives
ABI_NPROXY = '[{"stateMutability":"nonpayable","type":"fallback"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"getAccount","outputs":[{"components":[{"internalType":"uint40","name":"nextSettleTime","type":"uint40"},{"internalType":"bytes1","name":"hasDebt","type":"bytes1"},{"internalType":"uint8","name":"assetArrayLength","type":"uint8"},{"internalType":"uint16","name":"bitmapCurrencyId","type":"uint16"},{"internalType":"bytes18","name":"activeCurrencies","type":"bytes18"}],"internalType":"struct AccountContext","name":"accountContext","type":"tuple"},{"components":[{"internalType":"uint16","name":"currencyId","type":"uint16"},{"internalType":"int256","name":"cashBalance","type":"int256"},{"internalType":"int256","name":"nTokenBalance","type":"int256"},{"internalType":"uint256","name":"lastClaimTime","type":"uint256"},{"internalType":"uint256","name":"accountIncentiveDebt","type":"uint256"}],"internalType":"struct AccountBalance[]","name":"accountBalances","type":"tuple[]"},{"components":[{"internalType":"uint256","name":"currencyId","type":"uint256"},{"internalType":"uint256","name":"maturity","type":"uint256"},{"internalType":"uint256","name":"assetType","type":"uint256"},{"internalType":"int256","name":"notional","type":"int256"},{"internalType":"uint256","name":"storageSlot","type":"uint256"},{"internalType":"enum AssetStorageState","name":"storageState","type":"uint8"}],"internalType":"struct PortfolioAsset[]","name":"portfolio","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"getCurrencyAndRates","outputs":[{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"bool","name":"hasTransferFee","type":"bool"},{"internalType":"int256","name":"decimals","type":"int256"},{"internalType":"enum TokenType","name":"tokenType","type":"uint8"},{"internalType":"uint256","name":"maxCollateralBalance","type":"uint256"}],"internalType":"struct Token","name":"assetToken","type":"tuple"},{"components":[{"internalType":"address","name":"tokenAddress","type":"address"},{"internalType":"bool","name":"hasTransferFee","type":"bool"},{"internalType":"int256","name":"decimals","type":"int256"},{"internalType":"enum TokenType","name":"tokenType","type":"uint8"},{"internalType":"uint256","name":"maxCollateralBalance","type":"uint256"}],"internalType":"struct Token","name":"underlyingToken","type":"tuple"},{"components":[{"internalType":"int256","name":"rateDecimals","type":"int256"},{"internalType":"int256","name":"rate","type":"int256"},{"internalType":"int256","name":"buffer","type":"int256"},{"internalType":"int256","name":"haircut","type":"int256"},{"internalType":"int256","name":"liquidationDiscount","type":"int256"}],"internalType":"struct ETHRate","name":"ethRate","type":"tuple"},{"components":[{"internalType":"contract AssetRateAdapter","name":"rateOracle","type":"address"},{"internalType":"int256","name":"rate","type":"int256"},{"internalType":"int256","name":"underlyingDecimals","type":"int256"}],"internalType":"struct AssetRateParameters","name":"assetRate","type":"tuple"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getMaxCurrencyId","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getNoteToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"pure","type":"function"}, {"inputs":[{"internalType":"uint16","name":"currencyId","type":"uint16"}],"name":"nTokenAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"blockTime","type":"uint256"}],"name":"nTokenGetClaimableIncentives","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# nToken ABI - decimals, getPresentValueUnderlyingDenominated, totalSupply
ABI_NTOKEN = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getPresentValueUnderlyingDenominated","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# sNote ABI - NOTE, WETH, tokenClaimOf
ABI_SNOTE = '[{"inputs":[],"name":"NOTE","outputs":[{"internalType":"contract ERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"WETH","outputs":[{"internalType":"contract ERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"tokenClaimOf","outputs":[{"internalType":"uint256","name":"wethBalance","type":"uint256"},{"internalType":"uint256","name":"noteBalance","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def get_nproxy_address(blockchain):
    if blockchain == ETHEREUM:
        return NPROXY_ETHEREUM


def get_snote_address(blockchain):
    if blockchain == ETHEREUM:
        return SNOTE_ETH


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_markets_data
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'nproxy_contract' = nproxy_contract -> Improves performance
# 'token_address' = token_address -> retrieves the data of an specific token
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_markets_data(block, blockchain, web3=None, decimals=True, nproxy_contract=None, token_address=None):
    """

    :param block:
    :param blockchain:
    :param web3:
    :return:
    """

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    markets_data = []

    if nproxy_contract is None:
        nproxy_address = get_nproxy_address(blockchain)
        nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

    for i in range(nproxy_contract.functions.getMaxCurrencyId().call(block_identifier=block)):
        market_data = {}

        currency_rates = nproxy_contract.functions.getCurrencyAndRates(i + 1).call(block_identifier=block)

        if token_address is not None and currency_rates[1][0] != token_address:
            continue

        market_data["currencyId"] = i + 1
        market_data["underlyingToken"] = {
            "address": currency_rates[1][0],
            # in 10^decimals format
            "decimals": currency_rates[1][2],
        }
        market_data["cToken"] = {
            "address": currency_rates[0][0],
            # in 10^decimals format
            "decimals": currency_rates[0][2],
            "rate": currency_rates[3][1]
            / (1000000000000000000 * Decimal(currency_rates[1][2]) / Decimal(currency_rates[0][2])),
        }

        # TODO: check if const_call can be used
        ntoken_address = nproxy_contract.functions.nTokenAddress(i + 1).call(block_identifier=block)
        ntoken_contract = get_contract(ntoken_address, blockchain, web3=web3, abi=ABI_NTOKEN, block=block)
        market_data["nToken"] = {
            "address": ntoken_address,
            # in 10^decimals format
            "decimals": 10 ** const_call(ntoken_contract.functions.decimals()),
            "rate": ntoken_contract.functions.getPresentValueUnderlyingDenominated().call(block_identifier=block)
            / Decimal(ntoken_contract.functions.totalSupply().call(block_identifier=block)),
        }

        markets_data.append(market_data)

        if token_address is not None:
            break

    return markets_data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# all_note_rewards
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'nproxy_contract' = nproxy_contract -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def all_note_rewards(wallet, block, blockchain, web3=None, decimals=True, nproxy_contract=None):
    """
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :return:
    """
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    if nproxy_contract is None:
        nproxy_address = get_nproxy_address(blockchain)
        nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

    note_token_address = const_call(nproxy_contract.functions.getNoteToken())
    note_rewards = nproxy_contract.functions.nTokenGetClaimableIncentives(
        wallet, block_to_timestamp(block, blockchain)
    ).call(block_identifier=block)

    all_rewards.append(
        [note_token_address, to_token_amount(note_token_address, note_rewards, blockchain, web3, decimals)]
    )

    return all_rewards


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
def get_staked(wallet, block, blockchain, web3=None, decimals=True, reward=False):
    """
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param reward:
    :return:
    """
    balances = []
    result = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    nproxy_address = get_nproxy_address(blockchain)
    nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

    snote_token_address = get_snote_address(blockchain)
    snote_contract = get_contract(snote_token_address, blockchain, web3=web3, abi=ABI_SNOTE, block=block)

    weth_balance, note_balance = snote_contract.functions.tokenClaimOf(wallet).call(block_identifier=block)

    weth_address = const_call(snote_contract.functions.WETH())
    note_address = const_call(snote_contract.functions.NOTE())

    balances.append([weth_address, to_token_amount(weth_address, weth_balance, blockchain, web3, decimals)])
    balances.append([note_address, to_token_amount(note_address, note_balance, blockchain, web3, decimals)])

    if reward is True:
        all_rewards = all_note_rewards(
            wallet, block, blockchain, web3=web3, decimals=decimals, nproxy_contract=nproxy_contract
        )
        result.append(balances)
        result.append(all_rewards)

    else:
        result = balances

    return result


def _get_balances(markets_data, account_data, decimals):
    balances = []
    for market_data in markets_data:
        underlying_balance = 0
        for account_balance in account_data[1]:
            if account_balance[0] == market_data["currencyId"]:
                underlying_balance = (
                    underlying_balance
                    + account_balance[1]
                    * market_data["cToken"]["rate"]
                    * market_data["underlyingToken"]["decimals"]
                    / market_data["cToken"]["decimals"]
                )
                underlying_balance = (
                    underlying_balance
                    + account_balance[2]
                    * market_data["nToken"]["rate"]
                    * market_data["underlyingToken"]["decimals"]
                    / market_data["nToken"]["decimals"]
                )

        for portfolio_item in account_data[2]:
            if portfolio_item[0] == market_data["currencyId"]:
                underlying_balance = underlying_balance + portfolio_item[3] * market_data["underlyingToken"][
                    "decimals"
                ] / Decimal(10**8)

        if underlying_balance != 0:
            if decimals:
                underlying_balance = underlying_balance / Decimal(market_data["underlyingToken"]["decimals"])

            balances.append([market_data["underlyingToken"]["address"], underlying_balance])
    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [token_address, balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying_all(wallet, block, blockchain, web3=None, decimals=True, reward=False):
    """
    :param wallet:
    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param reward:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    nproxy_address = get_nproxy_address(blockchain)
    nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

    markets_data = get_markets_data(block, blockchain, web3=web3, nproxy_contract=nproxy_contract)
    account_data = nproxy_contract.functions.getAccount(wallet).call(block_identifier=block)

    result = _get_balances(markets_data, account_data, decimals)

    if reward is True:
        all_rewards = all_note_rewards(
            wallet, block, blockchain, web3=web3, decimals=decimals, nproxy_contract=nproxy_contract
        )
        result = [result, all_rewards]

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 elements:
# 1 - List of Tuples: [token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, token_address, block, blockchain, web3=None, decimals=True):
    """
    :param wallet:
    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    token_address = Web3.to_checksum_address(token_address)

    nproxy_address = get_nproxy_address(blockchain)
    nproxy_contract = get_contract(nproxy_address, blockchain, web3=web3, abi=ABI_NPROXY, block=block)

    markets_data = get_markets_data(
        block, blockchain, web3=web3, nproxy_contract=nproxy_contract, token_address=token_address
    )
    account_data = nproxy_contract.functions.getAccount(wallet).call(block_identifier=block)

    return _get_balances(markets_data, account_data, decimals)
