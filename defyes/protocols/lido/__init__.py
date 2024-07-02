from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.constants import Address
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, to_token_amount

STETH_ABI = '[{"constant":true,"inputs":[{"name":"_account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"}]'
WSTETH_ABI = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"stEthPerToken","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'


def underlying(wallet: str, block: int | str, steth: bool = False, decimals: bool = True, web3: object = None) -> list:
    """
    Returns the balance of underlying ETH (or stETH if steth=True) corresponding to the stETH and wstETH held by a wallet.

    Args:
        wallet (str): Address of the wallet holding the position.
        block (int or 'latest'): Block number at which the data is queried.
        steth (bool, optional): If True, the address of the underlying token returned is the Zero address. If False, it is the stETH's address. Defaults to False.
        web3 (obj, optional): Optional, already instantiated web3 object.
        decimals (bool, optional): Specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True. Defaults to True.

    Returns:
        list: A list where each element is a list with two elements, the underlying token address and its corresponding amount.
    """
    if web3 is None:
        web3 = get_node(Chain.ETHEREUM)

    wallet = Web3.to_checksum_address(wallet)

    steth_contract = get_contract(EthereumTokenAddr.stETH, Chain.ETHEREUM, abi=STETH_ABI)
    steth_balance = steth_contract.functions.balanceOf(wallet).call(block_identifier=block)

    wsteth_contract = get_contract(EthereumTokenAddr.wstETH, Chain.ETHEREUM, abi=WSTETH_ABI)
    wsteth_balance = wsteth_contract.functions.balanceOf(wallet).call(block_identifier=block)
    stEthPerToken = wsteth_contract.functions.stEthPerToken().call(block_identifier=block) / Decimal(10**18)

    steth_equivalent = steth_balance + wsteth_balance * stEthPerToken
    steth_equivalent = to_token_amount(EthereumTokenAddr.stETH, steth_equivalent, Chain.ETHEREUM, web3, decimals)

    token = EthereumTokenAddr.stETH if steth else Address.ZERO

    return [[token, steth_equivalent]]


def unwrap(amount: int | float, block: int | str, steth: bool = False, web3: object = None) -> list:
    """
    Returns the balance of the underlying ETH (or stETH if steth=True) corresponding to the inputted amount of wstETH.

    Args:
        amount (int or float): Amount of wstETH; should be inputted with the corresponding decimals if decimals=True or as an int if decimals=False.
        block (int or 'latest'): Block number at which the data is queried.
        steth (bool): If True, the address of the underlying token returned is the Zero address. If False, it is the stETH's address.
        web3 (obj): Optional, already instantiated web3 object.

    Returns:
        list: A list where the first element is the underlying token address and the second one is the balance.
    """
    if web3 is None:
        web3 = get_node(Chain.ETHEREUM)

    wsteth_contract = get_contract(EthereumTokenAddr.wstETH, Chain.ETHEREUM)
    stEthPerToken = wsteth_contract.functions.stEthPerToken().call(block_identifier=block) / Decimal(10**18)

    steth_equivalent = amount * stEthPerToken
    token = EthereumTokenAddr.stETH if steth else Address.ZERO

    return [token, steth_equivalent]
