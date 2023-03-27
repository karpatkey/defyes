from defi_protocols.functions import get_node, get_contract, get_decimals, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Contracts for calling liquidity pools and underlying tokens
BANCOR_NETWORK_ADDRESS = '0xeEF417e1D5CC832e619ae18D2F140De2999dD4fB'

BANCOR_NETWORK_INFO_ADDRESS = '0x8E303D296851B320e6a697bAcB979d13c9D6E760'

BNT_TOKEN = '0x1F573D6Fb3F13d689FF844B4cE37794d79a7FF1C'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Network ABI - liquidityPools
ABI_NETWORK = '[{"inputs":[],"name":"liquidityPools","outputs":[{"internalType":"contract Token[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"}]'

# NetworkInfo ABI - poolToken, withdrawalAmounts
ABI_NETWORK_INFO = '[{"inputs":[{"internalType":"contract Token","name":"pool","type":"address"}],"name":"poolToken","outputs":[{"internalType":"contract IPoolToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"contract Token","name":"pool","type":"address"},{"internalType":"uint256","name":"poolTokenAmount","type":"uint256"}],"name":"withdrawalAmounts","outputs":[{"components":[{"internalType":"uint256","name":"totalAmount","type":"uint256"},{"internalType":"uint256","name":"baseTokenAmount","type":"uint256"},{"internalType":"uint256","name":"bntAmount","type":"uint256"}],"internalType":"struct WithdrawalAmounts","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]'

# ABI of the pools - balanceOf, reserveToken
ABI_POOL = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"reserveToken","outputs":[{"internalType":"contract Token","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'


def underlying(token_address: str, wallet: str, block: int, blockchain: str, web3=None, execution=1, index=0,
               decimals=True, reward=False) -> list:
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        bancor_poolcontract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL, block=block)
        balance = bancor_poolcontract.functions.balanceOf(wallet).call(block_identifier=block)
        reserve_token = bancor_poolcontract.functions.reserveToken().call()
        pooltokens_contract = get_contract(BANCOR_NETWORK_INFO_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK_INFO,
                                           block=block)
        bancor_pool = pooltokens_contract.functions.withdrawalAmounts(reserve_token, balance).call()
        if balance != 0:
            if decimals is True:
                decimals0 = get_decimals(reserve_token, blockchain, web3=web3)
                decimals1 = get_decimals(BNT_TOKEN, blockchain, web3=web3)
                amount0 = bancor_pool[1] / 10 ** decimals0
                amount1 = bancor_pool[2] / 10 ** decimals1
            else:
                amount0 = bancor_pool[0]
                amount1 = bancor_pool[2]

            balances.append([reserve_token, amount0])
            balances.append([BNT_TOKEN, amount1])
        return balances

    except GetNodeIndexError:
        return underlying(token_address, wallet, block, blockchain, reward=reward, decimals=decimals, index=0,
                          execution=execution + 1)

    except:
        return underlying(token_address, wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


def underlying_all(wallet: str, block: int, blockchain: str, web3=None, execution=1, index=0, decimals=True,
                   reward=False) -> list:
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param reward:
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

        liquiditypools_contract = get_contract(BANCOR_NETWORK_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK,
                                               block=block)
        liquidity_pools = liquiditypools_contract.functions.liquidityPools().call()
        network_info_address = get_contract(BANCOR_NETWORK_INFO_ADDRESS, blockchain, web3=web3, abi=ABI_NETWORK_INFO,
                                            block=block)

        for pool in liquidity_pools:
            bn_token = network_info_address.functions.reserveToken(pool).call()
            balance = underlying(bn_token, wallet, block, blockchain, web3, execution, index, decimals, reward)
            balances.append(balance)
        return balances


    except GetNodeIndexError:
        return underlying_all(wallet, block, blockchain, reward=reward, decimals=decimals, index=0,
                              execution=execution + 1)

    except:
        return underlying_all(wallet, block, blockchain, reward=reward, decimals=decimals, index=index + 1,
                              execution=execution)

# to test
# wallet='0x849d52316331967b6ff1198e5e32a0eb168d039d'
# token_address = '0x36FAbE4cAeF8c190550b6f93c306A5644E7dCef6'
# bancor = underlying(token_address, wallet,'latest',ETHEREUM)
# print(bancor)
