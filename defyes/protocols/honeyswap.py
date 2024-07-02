import logging
from decimal import Decimal
from typing import List, Tuple

from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, get_decimals, get_logs_web3, to_token_amount

logger = logging.getLogger(__name__)

# LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast
ABI_LPTOKEN = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# EVENT SIGNATURES
# Swap Event Signature
SWAP_EVENT_SIGNATURE = "Swap(address,uint256,uint256,uint256,uint256,address)"


def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_data = {}

    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    lptoken_data["decimals"] = const_call(lptoken_data["contract"].functions.decimals())
    lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)
    lptoken_data["token0"] = const_call(lptoken_data["contract"].functions.token0())
    lptoken_data["token1"] = const_call(lptoken_data["contract"].functions.token1())
    lptoken_data["reserves"] = lptoken_data["contract"].functions.getReserves().call(block_identifier=block)
    lptoken_data["kLast"] = lptoken_data["contract"].functions.kLast().call(block_identifier=block)

    root_k = (Decimal(lptoken_data["reserves"][0]) * Decimal(lptoken_data["reserves"][1])).sqrt()
    root_k_last = (Decimal(lptoken_data["kLast"])).sqrt()

    if block != "latest":
        if block < 12108893:
            lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"]
        else:
            lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"] * 6 * root_k / (5 * root_k + root_k_last)
    else:
        lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"] * 6 * root_k / (5 * root_k + root_k_last)

    return lptoken_data


def underlying(wallet, lptoken_address, block, blockchain, web3=None, decimals=True) -> List[Tuple]:
    """
    Returns:
        List[Tuple]: List of (liquidity_token_address, balance)
    """
    result = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    balance = lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block)
    pool_balance_fraction = balance / lptoken_data["virtualTotalSupply"]

    for n, reserve in enumerate(lptoken_data["reserves"]):
        try:
            getattr(lptoken_data["contract"].functions, "token" + str(n))
        except AttributeError:
            continue

        token_address = lptoken_data["token" + str(n)]
        result.append(
            [
                token_address,
                to_token_amount(token_address, reserve, blockchain, web3, decimals) * Decimal(pool_balance_fraction),
            ]
        )

    return result


def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True) -> List[Tuple]:
    """
    Returns:
        List[Tuple]: List of (liquidity_token_address, balance)
    """
    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)
    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)
    reserves = lptoken_contract.functions.getReserves().call(block_identifier=block)

    for n, reserve in enumerate(reserves):
        try:
            func = getattr(lptoken_contract.functions, "token" + str(n))
        except AttributeError:
            continue

        token_address = const_call(func())
        balances.append([token_address, to_token_amount(token_address, reserve, blockchain, web3, decimals)])

    return balances


def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):
    result = {}

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    token0 = const_call(lptoken_contract.functions.token0())
    token1 = const_call(lptoken_contract.functions.token1())
    result["swaps"] = []

    decimals0 = get_decimals(token0, blockchain, web3=web3) if decimals else 0
    decimals1 = get_decimals(token1, blockchain, web3=web3) if decimals else 0

    swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()
    swap_logs = get_logs_web3(
        blockchain=blockchain,
        address=lptoken_address,
        block_start=block_start,
        block_end=block_end,
        topics=[swap_event],
    )

    for swap_log in swap_logs:
        if int(swap_log["data"].hex()[2:66], 16) == 0:
            token = token1
            amount = Decimal(0.003 * int(swap_log["data"].hex()[67:130], 16)) / Decimal(10**decimals1)
        else:
            token = token0
            amount = Decimal(0.003 * int(swap_log["data"].hex()[2:66], 16)) / Decimal(10**decimals0)

        swap_data = {"block": swap_log["blockNumber"], "token": token, "amount": amount}

        result["swaps"].append(swap_data)

    return result
