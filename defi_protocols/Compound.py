from decimal import Decimal
from web3.exceptions import ContractLogicError, BadFunctionCallOutput
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, balance_of, get_decimals, to_token_amount
from defi_protocols.constants import ETHEREUM, COMP_ETH, ZERO_ADDRESS
from defi_protocols.prices import prices

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# COMPTROLLER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum - Comptroller Address
COMPTROLLER_ETHEREUM = '0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# COMPOUND LENS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum - Compound Lens Address
COMPOUND_LENS_ETHEREUM = '0xdCbDb7306c6Ff46f77B349188dC18cEd9DF30299'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# cToken ABI - decimals, balanceOf, totalSupply, exchangeRateStored, underlying, borrowBalanceStored, supplyRatePerBlock, borrowRatePerBlock, totalBorrows
ABI_CTOKEN = '[{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"exchangeRateStored","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"underlying","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"borrowBalanceStored","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"supplyRatePerBlock","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"borrowRatePerBlock","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalBorrows","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Comptroller ABI - getAllMarkets, compRate, compSpeeds, compSupplySpeeds, compBorrowSpeeds
ABI_COMPTROLLER = '[{"constant":true,"inputs":[],"name":"getAllMarkets","outputs":[{"internalType":"contract CToken[]","name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"compRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"compSpeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"compSupplySpeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"compBorrowSpeeds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Compound Lens ABI - getCompBalanceMetadataExt
ABI_COMPOUND_LENS = '[{"constant":false,"inputs":[{"internalType":"contract Comp","name":"comp","type":"address"},{"internalType":"contract ComptrollerLensInterface","name":"comptroller","type":"address"},{"internalType":"address","name":"account","type":"address"}],"name":"getCompBalanceMetadataExt","outputs":[{"components":[{"internalType":"uint256","name":"balance","type":"uint256"},{"internalType":"uint256","name":"votes","type":"uint256"},{"internalType":"address","name":"delegate","type":"address"},{"internalType":"uint256","name":"allocated","type":"uint256"}],"internalType":"struct CompoundLens.CompBalanceMetadataExt","name":"","type":"tuple"}],"payable":false,"stateMutability":"nonpayable","type":"function"}]'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# WEB DOCS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

'''
https://docs.compound.finance/v2/
'''


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_comptoller_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_comptoller_address(blockchain):
    if blockchain == ETHEREUM:
        return COMPTROLLER_ETHEREUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_compound_lens_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_compound_lens_address(blockchain):
    if blockchain == ETHEREUM:
        return COMPOUND_LENS_ETHEREUM


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_compound_token_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_compound_token_address(blockchain):
    if blockchain == ETHEREUM:
        return COMP_ETH


def get_ctokens_contract_list(blockchain, web3, block):
    comptroller_address = get_comptoller_address(blockchain)
    comptroller_contract = get_contract(comptroller_address, blockchain, web3=web3, abi=ABI_COMPTROLLER,
                                        block=block)

    return comptroller_contract.functions.getAllMarkets().call()


def get_comptroller_contract(blockchain, web3, block):
    comptroller_address = get_comptoller_address(blockchain)
    return get_contract(comptroller_address, blockchain, web3=web3, abi=ABI_COMPTROLLER, block=block)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_ctoken_data
