from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, to_token_amount

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Contracts for calling liquidity pools and underlying tokens
BANCOR_NETWORK_ADDRESS = "0xeEF417e1D5CC832e619ae18D2F140De2999dD4fB"

BANCOR_NETWORK_INFO_ADDRESS = "0x8E303D296851B320e6a697bAcB979d13c9D6E760"

BNT_TOKEN = "0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Network ABI - liquidityPools
ABI_NETWORK = '[{"inputs":[],"name":"liquidityPools","outputs":[{"internalType":"contract Token[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"}]'

# NetworkInfo ABI - poolToken, withdrawalAmounts
ABI_NETWORK_INFO = '[{"inputs":[{"internalType":"contract Token","name":"pool","type":"address"}],"name":"poolToken","outputs":[{"internalType":"contract IPoolToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract Token","name":"pool","type":"address"},{"internalType":"uint256","name":"poolTokenAmount","type":"uint256"}],"name":"withdrawalAmounts","outputs":[{"components":[{"internalType":"uint256","name":"totalAmount","type":"uint256"},{"internalType":"uint256","name":"baseTokenAmount","type":"uint256"},{"internalType":"uint256","name":"bntAmount","type":"uint256"}],"internalType":"struct WithdrawalAmounts","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]'

# ABI of the pools - balanceOf, reserveToken
ABI_POOL = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveToken","outputs":[{"internalType":"contract Token","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'


def underlying(
    token_address: str, wallet: str, block: int, blockchain: str, web3=None, decimals=True, reward=True
) -> list:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    bancor_poolcontract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL, block=block)
    balance = bancor_poolcontract.functions.balanceOf(wallet).call(block_identifier=block)

    if balance != 0:
        reserve_token = const_call(bancor_poolcontract.functions.reserveToken())
        pooltokens_contract = get_contract(
            BANCOR_NETWORK_INFO_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK_INFO, block=block
        )
        bancor_pool = pooltokens_contract.functions.withdrawalAmounts(reserve_token, balance).call(
            block_identifier=block
        )

        balances.append([reserve_token, to_token_amount(reserve_token, bancor_pool[1], blockchain, web3, decimals)])
        if reward:
            balances.append([BNT_TOKEN, to_token_amount(BNT_TOKEN, bancor_pool[2], blockchain, web3, decimals)])
    return balances


def underlying_all(wallet: str, block: int, blockchain: str, web3=None, decimals=True, reward=True) -> list:
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
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    liquiditypools_contract = get_contract(BANCOR_NETWORK_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK, block=block)
    liquidity_pools = liquiditypools_contract.functions.liquidityPools().call(block_identifier=block)
    network_info_address = get_contract(
        BANCOR_NETWORK_INFO_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK_INFO, block=block
    )

    for pool in liquidity_pools:
        bn_token = const_call(network_info_address.functions.poolToken(pool))
        balance = underlying(bn_token, wallet, block, blockchain, web3, decimals, reward)
        balances.append(balance)
    return balances
