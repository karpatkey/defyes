from defi_protocols.functions import get_node, get_contract, balance_of, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, ETHEREUM, DAI_ETH
from typing import Union

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP MANAGER
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP Manager Contract Address
CDP_MANAGER_ADDRESS = '0x5ef30b9986345249bc32d8928B7ee64DE9435E39'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ILK REGISTRY
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ilk Registry Contract Address
ILK_REGISTRY_ADDRESS = '0x5a464C28D19848f44199D003BeF5ecc87d090F87'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# VAT
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Vat Contract Address
VAT_ADDRESS = '0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# SPOT
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Spot Contract Address
SPOT_ADDRESS = '0x65C79fcB50Ca1594B025960e539eD7A9a6D434A3'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CDP Manager ABI - ilks, urns
ABI_CDP_MANAGER = '[{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"ilks","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"urns","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Ilk Registry ABI - info
ABI_ILK_REGISTRY = '[{"inputs":[{"internalType":"bytes32","name":"ilk","type":"bytes32"}],"name":"info","outputs":[{"internalType":"string","name":"name","type":"string"},{"internalType":"string","name":"symbol","type":"string"},{"internalType":"uint256","name":"class","type":"uint256"},{"internalType":"uint256","name":"dec","type":"uint256"},{"internalType":"address","name":"gem","type":"address"},{"internalType":"address","name":"pip","type":"address"},{"internalType":"address","name":"join","type":"address"},{"internalType":"address","name":"xlip","type":"address"}],"stateMutability":"view","type":"function"}]'

# Vat ABI - urns, ilks
ABI_VAT = '[{"constant":true,"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"},{"internalType":"address","name":"","type":"address"}],"name":"urns","outputs":[{"internalType":"uint256","name":"ink","type":"uint256"},{"internalType":"uint256","name":"art","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}, {"constant":true,"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"ilks","outputs":[{"internalType":"uint256","name":"Art","type":"uint256"},{"internalType":"uint256","name":"rate","type":"uint256"},{"internalType":"uint256","name":"spot","type":"uint256"},{"internalType":"uint256","name":"line","type":"uint256"},{"internalType":"uint256","name":"dust","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'

# Spot ABI - ilks
ABI_SPOT = '[{"constant":true,"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"ilks","outputs":[{"internalType":"contract PipLike","name":"pip","type":"address"},{"internalType":"uint256","name":"mat","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vault_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vault_data(vault_id, block, web3=None, execution=1, index=0):
    """

    :param vault_id:
    :param block:
    :param web3:
    :param execution:
    :param index:
    :return:
    """
    vault_data = {}

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(ETHEREUM, block=block, index=index)

        cpd_manager_contract = get_contract(CDP_MANAGER_ADDRESS, ETHEREUM, web3=web3, abi=ABI_CDP_MANAGER, block=block)
        ilk_registry_contract = get_contract(ILK_REGISTRY_ADDRESS, ETHEREUM, web3=web3, abi=ABI_ILK_REGISTRY,
                                             block=block)
        vat_contract = get_contract(VAT_ADDRESS, ETHEREUM, web3=web3, abi=ABI_VAT, block=block)
        spot_contract = get_contract(SPOT_ADDRESS, ETHEREUM, web3=web3, abi=ABI_SPOT, block=block)

        ilk = cpd_manager_contract.functions.ilks(vault_id).call(block_identifier=block)

        ilk_info = ilk_registry_contract.functions.info(ilk).call()

        urn_handler_address = cpd_manager_contract.functions.urns(vault_id).call(block_identifier=block)

        urn_data = vat_contract.functions.urns(ilk, urn_handler_address).call(block_identifier=block)

        vault_data['mat'] = spot_contract.functions.ilks(ilk).call(block_identifier=block)[1] / 10 ** 27
        vault_data['gem'] = ilk_info[4]
        vault_data['dai'] = DAI_ETH
        vault_data['ink'] = urn_data[0] / 10 ** 18
        vault_data['art'] = urn_data[1] / 10 ** 18

        ilk_data = vat_contract.functions.ilks(ilk).call(block_identifier=block)

        vault_data['Art'] = ilk_data[0] / 10 ** 18
        vault_data['rate'] = ilk_data[1] / 10 ** 27
        vault_data['spot'] = ilk_data[2] / 10 ** 27
        vault_data['line'] = ilk_data[3] / 10 ** 45
        vault_data['dust'] = ilk_data[4] / 10 ** 45

        return vault_data

    except GetNodeIndexError:
        return get_vault_data(vault_id, block, index=0, execution=execution + 1)

    except:
        return get_vault_data(vault_id, block, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# **kwargs:
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# Output:
# 1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(vault_id, block, web3=None, execution=1, index=0):
    """

    :param vault_id:
    :param block:
    :param web3:
    :param execution:
    :param index:
    :return:
    """
    result = []

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(ETHEREUM, block=block, index=index)

        vault_data = get_vault_data(vault_id, block, web3=web3)

        # Append the Collateral Address and Balance to result[]
        result.append([vault_data['gem'], vault_data['ink']])

        # Append the Debt Address (DAI Address) and Balance to result[]
        total_debt = (vault_data['art'] * vault_data['rate']) * -1
        result.append([vault_data['dai'], total_debt])

        return result

    except GetNodeIndexError:
        return underlying(vault_id, block, index=0, execution=execution + 1)

    except:
        return underlying(vault_id, block, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_delegated_MKR(wallet: str, block: Union[int, str], web3=None, decimals=True, index: int = 0,
                      execution: int = 1) -> Union[int, float]:
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(ETHEREUM, block=block, index=index)

        MKR_address = '0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2'
        IOU_token_address = '0xA618E54de493ec29432EbD2CA7f14eFbF6Ac17F7'

        return [[MKR_address, balance_of(wallet, IOU_token_address, block, ETHEREUM, web3=web3, decimals=decimals)]]

    except GetNodeIndexError:
        return get_delegated_MKR(wallet, block, index=0, execution=execution + 1)

    except:
        return get_delegated_MKR(wallet, block, index=index + 1, execution=execution)
