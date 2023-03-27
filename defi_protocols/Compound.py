from defi_protocols.functions import get_node, get_contract, get_decimals, balance_of, GetNodeIndexError
from defi_protocols.constants import ETHEREUM, COMP_ETH, MAX_EXECUTIONS, ZERO_ADDRESS
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
ABI_CTOKEN = '[{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"exchangeRateStored","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"underlying","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"borrowBalanceStored","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"supplyRatePerBlock","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[],"name":"borrowRatePerBlock","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalBorrows","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

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


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_ctoken_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'ctoken_contract' = ctoken_contract -> Improves performance
# 'underlying_token' = underlying_token -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ctoken_data(ctoken_address, wallet, block, blockchain, web3=None, execution=1, index=0, ctoken_contract=None,
                    underlying_token=None):
    """

    :param ctoken_address:
    :param wallet:
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

        ctoken_data = {}

        if ctoken_contract is not None:
            ctoken_data['contract'] = ctoken_contract
        else:
            ctoken_data['contract'] = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

        if underlying_token is not None:
            ctoken_data['underlying'] = underlying_token
        else:
            try:
                ctoken_data['underlying'] = ctoken_data['contract'].functions.underlying().call(block_identifier=block)
            except:
                ctoken_data['underlying'] = ZERO_ADDRESS

        ctoken_data['decimals'] = ctoken_data['contract'].functions.decimals().call()
        ctoken_data['borrowBalanceStored'] = ctoken_data['contract'].functions.borrowBalanceStored(wallet).call(
            block_identifier=block)
        ctoken_data['balanceOf'] = ctoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)
        ctoken_data['exchangeRateStored'] = ctoken_data['contract'].functions.exchangeRateStored().call(
            block_identifier=block)

        return ctoken_data

    except GetNodeIndexError:
        return get_ctoken_data(ctoken_address, wallet, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_ctoken_data(ctoken_address, wallet, block, blockchain, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
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

        comptroller_address = get_comptoller_address(blockchain)
        if comptroller_address is None:
            return None

        comptroller_contract = get_contract(comptroller_address, blockchain, web3=web3, abi=ABI_COMPTROLLER,
                                            block=block)

        ctoken_list = comptroller_contract.functions.getAllMarkets().call()

        found = False
        for ctoken_address in ctoken_list:

            ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

            try:
                underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
            except:
                # cETH does not have the underlying function
                underlying_token = ZERO_ADDRESS

            if underlying_token == token_address:
                found = True
                break

        if not found:
            return []

        ctoken_data = get_ctoken_data(ctoken_address, wallet, block, blockchain, web3=web3,
                                      ctoken_contract=ctoken_contract, underlying_token=underlying_token)

        underlying_token_decimals = get_decimals(token_address, block=block, blockchain=blockchain, web3=web3,
                                                 index=index)

        mantissa = 18 - (ctoken_data['decimals']) + underlying_token_decimals

        exchange_rate = ctoken_data['exchangeRateStored'] / (10 ** mantissa)

        underlying_token_balance = ctoken_data['balanceOf'] / (10 ** ctoken_data['decimals']) * exchange_rate - \
                                   ctoken_data['borrowBalanceStored'] / (10 ** underlying_token_decimals)

        if decimals == False:
            underlying_token_balance = underlying_token_balance * (10 ** underlying_token_decimals)

        balances.append([token_address, underlying_token_balance])

        return balances

    except GetNodeIndexError:
        return underlying(wallet, token_address, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, token_address, block, blockchain, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying_all
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying_all(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False):
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
    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        comptroller_address = get_comptoller_address(blockchain)
        if comptroller_address is None:
            return None

        comptroller_contract = get_contract(comptroller_address, blockchain, web3=web3, abi=ABI_COMPTROLLER,
                                            block=block)

        assets_list = []
        ctoken_list = comptroller_contract.functions.getAllMarkets().call()
        for ctoken_address in ctoken_list:
            if balance_of(wallet, ctoken_address, block, blockchain, web3=web3) > 0:
                assets_list.append(ctoken_address)

        for ctoken_address in assets_list:

            ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

            try:
                underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
            except:
                # cETH does not have the underlying function
                underlying_token = ZERO_ADDRESS

            if underlying_token is not ZERO_ADDRESS:
                ctoken_data = get_ctoken_data(ctoken_address, wallet, block, blockchain, web3=web3,
                                              ctoken_contract=ctoken_contract, underlying_token=underlying_token)

                underlying_token_decimals = get_decimals(underlying_token, block=block, blockchain=blockchain,
                                                         web3=web3, index=index)

                mantissa = 18 - (ctoken_data['decimals']) + underlying_token_decimals

                exchange_rate = ctoken_data['exchangeRateStored'] / (10 ** mantissa)

                underlying_token_balance = ctoken_data['balanceOf'] / (10 ** ctoken_data['decimals']) * exchange_rate - \
                                           ctoken_data['borrowBalanceStored'] / (10 ** underlying_token_decimals)

                if decimals == False:
                    underlying_token_balance = underlying_token_balance * (10 ** underlying_token_decimals)

                balances.append([underlying_token, underlying_token_balance])

        if reward is True:
            all_rewards = all_comp_rewards(wallet, block, blockchain, web3=web3, decimals=decimals)
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
# all_comp_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def all_comp_rewards(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True):
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

        compound_lens_address = get_compound_lens_address(blockchain)
        if compound_lens_address is None:
            return None

        compound_lens_contract = get_contract(compound_lens_address, blockchain, web3=web3, abi=ABI_COMPOUND_LENS,
                                              block=block)

        comp_token_address = get_compound_token_address(blockchain)
        if comp_token_address is None:
            return None

        comptroller_address = get_comptoller_address(blockchain)
        if comptroller_address is None:
            return None

        meta_data = compound_lens_contract.functions.getCompBalanceMetadataExt(comp_token_address, comptroller_address,
                                                                               wallet).call(block_identifier=block)
        comp_rewards = meta_data[3]

        if decimals == True:
            comp_rewards = comp_rewards / (10 ** (get_decimals(comp_token_address, blockchain, web3=web3)))

        all_rewards.append([comp_token_address, comp_rewards])

        return all_rewards

    except GetNodeIndexError:
        return all_comp_rewards(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return all_comp_rewards(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(ctoken_amount, ctoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param ctoken_amount:
    :param ctoken_address:
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

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        ctoken_contract = get_contract(ctoken_address, blockchain, abi=ABI_CTOKEN, web3=web3, block=block)
        ctoken_decimals = ctoken_contract.functions.decimals().call()
        exchange_rate = ctoken_contract.functions.exchangeRateStored().call(block_identifier=block)

        try:
            underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
        except:
            # cETH does not have the underlying function
            underlying_token = ZERO_ADDRESS

        if decimals == True:
            underlying_token_decimals = get_decimals(underlying_token, blockchain, web3=web3)
        else:
            underlying_token_decimals = 0

        underlying_token_balance = ctoken_amount * exchange_rate / (
                    10 ** (18 - ctoken_decimals + underlying_token_decimals))

        return [underlying_token, underlying_token_balance]

    except GetNodeIndexError:
        return unwrap(ctoken_amount, ctoken_address, block, blockchain, decimals=decimals, index=0,
                      execution=execution + 1)

    except:
        return unwrap(ctoken_amount, ctoken_address, block, blockchain, decimals=decimals, index=index + 1,
                      execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_apr
# IMPORTANT: the apr/apy are aproximations since the number of blocks per day is hard-coded to 7200 (Compound does the same)
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'ctoken_address' = ctoken_address -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
#             {'metric': 'apr'/'apy', 'type': 'borrow', 'value': borrow_apr/borrow_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_apr(token_address, block, blockchain, web3=None, execution=1, index=0, ctoken_address=None, apy=False):
    """

    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param ctoken_address:
    :param apy:
    :return:
    """

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        token_address = web3.to_checksum_address(token_address)

        if ctoken_address is None:
            comptroller_address = get_comptoller_address(blockchain)
            if comptroller_address is None:
                return None

            comptroller_contract = get_contract(comptroller_address, blockchain, web3=web3, abi=ABI_COMPTROLLER,
                                                block=block)

            ctoken_list = comptroller_contract.functions.getAllMarkets().call()

            found = False
            for ctoken_address in ctoken_list:

                ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

                try:
                    underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
                except:
                    # cETH does not have the underlying function
                    underlying_token = ZERO_ADDRESS

                if underlying_token == token_address:
                    found = True
                    break

        else:
            ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

            try:
                underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
            except:
                # cETH does not have the underlying function
                underlying_token = ZERO_ADDRESS

            if underlying_token == token_address:
                found = True

        if not found:
            None

        # blocks_per_day is an aproximation (5 blocks per minute)
        blocks_per_day = 7200
        days_per_year = 365
        mantissa = 10 ** 18
        seconds_per_year = 31536000

        supply_rate_per_block = ctoken_contract.functions.supplyRatePerBlock().call(block_identifier=block)
        borrow_rate_per_block = ctoken_contract.functions.borrowRatePerBlock().call(block_identifier=block)

        supply_apy = (((supply_rate_per_block / mantissa * blocks_per_day + 1) ** days_per_year) - 1)
        borrow_apy = (((borrow_rate_per_block / mantissa * blocks_per_day + 1) ** days_per_year) - 1)

        if apy is True:
            return [{'metric': 'apy', 'type': 'supply', 'value': supply_apy},
                    {'metric': 'apy', 'type': 'borrow', 'value': borrow_apy}]
        else:
            supply_apr = ((1 + supply_apy) ** (1 / seconds_per_year) - 1) * seconds_per_year
            borrow_apr = ((1 + borrow_apy) ** (1 / seconds_per_year) - 1) * seconds_per_year

            return [{'metric': 'apr', 'type': 'supply', 'value': supply_apr},
                    {'metric': 'apr', 'type': 'borrow', 'value': borrow_apr}]

    except GetNodeIndexError:
        return get_apr(token_address, block, blockchain, ctoken_address=ctoken_address, apy=apy, index=0,
                       execution=execution + 1)

    except:
        return get_apr(token_address, block, blockchain, ctoken_address=ctoken_address, apy=apy, index=index + 1,
                       execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_comp_apr
# IMPORTANT: the apr/apy are aproximations since the number of blocks per day is hard-coded to 7200 (Compound does the same)
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'ctoken_address' = ctoken_address -> Improves performance
# 'apy' = True/False -> True = returns APY / False = returns APR
# Output: Tuple:
# 1 - Tuple: [{'metric': 'apr'/'apy', 'type': 'supply', 'value': supply_apr/supply_apy},
#             {'metric': 'apr'/'apy', 'type': 'borrow', 'value': borrow_apr/borrow_apy}]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_comp_apr(token_address, block, blockchain, web3=None, execution=1, index=0, ctoken_address=None, apy=False):
    """

    :para token_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param ctoken_address:
    :param apy:
    :return:
    """

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        token_address = web3.to_checksum_address(token_address)

        comptroller_address = get_comptoller_address(blockchain)
        if comptroller_address is None:
            return None

        comptroller_contract = get_contract(comptroller_address, blockchain, web3=web3, abi=ABI_COMPTROLLER,
                                            block=block)

        if ctoken_address is None:

            ctoken_list = comptroller_contract.functions.getAllMarkets().call()

            found = False
            for ctoken_address in ctoken_list:

                ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

                try:
                    underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
                except:
                    # cETH does not have the underlying function
                    underlying_token = ZERO_ADDRESS

                if underlying_token == token_address:
                    found = True
                    break

        else:
            ctoken_contract = get_contract(ctoken_address, blockchain, web3=web3, abi=ABI_CTOKEN, block=block)

            try:
                underlying_token = ctoken_contract.functions.underlying().call(block_identifier=block)
            except:
                underlying_token = ZERO_ADDRESS

            if underlying_token == token_address:
                found = True

        if not found:
            return None

        # blocks_per_day is an aproximation
        blocks_per_day = 7200
        mantissa = 10 ** 18
        days_per_year = 365
        seconds_per_year = 31536000

        comp_supply_speed_per_block = comptroller_contract.functions.compSupplySpeeds(ctoken_address).call(
            block_identifier=block) / mantissa
        comp_supply_per_day = comp_supply_speed_per_block * blocks_per_day

        comp_borrow_speed_per_block = comptroller_contract.functions.compBorrowSpeeds(ctoken_address).call(
            block_identifier=block) / mantissa
        comp_borrow_per_day = comp_borrow_speed_per_block * blocks_per_day

        comp_price = prices.get_price(COMP_ETH, block, blockchain, web3=web3)[0]
        underlying_token_price = prices.get_price(underlying_token, block, blockchain, web3=web3)[0]

        ctoken_decimals = ctoken_contract.functions.decimals().call()
        underlying_decimals = get_decimals(underlying_token, ETHEREUM, web3=web3)
        exchange_rate = ctoken_contract.functions.exchangeRateStored().call(block_identifier=block) / (
                    10 ** (18 - ctoken_decimals + underlying_decimals))
        ctoken_price = underlying_token_price * exchange_rate

        ctoken_total_supply = ctoken_contract.functions.totalSupply().call(block_identifier=block) / (
                    10 ** ctoken_decimals)

        total_borrows = ctoken_contract.functions.totalBorrows().call(block_identifier=block) / (
                    10 ** underlying_decimals)

        comp_supply_apy = (((1 + (comp_price * comp_supply_per_day) / (
                    ctoken_total_supply * ctoken_price))) ** days_per_year) - 1
        comp_borrow_apy = (((1 + (comp_price * comp_borrow_per_day) / (
                    total_borrows * underlying_token_price))) ** days_per_year) - 1

        if apy is True:
            return [{'metric': 'apy', 'type': 'supply', 'value': comp_supply_apy},
                    {'metric': 'apy', 'type': 'borrow', 'value': comp_borrow_apy}]
        else:
            comp_supply_apr = ((1 + comp_supply_apy) ** (1 / seconds_per_year) - 1) * seconds_per_year
            comp_borrow_apr = ((1 + comp_borrow_apy) ** (1 / seconds_per_year) - 1) * seconds_per_year

            return [{'metric': 'apr', 'type': 'supply', 'value': comp_supply_apr},
                    {'metric': 'apr', 'type': 'borrow', 'value': comp_borrow_apr}]

    except GetNodeIndexError:
        return get_comp_apr(token_address, block, blockchain, ctoken_address=ctoken_address, apy=apy, index=0,
                            execution=execution + 1)

    except:
        return get_comp_apr(token_address, block, blockchain, ctoken_address=ctoken_address, apy=apy, index=index + 1,
                            execution=execution)
