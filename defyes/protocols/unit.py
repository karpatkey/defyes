from decimal import Decimal

from defabipedia import Chain
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, get_decimals

# VAULT
# Vault Address - Ethereum
VAULT_ETHEREUM = "0xb1cFF81b9305166ff1EFc49A129ad2AfCd7BCf19"

# Vault Address - Binance Smart Chain
VAULT_BINANCE = "0xdacfeed000e12c356fb72ab5089e7dd80ff4dd93"

# Vault Address - Fantom
VAULT_FANTOM = "0xD7A9b0D75e51bfB91c843b23FB2C19aa3B8D958e"

# CDP REGISTRY
# CDP Registry Address - Ethereum
CDP_REGISTRY_ETHEREUM = "0x1a5Ff58BC3246Eb233fEA20D32b79B5F01eC650c"

# CDP Registry Address - Binance Smart Chain
CDP_REGISTRY_BINANCE = "0xE8372dcef80189c0F88631507f6466b3f60E24A4"

# CDP Registry Address - Fantom
CDP_REGISTRY_FANTOM = "0x1442bC024a92C2F96c3c1D2E9274bC4d8119d97e"

# CDP MANAGER
# CDP Manager Address - Ethereum
CDP_MANAGER_ETHEREUM = "0x69FB4D4e3404Ea023F940bbC547851681e893a91"

# CDP Manager Address - Binance Smart Chain
CDP_MANAGER_BINANCE = "0x1337daC01Fc21Fa21D17914f96725f7a7b73868f"

# CDP Manager Address - Fantom
CDP_MANAGER_FANTOM = "0xD12d6082811709287AE8b6d899Ab841659075FC3"

# CDP VIEWER
# CDP Viewer Address - Ethereum
CDP_VIEWER_ETHEREUM = "0x68AF7bD6F3e2fb480b251cb1b508bbb406E8e21D"

# CDP Manager Address - Fantom
CDP_VIEWER_FANTOM = "0xe1761578848E774Cad9Ddc21b705dDda0c5B2473"

# ABIs
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


def get_vault_address(blockchain):
    if blockchain == Chain.ETHEREUM:
        return VAULT_ETHEREUM

    elif blockchain == Chain.BINANCE:
        return VAULT_BINANCE

    elif blockchain == Chain.FANTOM:
        return VAULT_FANTOM


def get_cdp_registry_address(blockchain):
    if blockchain == Chain.ETHEREUM:
        return CDP_REGISTRY_ETHEREUM

    elif blockchain == Chain.BINANCE:
        return CDP_REGISTRY_BINANCE

    elif blockchain == Chain.FANTOM:
        return CDP_REGISTRY_FANTOM


def get_cdp_manager_address(blockchain):
    if blockchain == Chain.ETHEREUM:
        return CDP_MANAGER_ETHEREUM

    elif blockchain == Chain.BINANCE:
        return CDP_MANAGER_BINANCE

    elif blockchain == Chain.FANTOM:
        return CDP_MANAGER_FANTOM


def get_cdp_viewer_address(blockchain):
    if blockchain == Chain.ETHEREUM:
        return CDP_VIEWER_ETHEREUM

    elif blockchain == Chain.FANTOM:
        return CDP_VIEWER_FANTOM


def get_cdp_viewer_data(wallet, collateral_address, block, blockchain, web3=None, decimals=True):
    cdp_data = {}

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    collateral_address = Web3.to_checksum_address(collateral_address)

    cdp_registry_address = get_cdp_registry_address(blockchain)
    cdp_registry_contract = get_contract(cdp_registry_address, blockchain, web3=web3, abi=ABI_CDP_REGISTRY)

    if cdp_registry_contract.functions.isAlive(collateral_address, wallet).call(block_identifier=block):
        # vault_address = getVaultAddress(blockchain)
        # vault_contract = getContract(vault_address, blockchain, web3=web3, abi=ABI_VAULT, block=block)

        cpd_viewer_address = get_cdp_viewer_address(blockchain)
        cdp_viewer_contract = get_contract(cpd_viewer_address, blockchain, web3=web3, abi=ABI_CDP_VIEWER)
        cdp_viewer_data = cdp_viewer_contract.functions.getCollateralParameters(collateral_address, wallet).call(
            block_identifier=block
        )

        collateral_decimals = get_decimals(collateral_address, blockchain, web3=web3)

        cdp_manager_address = get_cdp_manager_address(blockchain)
        cdp_manager_contract = get_contract(cdp_manager_address, blockchain, web3=web3, abi=ABI_CDP_MANAGER)
        q112 = Decimal(cdp_manager_contract.functions.Q112().call(block_identifier=block))
        usdp_address = const_call(cdp_manager_contract.functions.usdp())
        usdp_decimals = get_decimals(usdp_address, blockchain, web3=web3)

        # Initial Collateral Ratio
        cdp_data["icr"] = cdp_viewer_data[6]

        # Liquidation Ratio
        cdp_data["liquidation_ratio"] = cdp_viewer_data[5]

        # Stability Fee
        # cdp_data['stability_fee'] = cdp_viewer_data[2] / 1000

        # Liquidation Fee
        # cdp_data['liquidation_fee'] = cdp_viewer_data[7]

        # Issuance fee
        # cdp_data['issuance_fee'] = cdp_viewer_data[9] / 100

        # Collateral Address
        cdp_data["collateral_address"] = collateral_address

        # Collateral Amount
        cdp_data["collateral_amount"] = Decimal(cdp_viewer_data[10][0]) / Decimal(
            10 ** (collateral_decimals if decimals else 0)
        )

        # Debt Address
        # cdp_data['debt_address'] = usdp_address

        # Debt Amount
        cdp_data["debt_amount"] = Decimal(cdp_viewer_data[10][2]) / Decimal(10 ** (usdp_decimals if decimals else 0))

        # Liquidation Price
        cdp_data["liquidation_price"] = (
            Decimal(
                cdp_manager_contract.functions.liquidationPrice_q112(collateral_address, wallet).call(
                    block_identifier=block
                )
            )
            / q112
        )

        # Collateral USD Value
        cdp_data["collateral_usd_value"] = Decimal(
            cdp_manager_contract.functions.getCollateralUsdValue_q112(collateral_address, wallet).call(
                block_identifier=block
            )
        ) / (q112 * Decimal(10**collateral_decimals))

        # Utilization Ratio
        # cdp_manager_contract.functions.utilizationRatio -> returns an the integer part of the Utilization Ratio
        # cdp_data['utilization_ratio'] = cdp_manager_contract.functions.utilizationRatio(collateral_address, wallet).call(block_identifier=block)
        cdp_data["utilization_ratio"] = (
            (Decimal(cdp_viewer_data[10][2]) / Decimal(10**usdp_decimals))
            * Decimal(100)
            / cdp_data["collateral_usd_value"]
        )

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


