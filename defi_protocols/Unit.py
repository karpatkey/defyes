from defi_protocols.functions import get_node, get_contract, get_decimals, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, ETHEREUM, FANTOM, BINANCE

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# VAULT
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Vault Address - Ethereum
VAULT_ETHEREUM = '0xb1cFF81b9305166ff1EFc49A129ad2AfCd7BCf19'

# Vault Address - Binance Smart Chain
VAULT_BINANCE = '0xdacfeed000e12c356fb72ab5089e7dd80ff4dd93'

# Vault Address - Fantom
VAULT_FANTOM = '0xD7A9b0D75e51bfB91c843b23FB2C19aa3B8D958e'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP REGISTRY
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP Registry Address - Ethereum
CDP_REGISTRY_ETHEREUM = '0x1a5Ff58BC3246Eb233fEA20D32b79B5F01eC650c'

# CDP Registry Address - Binance Smart Chain
CDP_REGISTRY_BINANCE = '0xE8372dcef80189c0F88631507f6466b3f60E24A4'

# CDP Registry Address - Fantom
CDP_REGISTRY_FANTOM = '0x1442bC024a92C2F96c3c1D2E9274bC4d8119d97e'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP MANAGER
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP Manager Address - Ethereum
CDP_MANAGER_ETHEREUM = '0x69FB4D4e3404Ea023F940bbC547851681e893a91'

# CDP Manager Address - Binance Smart Chain
CDP_MANAGER_BINANCE = '0x1337daC01Fc21Fa21D17914f96725f7a7b73868f'

# CDP Manager Address - Fantom
CDP_MANAGER_FANTOM = '0xD12d6082811709287AE8b6d899Ab841659075FC3'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP VIEWER
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP Viewer Address - Ethereum
CDP_VIEWER_ETHEREUM = '0x68AF7bD6F3e2fb480b251cb1b508bbb406E8e21D'

# CDP Manager Address - Fantom
CDP_VIEWER_FANTOM = '0xe1761578848E774Cad9Ddc21b705dDda0c5B2473'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Vault ABI - collaterals, getTotalDebt, liquidationFee, stabilityFee, usdp, vaultParameters
ABI_VAULT = '[{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"collaterals","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"getTotalDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"liquidationFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"stabilityFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"usdp","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"vaultParameters","outputs":[{"internalType":"contract VaultParameters","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# CDP Registry ABI - getCdpsByCollateral, getCdpsByOwner, isAlive
ABI_CDP_REGISTRY = '[{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getCdpsByCollateral","outputs":[{"components":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"internalType":"struct CDPRegistry.CDP[]","name":"cdps","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"getCdpsByOwner","outputs":[{"components":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"internalType":"struct CDPRegistry.CDP[]","name":"r","type":"tuple[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"name":"isAlive","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"}]'

# CDP Manager ABI - Q112, getCollateralUsdValue_q112, liquidationPrice_q112, usdp, utilizationRatio, vaultManagerBorrowFeeParameters, vaultManagerParameters
ABI_CDP_MANAGER = '[{"inputs":[],"name":"Q112","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"name":"getCollateralUsdValue_q112","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"name":"liquidationPrice_q112","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"usdp","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"name":"utilizationRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"vaultManagerBorrowFeeParameters","outputs":[{"internalType":"contract IVaultManagerBorrowFeeParameters","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"vaultManagerParameters","outputs":[{"internalType":"contract IVaultManagerParameters","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# Vault Manager Parameters ABI - initialCollateralRatio, liquidationRatio
ABI_VAULT_MANAGER_PARAMETERS = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"initialCollateralRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"liquidationRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Vault Manager Borrow Fee Parameters ABI - getBorrowFee
ABI_VAULT_MANAGER_BORROW_FEE_PARAMETERS = '[{"inputs":[{"internalType":"address","name":"asset","type":"address"}],"name":"getBorrowFee","outputs":[{"internalType":"uint16","name":"feeBasisPoints","type":"uint16"}],"stateMutability":"view","type":"function"}]'