# 'web3' = web3 (Node) -> Improves performance
# 'ctoken_contract' = ctoken_contract -> Improves performance
# 'underlying_token' = underlying_token -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ctoken_data(ctoken_address, wallet, block, blockchain, web3=None, ctoken_contract=None, underlying_token=None):
    """
    :param ctoken_address:
    :param wallet:
    :param block:
    :param blockchain:
    :param web3:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    ctoken_data = {}

    if ctoken_contract:
        ctoken_data['contract'] = ctoken_contract
    else:
        ctoken_data['contract'] = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

    if underlying_token:
        ctoken_data['underlying'] = underlying_token
    else:
        try:
            ctoken_data['underlying'] = ctoken_data['contract'].functions.underlying().call(block_identifier=block)
        except (ContractLogicError, BadFunctionCallOutput):
            ctoken_data['underlying'] = ZERO_ADDRESS

    ctoken_data['decimals'] = ctoken_data['contract'].functions.decimals().call()
    ctoken_data['borrowBalanceStored'] = ctoken_data['contract'].functions.borrowBalanceStored(wallet).call(
        block_identifier=block)
    ctoken_data['balanceOf'] = ctoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)
    ctoken_data['exchangeRateStored'] = ctoken_data['contract'].functions.exchangeRateStored().call(
        block_identifier=block)

    return ctoken_data


def _get_token_balance(ctoken_data, token_address, block, blockchain, web3, decimals):
    underlying_token_decimals = get_decimals(token_address, block=block, blockchain=blockchain, web3=web3)

    mantissa = 18 - ctoken_data['decimals'] + underlying_token_decimals
    exchange_rate = ctoken_data['exchangeRateStored'] / Decimal(10 ** mantissa)

    underlying_token_balance = ctoken_data['balanceOf'] / Decimal(10 ** ctoken_data['decimals']) * exchange_rate
    underlying_token_balance -= ctoken_data['borrowBalanceStored'] / Decimal(10 ** underlying_token_decimals)

    if not decimals:
        underlying_token_balance = underlying_token_balance * Decimal(10 ** underlying_token_decimals)

    return [token_address, underlying_token_balance]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 elements:
# 1 - List of Tuples: [token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, token_address, block, blockchain, web3=None, decimals=True):
    """
    :param wallet:
    :param token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)
    wallet = Web3.to_checksum_address(wallet)
    token_address = Web3.to_checksum_address(token_address)

    ctoken_list = get_ctokens_contract_list(blockchain, web3, block)
    for ctoken_address in ctoken_list:

        ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

        try:
            underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
        except (ContractLogicError, BadFunctionCallOutput):
            # cETH does not have the underlying function
            underlying_token = ZERO_ADDRESS

        if underlying_token == token_address:
            ctoken_data = get_ctoken_data(ctoken_address, wallet, block, blockchain, web3=web3,
                                          ctoken_contract=ctoken_contract, underlying_token=underlying_token)
            balances.append(_get_token_balance(ctoken_data, token_address, block, blockchain, web3, decimals))

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
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
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    ctoken_list = get_ctokens_contract_list(blockchain, web3, block)

    for ctoken_address in ctoken_list:
        if balance_of(wallet, ctoken_address, block, blockchain, web3=web3) > 0:
            ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

            try:
                underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
            except (ContractLogicError, BadFunctionCallOutput):
                # cETH does not have the underlying function
                underlying_token = ZERO_ADDRESS

            ctoken_data = get_ctoken_data(ctoken_address, wallet, block, blockchain, web3=web3,
                                          ctoken_contract=ctoken_contract, underlying_token=underlying_token)

            balances.append(_get_token_balance(ctoken_data, underlying_token, block, blockchain, web3, decimals))

    if reward is True:
        all_rewards = all_comp_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)
        balances = [balances, all_rewards]

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# all_comp_rewards
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def all_comp_rewards(wallet, block, blockchain, web3=None, decimals=True):
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

    compound_lens_address = get_compound_lens_address(blockchain)
    comp_token_address = get_compound_token_address(blockchain)
    comptroller_address = get_comptoller_address(blockchain)
    if compound_lens_address and comp_token_address and comptroller_address:
        compound_lens_contract = get_contract(compound_lens_address,
                                              blockchain,
                                              web3=web3,
                                              abi=ABI_COMPOUND_LENS,
                                              block=block)
        meta_data = compound_lens_contract.functions.getCompBalanceMetadataExt(comp_token_address,
                                                                               comptroller_address,
                                                                               wallet).call(block_identifier=block)
        comp_rewards = meta_data[3]

        all_rewards.append([comp_token_address, to_token_amount(comp_token_address, comp_rewards, blockchain, web3, decimals)])

    return all_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(ctoken_amount, ctoken_address, block, blockchain, web3=None, decimals=True):
    """
    :param ctoken_amount:
    :param ctoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    ctoken_contract = get_contract(ctoken_address, blockchain, abi=ABI_CTOKEN, web3=web3, block=block)
    ctoken_decimals = ctoken_contract.functions.decimals().call()
    exchange_rate = ctoken_contract.functions.exchangeRateStored().call(block_identifier=block)

    try:
        underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
    except (ContractLogicError, BadFunctionCallOutput):
        # cETH does not have the underlying function
        underlying_token = ZERO_ADDRESS

    underlying_token_decimals = get_decimals(underlying_token, blockchain, web3=web3) if decimals else 0
    mantissa = 18 - ctoken_decimals + underlying_token_decimals
    underlying_token_balance = ctoken_amount * exchange_rate / Decimal(10 ** mantissa)

    return [underlying_token, underlying_token_balance]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_apr
# IMPORTANT: the apr/apy are aproximations since the number of blocks per day is hard-coded to 7200 (Compound does the same)
# 'web3' = web3 (Node) -> Improves performance
# 'ctoken_address' = ctoken_address -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
#             {'metric': 'apr'/'apy', 'type': 'borrow', 'value': borrow_apr/borrow_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_apr(token_address, block, blockchain, web3=None, ctoken_address=None, apy=False):
    """
    :param token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param ctoken_address:
    :param apy:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    result = []
    token_address = Web3.to_checksum_address(token_address)
    if ctoken_address:
        ctoken_list = [ctoken_address]
    else:
        ctoken_list = get_ctokens_contract_list(blockchain, web3, block)

    for ctoken_address in ctoken_list:
        ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

        try:
            underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
        except (ContractLogicError, BadFunctionCallOutput):
            # cETH does not have the underlying function
            underlying_token = ZERO_ADDRESS

        if underlying_token == token_address:
            # blocks_per_day is an aproximation (5 blocks per minute)
            blocks_per_day = 7200
            days_per_year = 365
            mantissa = Decimal(10 ** 18)
            seconds_per_year = 31536000

            supply_rate_per_block = ctoken_contract.functions.supplyRatePerBlock().call(block_identifier=block)
            borrow_rate_per_block = ctoken_contract.functions.borrowRatePerBlock().call(block_identifier=block)

            metric = 'apy'
            supply = (((supply_rate_per_block / mantissa * blocks_per_day + 1) ** days_per_year) - 1)
            borrow = (((borrow_rate_per_block / mantissa * blocks_per_day + 1) ** days_per_year) - 1)

            if not apy:
                metric = 'apr'
                supply = ((1 + supply) ** Decimal(1 / seconds_per_year) - 1) * seconds_per_year
                borrow = ((1 + borrow) ** Decimal(1 / seconds_per_year) - 1) * seconds_per_year

            result = [{'metric': metric, 'type': 'supply', 'value': supply},
                      {'metric': metric, 'type': 'borrow', 'value': borrow}]
            break

    return result

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_comp_apr
# IMPORTANT: the apr/apy are aproximations since the number of blocks per day is hard-coded to 7200 (Compound does the same)
# 'web3' = web3 (Node) -> Improves performance
# 'ctoken_address' = ctoken_address -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
#             {'metric': 'apr'/'apy', 'type': 'borrow', 'value': borrow_apr/borrow_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_comp_apr(token_address, block, blockchain, web3=None, ctoken_address=None, apy=False):
    """
    :param token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param ctoken_address:
    :param apy:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    result = []
    token_address = Web3.to_checksum_address(token_address)
    if ctoken_address:
        ctoken_list = [ctoken_address]
    else:
        ctoken_list = get_ctokens_contract_list(blockchain, web3, block)

    for ctoken_address in ctoken_list:
        ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

        try:
            underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
        except (ContractLogicError, BadFunctionCallOutput):
            # cETH does not have the underlying function
            underlying_token = ZERO_ADDRESS

        if underlying_token == token_address:
            # blocks_per_day is an aproximation
            blocks_per_day = 7200
            mantissa = Decimal(10 ** 18)
            days_per_year = 365
            seconds_per_year = 31536000

            comptroller_contract = get_comptroller_contract(blockchain, web3, block)
            comp_supply_speed_per_block = comptroller_contract.functions.compSupplySpeeds(ctoken_address).call(
                block_identifier=block) / mantissa
            comp_supply_per_day = comp_supply_speed_per_block * blocks_per_day

            comp_borrow_speed_per_block = comptroller_contract.functions.compBorrowSpeeds(ctoken_address).call(
                block_identifier=block) / mantissa
            comp_borrow_per_day = comp_borrow_speed_per_block * blocks_per_day

            comp_price = Decimal(prices.get_price(COMP_ETH, block, blockchain, web3=web3)[0])
            underlying_token_price = Decimal(prices.get_price(underlying_token, block, blockchain, web3=web3)[0])

            ctoken_decimals = ctoken_contract.functions.decimals().call()
            underlying_decimals = get_decimals(underlying_token, ETHEREUM, web3=web3)
            underlying_mantissa = 18 - ctoken_decimals + underlying_decimals

            exchange_rate = ctoken_contract.functions.exchangeRateStored().call(block_identifier=block)
            exchange_rate /= Decimal(10 ** underlying_mantissa)

            ctoken_price = underlying_token_price * exchange_rate

            ctoken_total_supply = ctoken_contract.functions.totalSupply().call(block_identifier=block)
            ctoken_total_supply /= Decimal(10 ** ctoken_decimals)

            total_borrows = ctoken_contract.functions.totalBorrows().call(block_identifier=block)
            total_borrows /= Decimal(10 ** underlying_decimals)

            metric = 'apy'
            comp_supply = ((1 + (comp_price * comp_supply_per_day) / (ctoken_total_supply * ctoken_price)) ** days_per_year) - 1
            comp_borrow = ((1 + (comp_price * comp_borrow_per_day) / (total_borrows * underlying_token_price)) ** days_per_year) - 1

            if not apy:
                metric = 'apr'
                comp_supply = ((1 + comp_supply) ** Decimal(1 / seconds_per_year) - 1) * seconds_per_year
                comp_borrow = ((1 + comp_borrow) ** Decimal(1 / seconds_per_year) - 1) * seconds_per_year

            result = [{'metric': metric, 'type': 'supply', 'value': comp_supply},
                      {'metric': metric, 'type': 'borrow', 'value': comp_borrow}]
            break

    return result
