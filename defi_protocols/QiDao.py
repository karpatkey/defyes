from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, get_decimals, timestamp_to_block, block_to_timestamp, to_token_amount
from defi_protocols.constants import XDAI, GnosisTokenAddr, POLYGON, MAI_POL

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# QIDAO_VAULTS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# QiDao Vaults List
QIDAO_VAULTS = {
    GnosisTokenAddr.GNO: {
        'blockchain': XDAI,
        'address': '0x014A177E9642d1b4E970418f894985dC1b85657f'  # GNO Vault Address
        },
    GnosisTokenAddr.WETH:
    {
        'blockchain': XDAI,
        'address': '0x5c49b268c9841AFF1Cc3B0a418ff5c3442eE3F3b'  # WETH Vault Address
    }
}


# 1inch Polygon Oracle Address
ORACLE_1INCH_POLYGON = '0x7F069df72b7A39bCE9806e3AfaF579E54D8CF2b9'

# POLYGON - MATIC/USD Pair - Chainlink Price Feed
CHAINLINK_MATIC_USD = '0xAB594600376Ec9fD91F8e885dADF0CE036862dE0'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Vault ABI - _minimumCollateralPercentage, checkCollateralPercentage, exists, getDebtCeiling, getEthPriceSource, getTokenPriceSource, mai, priceSourceDecimals, vaultCollateral, vaultDebt
ABI_VAULT = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"_minimumCollateralPercentage","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"checkCollateralPercentage","inputs":[{"type":"uint256","name":"vaultID","internalType":"uint256"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"exists","inputs":[{"type":"uint256","name":"vaultID","internalType":"uint256"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getDebtCeiling","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getEthPriceSource","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"getTokenPriceSource","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"contract ERC20Detailed"}],"name":"mai","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"priceSourceDecimals","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"vaultCollateral","inputs":[{"type":"uint256","name":"","internalType":"uint256"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"vaultDebt","inputs":[{"type":"uint256","name":"","internalType":"uint256"}],"constant":true}]'