# Vault Parameters ABI - tokenDebtLimit
ABI_VAULT_PARAMETERS = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"tokenDebtLimit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# CDP Viewer ABI - getCollateralParameters
ABI_CDP_VIEWER = '[{"inputs":[{"internalType":"address","name":"asset","type":"address"},{"internalType":"address","name":"owner","type":"address"}],"name":"getCollateralParameters","outputs":[{"components":[{"internalType":"uint128","name":"tokenDebtLimit","type":"uint128"},{"internalType":"uint128","name":"tokenDebt","type":"uint128"},{"internalType":"uint32","name":"stabilityFee","type":"uint32"},{"internalType":"uint32","name":"liquidationDiscount","type":"uint32"},{"internalType":"uint32","name":"devaluationPeriod","type":"uint32"},{"internalType":"uint16","name":"liquidationRatio","type":"uint16"},{"internalType":"uint16","name":"initialCollateralRatio","type":"uint16"},{"internalType":"uint16","name":"liquidationFee","type":"uint16"},{"internalType":"uint16","name":"oracleType","type":"uint16"},{"internalType":"uint16","name":"borrowFee","type":"uint16"},{"components":[{"internalType":"uint128","name":"collateral","type":"uint128"},{"internalType":"uint128","name":"debt","type":"uint128"},{"internalType":"uint256","name":"totalDebt","type":"uint256"},{"internalType":"uint32","name":"stabilityFee","type":"uint32"},{"internalType":"uint32","name":"lastUpdate","type":"uint32"},{"internalType":"uint16","name":"liquidationFee","type":"uint16"},{"internalType":"uint16","name":"oracleType","type":"uint16"}],"internalType":"struct CDPViewer.CDP","name":"cdp","type":"tuple"}],"internalType":"struct CDPViewer.CollateralParameters","name":"r","type":"tuple"}],"stateMutability":"view","type":"function"}]'


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# getVaultAddress
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vault_address(blockchain):
    """

    :param blockchain:
    :return:
    """
    if blockchain == ETHEREUM:
        return VAULT_ETHEREUM

    elif blockchain == BINANCE:
        return VAULT_BINANCE

    elif blockchain == FANTOM:
        return VAULT_FANTOM


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cdp_registry_address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cdp_registry_address(blockchain):
    """

    :param blockchain:
    :return:
    """
    if blockchain == ETHEREUM:
        return CDP_REGISTRY_ETHEREUM

    elif blockchain == BINANCE:
        return CDP_REGISTRY_BINANCE

    elif blockchain == FANTOM:
        return CDP_REGISTRY_FANTOM


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cdp_manager_address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cdp_manager_address(blockchain):
    """

    :param blockchain:
    :return:
    """
    if blockchain == ETHEREUM:
        return CDP_MANAGER_ETHEREUM

    elif blockchain == BINANCE:
        return CDP_MANAGER_BINANCE

    elif blockchain == FANTOM:
        return CDP_MANAGER_FANTOM


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cdp_viewer_address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cdp_viewer_address(blockchain):
    """

    :param blockchain:
    :return:
    """
    if blockchain == ETHEREUM:
        return CDP_VIEWER_ETHEREUM

    elif blockchain == FANTOM:
        return CDP_VIEWER_FANTOM


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cdp_viewer_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cdp_viewer_data(wallet, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param wallet:
    :param collateral_address:
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

    cdp_data = {}

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        collateral_address = web3.to_checksum_address(collateral_address)

        cdp_registry_address = get_cdp_registry_address(blockchain)
        cdp_registry_contract = get_contract(cdp_registry_address, blockchain, web3=web3, abi=ABI_CDP_REGISTRY,
                                             block=block)

        if cdp_registry_contract.functions.isAlive(collateral_address, wallet).call(block_identifier=block):

            # vault_address = getVaultAddress(blockchain)
            # vault_contract = getContract(vault_address, blockchain, web3=web3, abi=ABI_VAULT, block=block)

            cpd_viewer_address = get_cdp_viewer_address(blockchain)
            cdp_viewer_contract = get_contract(cpd_viewer_address, blockchain, web3=web3, abi=ABI_CDP_VIEWER,
                                               block=block)
            cdp_viewer_data = cdp_viewer_contract.functions.getCollateralParameters(collateral_address, wallet).call(
                block_identifier=block)

            collateral_decimals = get_decimals(collateral_address, blockchain, web3=web3)

            cdp_manager_address = get_cdp_manager_address(blockchain)
            cdp_manager_contract = get_contract(cdp_manager_address, blockchain, web3=web3, abi=ABI_CDP_MANAGER,
                                                block=block)
            q112 = cdp_manager_contract.functions.Q112().call(block_identifier=block)
            usdp_address = cdp_manager_contract.functions.usdp().call()
            usdp_decimals = get_decimals(usdp_address, blockchain, web3=web3)

            # Initial Collateral Ratio
            cdp_data['icr'] = cdp_viewer_data[6]

            # Liquidation Ratio
            cdp_data['liquidation_ratio'] = cdp_viewer_data[5]

            # Stability Fee
            # cdp_data['stability_fee'] = cdp_viewer_data[2] / 1000

            # Liquidation Fee
            # cdp_data['liquidation_fee'] = cdp_viewer_data[7]

            # Issuance fee
            # cdp_data['issuance_fee'] = cdp_viewer_data[9] / 100

            # Collateral Address
            cdp_data['collateral_address'] = collateral_address

            # Collateral Amount
            if decimals is True:
                cdp_data['collateral_amount'] = cdp_viewer_data[10][0] / (10 ** collateral_decimals)
            else:
                cdp_data['collateral_amount'] = cdp_viewer_data[10][0]

            # Debt Address
            # cdp_data['debt_address'] = usdp_address

            # Debt Amount
            if decimals is True:
                cdp_data['debt_amount'] = cdp_viewer_data[10][2] / (10 ** usdp_decimals)
            else:
                cdp_data['debt_amount'] = cdp_viewer_data[10][2]

            # Liquidation Price
            cdp_data['liquidation_price'] = cdp_manager_contract.functions.liquidationPrice_q112(collateral_address,
                                                                                                 wallet).call(
                block_identifier=block) / q112

            # Collateral USD Value
            cdp_data['collateral_usd_value'] = cdp_manager_contract.functions.getCollateralUsdValue_q112(
                collateral_address, wallet).call(block_identifier=block) / (q112 * (10 ** collateral_decimals))

            # Utilization Ratio
            # cdp_manager_contract.functions.utilizationRatio -> returns an the integer part of the Utilization Ratio
            # cdp_data['utilization_ratio'] = cdp_manager_contract.functions.utilizationRatio(collateral_address, wallet).call(block_identifier=block)
            cdp_data['utilization_ratio'] = (cdp_viewer_data[10][2] / (10 ** usdp_decimals)) * 100 / cdp_data[
                'collateral_usd_value']

            # Utilization
            # cdp_data['utilization'] = (cdp_data['debt_amount'] * 100) / (cdp_data['collateral_usd_value'] * cdp_data['icr'] / 100)

            # Debt Limit
            # cdp_data['debt_limit'] = cdp_viewer_data[0] / (10**collateral_decimals)

            # Borrowable Debt = MIN(cdp_data['collateral_usd_value']*cdp_data['icr'], cdp_data['debt_limit'] - debt of ALL cdps for a the collateral)
            # cdps = cdp_registry_contract.functions.getCdpsByCollateral(collateral_address).call(block_identifier=block)

            # debt_amount_all_cdps = 0
            # for cdp in cdps:
            #     if cdp_registry_contract.functions.isAlive(cdp[0], cdp[1]).call(block_identifier=block):
            #         debt_amount_all_cdps += vault_contract.functions.getTotalDebt(cdp[0], cdp[1]).call(block_identifier=block) / (10**usdp_decimals)

            # if (cdp_data['collateral_usd_value'] * cdp_data['icr']) <= (cdp_data['debt_limit'] - debt_amount_all_cdps):
            #     cdp_data['borrowable_debt'] = cdp_data['collateral_usd_value'] * cdp_data['icr']
            # else:
            #      cdp_data['borrowable_debt'] = cdp_data['debt_limit'] - debt_amount_all_cdps

        return cdp_data

    except GetNodeIndexError:
        return get_cdp_viewer_data(wallet, collateral_address, block, blockchain, decimals=decimals, index=0,
                                   execution=execution + 1)

    except:
        return get_cdp_viewer_data(wallet, collateral_address, block, blockchain, decimals=decimals, index=index + 1,
                                   execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_cdp_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cdp_data(wallet, collateral_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param wallet:
    :param collateral_address:
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

    cdp_data = {}

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        collateral_address = web3.to_checksum_address(collateral_address)

        cdp_registry_address = get_cdp_registry_address(blockchain)
        cdp_registry_contract = get_contract(cdp_registry_address, blockchain, web3=web3, abi=ABI_CDP_REGISTRY,
                                             block=block)

        if cdp_registry_contract.functions.isAlive(collateral_address, wallet).call(block_identifier=block):

            vault_address = get_vault_address(blockchain)
            vault_contract = get_contract(vault_address, blockchain, web3=web3, abi=ABI_VAULT, block=block)

            vault_parameters_address = vault_contract.functions.vaultParameters().call(block_identifier=block)
            vault_parameters_contract = get_contract(vault_parameters_address, blockchain, web3=web3,
                                                     abi=ABI_VAULT_PARAMETERS, block=block)

            collateral_decimals = get_decimals(collateral_address, blockchain, web3=web3)
            collateral_amount = vault_contract.functions.collaterals(collateral_address, wallet).call(
                block_identifier=block)

            usdp_address = vault_contract.functions.usdp().call()
            usdp_decimals = get_decimals(usdp_address, blockchain, web3=web3)
            debt_amount = vault_contract.functions.getTotalDebt(collateral_address, wallet).call(block_identifier=block)

            cdp_manager_address = get_cdp_manager_address(blockchain)
            cdp_manager_contract = get_contract(cdp_manager_address, blockchain, web3=web3, abi=ABI_CDP_MANAGER,
                                                block=block)
            q112 = cdp_manager_contract.functions.Q112().call(block_identifier=block)

            vault_manager_parameters_address = cdp_manager_contract.functions.vaultManagerParameters().call(
                block_identifier=block)
            vault_manager_parameters_contract = get_contract(vault_manager_parameters_address, blockchain, web3=web3,
                                                             abi=ABI_VAULT_MANAGER_PARAMETERS, block=block)

            vault_manager_borrow_fee_parameters_address = cdp_manager_contract.functions.vaultManagerBorrowFeeParameters().call(
                block_identifier=block)
            vault_manager_borrow_fee_parameters_contract = get_contract(vault_manager_borrow_fee_parameters_address,
                                                                        blockchain, web3=web3,
                                                                        abi=ABI_VAULT_MANAGER_BORROW_FEE_PARAMETERS,
                                                                        block=block)

            # Initial Collateral Ratio
            cdp_data['icr'] = vault_manager_parameters_contract.functions.initialCollateralRatio(
                collateral_address).call(block_identifier=block)

            # Liquidation Ratio
            cdp_data['liquidation_ratio'] = vault_manager_parameters_contract.functions.liquidationRatio(
                collateral_address).call(block_identifier=block)

            # Stability Fee
            cdp_data['stability_fee'] = vault_contract.functions.stabilityFee(collateral_address, wallet).call(
                block_identifier=block) / 1000

            # Liquidation Fee
            cdp_data['liquidation_fee'] = vault_contract.functions.liquidationFee(collateral_address, wallet).call(
                block_identifier=block)

            # Issuance fee
            cdp_data['issuance_fee'] = vault_manager_borrow_fee_parameters_contract.functions.getBorrowFee(
                collateral_address).call(block_identifier=block) / 100

            # Collateral Address
            cdp_data['collateral_address'] = collateral_address

            # Collateral Amount
            if decimals is True:
                cdp_data['collateral_amount'] = collateral_amount / (10 ** collateral_decimals)
            else:
                cdp_data['collateral_amount'] = collateral_amount

                # Debt Address
            cdp_data['debt_address'] = usdp_address

            # Debt Amount
            if decimals is True:
                cdp_data['debt_amount'] = debt_amount / (10 ** usdp_decimals)
            else:
                cdp_data['debt_amount'] = debt_amount

            # Liquidation Price
            cdp_data['liquidation_price'] = cdp_manager_contract.functions.liquidationPrice_q112(collateral_address,
                                                                                                 wallet).call(
                block_identifier=block) / q112

            # Collateral USD Value
            cdp_data['collateral_usd_value'] = cdp_manager_contract.functions.getCollateralUsdValue_q112(
                collateral_address, wallet).call(block_identifier=block) / (q112 * 10 ** collateral_decimals)

            # Utilization Ratio
            # cdp_manager_contract.functions.utilizationRatio -> returns an the integer part of the Utilization Ratio
            # cdp_data['utilization_ratio'] = cdp_manager_contract.functions.utilizationRatio(collateral_address, wallet).call(block_identifier=block)
            cdp_data['utilization_ratio'] = (debt_amount / (10 ** usdp_decimals)) * 100 / cdp_data[
                'collateral_usd_value']

            # Utilization
            cdp_data['utilization'] = ((debt_amount / (10 ** usdp_decimals)) * 100) / (
                        cdp_data['collateral_usd_value'] * cdp_data['icr'] / 100)

            # Debt Limit
            debt_limit = vault_parameters_contract.functions.tokenDebtLimit(collateral_address).call(
                block_identifier=block)
            if decimals is True:
                cdp_data['debt_limit'] = debt_limit / (10 ** usdp_decimals)
            else:
                cdp_data['debt_limit'] = debt_limit

            # Borrowable Debt = MIN(cdp_data['collateral_usd_value']*cdp_data['icr'], cdp_data['debt_limit'] - debt of ALL cdps for a the collateral)
            cdps = cdp_registry_contract.functions.getCdpsByCollateral(collateral_address).call(block_identifier=block)

            debt_amount_all_cdps = 0
            for cdp in cdps:
                if cdp_registry_contract.functions.isAlive(cdp[0], cdp[1]).call(block_identifier=block):
                    debt_amount_all_cdps += vault_contract.functions.getTotalDebt(cdp[0], cdp[1]).call(
                        block_identifier=block) / (10 ** usdp_decimals)

            if (cdp_data['collateral_usd_value'] * cdp_data['icr']) <= (
                    (debt_limit / (10 ** usdp_decimals)) - debt_amount_all_cdps):
                if decimals is True:
                    cdp_data['borrowable_debt'] = cdp_data['collateral_usd_value'] * cdp_data['icr']
                else:
                    cdp_data['borrowable_debt'] = cdp_data['collateral_usd_value'] * cdp_data['icr'] * (
                                10 ** usdp_decimals)
            else:
                if decimals is True:
                    cdp_data['borrowable_debt'] = (debt_limit / (10 ** usdp_decimals)) - debt_amount_all_cdps
                else:
                    cdp_data['borrowable_debt'] = ((debt_limit / (10 ** usdp_decimals)) - debt_amount_all_cdps) * (
                                10 ** usdp_decimals)

        return cdp_data

    except GetNodeIndexError:
        return get_cdp_data(wallet, collateral_address, block, blockchain, decimals=decimals, index=0,
                            execution=execution + 1)

    except:
        return get_cdp_data(wallet, collateral_address, block, blockchain, decimals=decimals, index=index + 1,
                            execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with N elements, where N = number of CDPs for the wallet:
# 1 - List of Tuples: [[collateral_addressN, collateral_amountN], [debt_addressN, -debt_amountN]]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, block, blockchain, web3=None, execution=1, index=0, decimals=True):
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
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    result = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        cdp_registry_address = get_cdp_registry_address(blockchain)
        cdp_registry_contract = get_contract(cdp_registry_address, blockchain, web3=web3, abi=ABI_CDP_REGISTRY,
                                             block=block)

        cdps = cdp_registry_contract.functions.getCdpsByOwner(wallet).call(block_identifier=block)

        if len(cdps) == 0:
            return result
        else:
            vault_address = get_vault_address(blockchain)
            vault_contract = get_contract(vault_address, blockchain, web3=web3, abi=ABI_VAULT, block=block)

            usdp_address = vault_contract.functions.usdp().call()

            if decimals is True:
                usdp_decimals = get_decimals(usdp_address, blockchain, web3=web3)
            else:
                usdp_decimals = 0

            for cdp in cdps:

                if cdp_registry_contract.functions.isAlive(cdp[0], wallet).call(block_identifier=block):

                    if decimals is True:
                        collateral_decimals = get_decimals(cdp[0], blockchain, web3=web3)
                    else:
                        collateral_decimals = 0

                    collateral_amount = vault_contract.functions.collaterals(cdp[0], wallet).call(
                        block_identifier=block) / (10 ** collateral_decimals)

                    debt_amount = -1 * vault_contract.functions.getTotalDebt(cdp[0], wallet).call(
                        block_identifier=block) / (10 ** usdp_decimals)

                    result.append([[cdp[0], collateral_amount], [usdp_address, debt_amount]])

            return result

    except GetNodeIndexError:
        return underlying(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)