def get_cdp_data(wallet, collateral_address, block, blockchain, web3=None, decimals=True):
    cdp_data = {}

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    collateral_address = Web3.to_checksum_address(collateral_address)

    cdp_registry_address = get_cdp_registry_address(blockchain)
    cdp_registry_contract = get_contract(cdp_registry_address, blockchain, web3=web3, abi=ABI_CDP_REGISTRY)

    if cdp_registry_contract.functions.isAlive(collateral_address, wallet).call(block_identifier=block):
        vault_address = get_vault_address(blockchain)
        vault_contract = get_contract(vault_address, blockchain, web3=web3, abi=ABI_VAULT)

        vault_parameters_address = vault_contract.functions.vaultParameters().call(block_identifier=block)
        vault_parameters_contract = get_contract(
            vault_parameters_address, blockchain, web3=web3, abi=ABI_VAULT_PARAMETERS
        )

        collateral_decimals = get_decimals(collateral_address, blockchain, web3=web3)
        collateral_amount = vault_contract.functions.collaterals(collateral_address, wallet).call(
            block_identifier=block
        )

        usdp_address = const_call(vault_contract.functions.usdp())
        usdp_decimals = get_decimals(usdp_address, blockchain, web3=web3)
        debt_amount = vault_contract.functions.getTotalDebt(collateral_address, wallet).call(block_identifier=block)

        cdp_manager_address = get_cdp_manager_address(blockchain)
        cdp_manager_contract = get_contract(cdp_manager_address, blockchain, web3=web3, abi=ABI_CDP_MANAGER)
        q112 = cdp_manager_contract.functions.Q112().call(block_identifier=block)

        vault_manager_parameters_address = cdp_manager_contract.functions.vaultManagerParameters().call(
            block_identifier=block
        )
        vault_manager_parameters_contract = get_contract(
            vault_manager_parameters_address, blockchain, web3=web3, abi=ABI_VAULT_MANAGER_PARAMETERS
        )

        vault_manager_borrow_fee_parameters_address = (
            cdp_manager_contract.functions.vaultManagerBorrowFeeParameters().call(block_identifier=block)
        )
        vault_manager_borrow_fee_parameters_contract = get_contract(
            vault_manager_borrow_fee_parameters_address,
            blockchain,
            web3=web3,
            abi=ABI_VAULT_MANAGER_BORROW_FEE_PARAMETERS,
        )

        # Initial Collateral Ratio
        cdp_data["icr"] = vault_manager_parameters_contract.functions.initialCollateralRatio(collateral_address).call(
            block_identifier=block
        )

        # Liquidation Ratio
        cdp_data["liquidation_ratio"] = vault_manager_parameters_contract.functions.liquidationRatio(
            collateral_address
        ).call(block_identifier=block)

        # Stability Fee
        cdp_data["stability_fee"] = (
            Decimal(vault_contract.functions.stabilityFee(collateral_address, wallet).call(block_identifier=block))
            / 1000
        )

        # Liquidation Fee
        cdp_data["liquidation_fee"] = vault_contract.functions.liquidationFee(collateral_address, wallet).call(
            block_identifier=block
        )

        # Issuance fee
        cdp_data["issuance_fee"] = (
            Decimal(
                vault_manager_borrow_fee_parameters_contract.functions.getBorrowFee(collateral_address).call(
                    block_identifier=block
                )
            )
            / 100
        )

        # Collateral Address
        cdp_data["collateral_address"] = collateral_address

        # Collateral Amount
        cdp_data["collateral_amount"] = Decimal(collateral_amount) / Decimal(
            10 ** (collateral_decimals if decimals else 0)
        )

        # Debt Address
        cdp_data["debt_address"] = usdp_address

        # Debt Amount
        cdp_data["debt_amount"] = Decimal(debt_amount) / Decimal(10 ** (usdp_decimals if decimals else 0))

        # Liquidation Price
        cdp_data["liquidation_price"] = Decimal(
            cdp_manager_contract.functions.liquidationPrice_q112(collateral_address, wallet).call(
                block_identifier=block
            )
        ) / Decimal(q112)

        # Collateral USD Value
        cdp_data["collateral_usd_value"] = Decimal(
            cdp_manager_contract.functions.getCollateralUsdValue_q112(collateral_address, wallet).call(
                block_identifier=block
            )
        ) / (Decimal(q112) * Decimal(10**collateral_decimals))

        # Utilization Ratio
        # cdp_manager_contract.functions.utilizationRatio -> returns an the integer part of the Utilization Ratio
        # cdp_data['utilization_ratio'] = cdp_manager_contract.functions.utilizationRatio(collateral_address, wallet).call(block_identifier=block)
        cdp_data["utilization_ratio"] = (
            Decimal(100) * (Decimal(debt_amount) / Decimal(10**usdp_decimals)) / cdp_data["collateral_usd_value"]
        )

        # Utilization
        cdp_data["utilization"] = ((Decimal(debt_amount) / Decimal(10**usdp_decimals)) * Decimal(100)) / (
            cdp_data["collateral_usd_value"] * Decimal(cdp_data["icr"]) / Decimal(100)
        )

        # Debt Limit
        debt_limit = vault_parameters_contract.functions.tokenDebtLimit(collateral_address).call(block_identifier=block)
        cdp_data["debt_limit"] = Decimal(debt_limit) / Decimal(10 ** (usdp_decimals if decimals else 0))

        # Borrowable Debt = MIN(cdp_data['collateral_usd_value']*cdp_data['icr'], cdp_data['debt_limit'] - debt of ALL cdps for a the collateral)
        cdps = cdp_registry_contract.functions.getCdpsByCollateral(collateral_address).call(block_identifier=block)

        debt_amount_all_cdps = Decimal(0)
        for cdp in cdps:
            if cdp_registry_contract.functions.isAlive(cdp[0], cdp[1]).call(block_identifier=block):
                debt_amount_all_cdps += Decimal(
                    vault_contract.functions.getTotalDebt(cdp[0], cdp[1]).call(block_identifier=block)
                ) / Decimal(10**usdp_decimals)

        if (cdp_data["collateral_usd_value"] * Decimal(cdp_data["icr"])) <= (
            (Decimal(debt_limit) / Decimal(10**usdp_decimals)) - debt_amount_all_cdps
        ):
            cdp_data["borrowable_debt"] = (
                cdp_data["collateral_usd_value"]
                * Decimal(cdp_data["icr"])
                * Decimal(10 ** (0 if decimals else usdp_decimals))
            )
        else:
            cdp_data["borrowable_debt"] = (
                (Decimal(debt_limit) / Decimal(10**usdp_decimals)) - debt_amount_all_cdps
            ) * Decimal(10 ** (0 if decimals else usdp_decimals))

    return cdp_data


