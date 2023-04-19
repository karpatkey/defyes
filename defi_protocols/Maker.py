from defi_protocols.functions import get_node, get_contract, balance_of
from defi_protocols.constants import ETHEREUM, DAI_ETH, ETHTokenAddr
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


def get_vault_data(vault_id, block, web3=None):
    vault_data = {}

    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    cpd_manager_contract = get_contract(CDP_MANAGER_ADDRESS, ETHEREUM,
                                        web3=web3, abi=ABI_CDP_MANAGER,
                                        block=block)
    ilk_registry_contract = get_contract(ILK_REGISTRY_ADDRESS, ETHEREUM,
                                         web3=web3, abi=ABI_ILK_REGISTRY,
                                         block=block)
    vat_contract = get_contract(VAT_ADDRESS, ETHEREUM,
                                web3=web3, abi=ABI_VAT, block=block)
    spot_contract = get_contract(SPOT_ADDRESS, ETHEREUM,
                                 web3=web3, abi=ABI_SPOT, block=block)

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


def underlying(vault_id, block, web3=None):
    '''
    Output:
    1 - Tuple: [[collateral_address, collateral_amount], [debt_address, -debt_amount]]
    '''
    result = []

    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    vault_data = get_vault_data(vault_id, block, web3=web3)

    # Append the Collateral Address and Balance to result[]
    result.append([vault_data['gem'], vault_data['ink']])

    # Append the Debt Address (DAI Address) and Balance to result[]
    total_debt = (vault_data['art'] * vault_data['rate']) * -1
    result.append([vault_data['dai'], total_debt])

    return result


def get_delegated_MKR(wallet: str, block: Union[int, str],
                      web3=None, decimals=True) -> Union[int, float]:
    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    IOU_token_address = '0xA618E54de493ec29432EbD2CA7f14eFbF6Ac17F7'
    balance = balance_of(wallet, IOU_token_address, block, ETHEREUM,
                         web3=web3, decimals=decimals)

    return [[ETHTokenAddr.MKR, balance]]


# This classes are just a working draft
# of a possible refactor

class Contract:
    ADDRESS = 'replace_me_or_watch_me_fail'

    def __init__(self, block):
        self.block = block
        self.web3 = get_node(ETHEREUM, block=self.block)
        self.contract = get_contract(self.ADDRESS, ETHEREUM, web3=self.web3,
                                     block=self.block)

    def __getattr__(self, a):
        fun = getattr(self.contract.functions, a)
        def aux(*args, **kwargs):
            return fun(*args, **kwargs).call(block_identifier=self.block)
        return aux


class ProxyRegistry(Contract):
    ADDRESS = '0x4678f0a6958e4D2Bc4F1BAF7Bc52E8F3564f3fE4'


class CDPManager(Contract):
    ADDRESS = CDP_MANAGER_ADDRESS

    def vaults(self, wallet_address: str):
        wallet_address = self.web3.to_checksum_address(wallet_address)
        # I'm sorry if walruses scare you := := :=
        _vs = [_next := self.first(wallet_address)]
        while (_next := self.list(_next)[1]) > 0:
            _vs.append(_next)
        return _vs
