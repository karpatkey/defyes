from decimal import Decimal
from typing import Union
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, to_token_amount
from defi_protocols.constants import ETHEREUM, ZERO_ADDRESS, ETHTokenAddr

STETH_ABI = '[{"constant":true,"inputs":[{"name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
WSTETH_ABI = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stEthPerToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def underlying(wallet: str, block: Union[int, str], steth: bool = False, decimals: bool = True, web3: object = None) -> list:
    """
    Returns the balance of underlying ETH (or stETH if steth=True) corresponding to the stETH and wstETH held by a wallet.
    Parameters
    ----------
    wallet : str
        address of the wallet holding the position
    block : int or 'latest'
        block number at which the data is queried
    steth : bool
        if True the address of the underlying token returned is the Zero address, if False it is the stETH's address
    web3: obj
        optional, already instantiated web3 object
    decimals: bool
        specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True

    Returns
    ----------
    list
        a list where each element is a list with two elements, the underlying token address and its corresponding amount
    """
    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    wallet = Web3.to_checksum_address(wallet)

    steth_contract = get_contract(ETHTokenAddr.stETH, ETHEREUM, abi=STETH_ABI, block=block, web3=web3)
    steth_balance = steth_contract.functions.balanceOf(wallet).call(block_identifier=block)

    wsteth_contract = get_contract(ETHTokenAddr.wstETH, ETHEREUM, abi=WSTETH_ABI, block=block, web3=web3)
    wsteth_balance = wsteth_contract.functions.balanceOf(wallet).call(block_identifier=block)
    stEthPerToken = wsteth_contract.functions.stEthPerToken().call(block_identifier=block) / Decimal(10**18)

    steth_equivalent = steth_balance + wsteth_balance * stEthPerToken
    steth_equivalent = to_token_amount(ETHTokenAddr.stETH, steth_equivalent, ETHEREUM, web3, decimals)

    token = ETHTokenAddr.stETH if steth else ZERO_ADDRESS

    return [[token, steth_equivalent]]


def unwrap(amount: Union[int, float], block: Union[int, str], steth: bool = False, web3: object = None) -> list:
    """
    Returns the balance of the underlying ETH (or stETH if steth=True) corresponding to the inputted amount of wstETH.
    Parameters
    ----------
    amount : int or float
        amount of wstETH; should be inputted with the corresponding decimals if decimals=True or as an int if decimals=False
    block : int or 'latest'
        block number at which the data is queried
    steth : bool
        if True the address of the underlying token returned is the Zero address, if False it is the stETH's address
    web3: obj
        optional, already instantiated web3 object

    Returns
    ----------
    list
        a list where the first element is the underlying token address and the second one is the balance
    """
    if web3 is None:
        web3 = get_node(ETHEREUM, block=block)

    wsteth_contract = get_contract(ETHTokenAddr.wstETH, ETHEREUM, block=block, web3=web3)
    stEthPerToken = wsteth_contract.functions.stEthPerToken().call(block_identifier=block) / Decimal(10 ** 18)

    steth_equivalent = amount * stEthPerToken
    token = ETHTokenAddr.stETH if steth else ZERO_ADDRESS

    return [token, steth_equivalent]