# Output: a list with N elements, where N = number of CDPs for the wallet:
# 1 - List of Tuples: [[collateral_addressN, collateral_amountN], [debt_addressN, -debt_amountN]]
def underlying(wallet, block, blockchain, web3=None, decimals=True):
    result = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    cdp_registry_address = get_cdp_registry_address(blockchain)
    cdp_registry_contract = get_contract(cdp_registry_address, blockchain, web3=web3, abi=ABI_CDP_REGISTRY)

    cdps = cdp_registry_contract.functions.getCdpsByOwner(wallet).call(block_identifier=block)

    if len(cdps) == 0:
        return result
    else:
        vault_address = get_vault_address(blockchain)
        vault_contract = get_contract(vault_address, blockchain, web3=web3, abi=ABI_VAULT)

        usdp_address = const_call(vault_contract.functions.usdp())

        usdp_decimals = get_decimals(usdp_address, blockchain, web3=web3) if decimals else 0

        for cdp in cdps:
            if cdp_registry_contract.functions.isAlive(cdp[0], wallet).call(block_identifier=block):
                collateral_decimals = get_decimals(cdp[0], blockchain, web3=web3) if decimals else 0

                collateral_amount = Decimal(
                    vault_contract.functions.collaterals(cdp[0], wallet).call(block_identifier=block)
                ) / Decimal(10**collateral_decimals)

                debt_amount = (
                    Decimal(-1)
                    * Decimal(vault_contract.functions.getTotalDebt(cdp[0], wallet).call(block_identifier=block))
                    / Decimal(10**usdp_decimals)
                )

                result.append([[cdp[0], collateral_amount], [usdp_address, debt_amount]])

        return result