# Oracle ABI - connectors, oracles, getRate, getRateToEth
ABI_ORACLE = '[{"inputs":[],"name":"connectors","outputs":[{"internalType":"contract IERC20[]","name":"allConnectors","type":"address[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"oracles","outputs":[{"internalType":"contract IOracle[]","name":"allOracles","type":"address[]"},{"internalType":"enum OffchainOracle.OracleType[]","name":"oracleTypes","type":"uint8[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"contract IERC20","name":"srcToken","type":"address"},{"internalType":"contract IERC20","name":"dstToken","type":"address"},{"internalType":"bool","name":"useWrappers","type":"bool"}],"name":"getRate","outputs":[{"internalType":"uint256","name":"weightedRate","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"contract IERC20","name":"srcToken","type":"address"},{"internalType":"bool","name":"useSrcWrappers","type":"bool"}],"name":"getRateToEth","outputs":[{"internalType":"uint256","name":"weightedRate","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# ChainLink Price Feed ABI - latestAnswer, decimals
ABI_CHAINLINK_PRICE_FEED = '[{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vault_address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vault_address(collateral_address, blockchain):
    """
    :param collateral_address:
    :param blockchain:
    :return:
    """
    vault_address = None
    try:
        if QIDAO_VAULTS[collateral_address]['blockchain'] == blockchain:
            vault_address = QIDAO_VAULTS[collateral_address]['address']
    except KeyError:
        pass

    return vault_address


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vault_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vault_data(vault_id, collateral_address, block, blockchain, web3=None, decimals=True):
    """
    :param vault_id:
    :param collateral_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    vault_data = {}

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    collateral_address = Web3.to_checksum_address(collateral_address)

    vault_address = get_vault_address(collateral_address, blockchain)

    if vault_address is not None:
        vault_contract = get_contract(vault_address, blockchain, web3=web3, abi=ABI_VAULT, block='latest')

        if vault_contract.functions.exists(vault_id).call(block_identifier=block):

            debt_address = vault_contract.functions.mai().call()
            vault_collateral = vault_contract.functions.vaultCollateral(vault_id).call(block_identifier=block)
            vault_debt = vault_contract.functions.vaultDebt(vault_id).call(block_identifier=block)

            price_source_decimals = vault_contract.functions.priceSourceDecimals().call()

            # Collateral Address
            vault_data['collateral_address'] = collateral_address
            # Collateral Amount
            vault_data['collateral_amount'] = to_token_amount(collateral_address, vault_collateral, blockchain, web3, decimals)
            # Collateral Token USD Value
            vault_data['collateral_token_usd_value'] = Decimal(vault_contract.functions.getEthPriceSource().call(block_identifier=block))
            vault_data['collateral_token_usd_value'] /= Decimal(10 ** price_source_decimals)
            # Debt Address
            vault_data['debt_address'] = debt_address
            # Debt Amount
            vault_data['debt_amount'] = to_token_amount(debt_address, vault_debt, blockchain, web3, decimals)

            # Debt Token USD Value
            # getTokenPriceSource() always returns MAI price = 1 USD. This is the price QiDao uses to calculate the Collateral Ratio.
            # MAI price might have depegged from USD so afterwards vault_data['debt_token_usd_value'] is overwritten with the price obtained from 1inch
            vault_data['debt_token_usd_value'] = Decimal(vault_contract.functions.getTokenPriceSource().call(block_identifier=block))
            vault_data['debt_token_usd_value'] /= Decimal(10 ** price_source_decimals)

            # Debt USD Value
            if vault_debt != 0:
                vault_data['debt_usd_value'] = vault_data['debt_token_usd_value'] * Decimal(vault_debt) / Decimal(10 ** debt_decimals)
            else:
                vault_data['debt_usd_value'] = Decimal(0)

            # Collateral Ratio
            if vault_debt != 0:
                vault_data['collateral_ratio'] = vault_data['collateral_amount'] * vault_data['collateral_token_usd_value']
                vault_data['collateral_ratio'] /= vault_data['debt_usd_value'] * 100
            else:
                vault_data['collateral_ratio'] = Decimal('infinity')

            # Available Debt Amount to Borrow
            vault_data['available_debt_amount'] = to_token_amount(debt_address,
                                                                  vault_contract.functions.getDebtCeiling().call(block_identifier=block),
                                                                  blockchain,
                                                                  web3,
                                                                  decimals)
            # Liquidation Ratio
            vault_data['liquidation_ratio'] = vault_contract.functions._minimumCollateralPercentage().call(block_identifier=block)
            # Liquidation Price
            if vault_debt != 0:
                vault_data['liquidation_price'] = Decimal(vault_data['liquidation_ratio'] / 100) * vault_data['debt_usd_value'] / vault_data['collateral_amount']
            else:
                vault_data['liquidation_price'] = Decimal('nan')

            # Debt Token USD Value from Polygon Chainlink feed
            block_polygon = timestamp_to_block(block_to_timestamp(block, blockchain), POLYGON)

            price_feed_contract = get_contract(CHAINLINK_MATIC_USD, POLYGON, abi=ABI_CHAINLINK_PRICE_FEED, block=block_polygon)
            price_feed_decimals = price_feed_contract.functions.decimals().call()
            matic_usd_price = Decimal(price_feed_contract.functions.latestAnswer().call(block_identifier=block_polygon))
            matic_usd_price /= Decimal(10 ** price_feed_decimals)

            oracle_contract = get_contract(ORACLE_1INCH_POLYGON, POLYGON, abi=ABI_ORACLE, block=block_polygon)
            rate = Decimal(oracle_contract.functions.getRateToEth(MAI_POL, False).call(block_identifier=block_polygon))
            rate /= Decimal(10 ** abs(18 + 18 - get_decimals(debt_address, blockchain, web3=web3)))

            vault_data['debt_token_usd_value'] = matic_usd_price * rate

    return vault_data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(vault_id, collateral_address, block, blockchain, web3=None, decimals=True):
    """
    :param vault_id:
    :param collateral_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    result = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    collateral_address = Web3.to_checksum_address(collateral_address)
    vault_address = get_vault_address(collateral_address, blockchain)

    if vault_address is not None:
        vault_contract = get_contract(vault_address, blockchain, web3=web3, abi=ABI_VAULT, block=block)

        if vault_contract.functions.exists(vault_id).call(block_identifier=block):

            collateral_decimals = get_decimals(collateral_address, blockchain, web3=web3) if decimals else 0

            collateral_amount = Decimal(vault_contract.functions.vaultCollateral(vault_id).call(block_identifier=block))
            collateral_amount /= Decimal(10 ** collateral_decimals)

            result.append([collateral_address, collateral_amount])

            debt_address = vault_contract.functions.mai().call()
            debt_decimals = get_decimals(debt_address, blockchain, web3=web3) if decimals else 0

            debt_amount = -1 * Decimal(vault_contract.functions.vaultDebt(vault_id).call(block_identifier=block))
            debt_amount /= Decimal(10 ** debt_decimals)

            result.append([debt_address, debt_amount])

    return result
