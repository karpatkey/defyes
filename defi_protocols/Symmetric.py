import logging
import json
from decimal import Decimal
from pathlib import Path
from web3 import Web3
from web3.exceptions import ContractLogicError

from defi_protocols.functions import get_node, get_contract, get_decimals, get_logs, BlockchainError, to_token_amount
from defi_protocols.constants import XDAI, ZERO_ADDRESS


logger = logging.getLogger(__name__)

# xDAI - Symmetric Vault Contract Address
VAULT_XDAI = '0x24F87b37F4F249Da61D89c3FF776a55c321B2773'

# xDAI - SymmChef Contract Address
SYMMCHEF_XDAI = '0xdf667DeA9F6857634AaAf549cA40E06f04845C03'

# xDAI - SymmChef Contract Address
SYMFACTORY_XDAI = '0x9B4214FD41cD24347A25122AC7bb6B479BED72Ac'

# Symmetric Vault ABI - getPoolTokens
ABI_VAULT = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address[]","name":"tokens","internalType":"contract IERC20[]"},{"type":"uint256[]","name":"balances","internalType":"uint256[]"},{"type":"uint256","name":"lastChangeBlock","internalType":"uint256"}],"name":"getPoolTokens","inputs":[{"type":"bytes32","name":"poolId","internalType":"bytes32"}]}]'

# Chefs V2 ABI - SYMM, rewarder, pendingSymm, lpToken, userInfo, poolLength, poolInfo, symmPerSecond, totalAllocPoint
ABI_CHEF_V2 = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"SYMM","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IRewarder"}],"name":"rewarder","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"pending","internalType":"uint256"}],"name":"pendingSymm","inputs":[{"type":"uint256","name":"_pid","internalType":"uint256"},{"type":"address","name":"_user","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"lpToken","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"amount","internalType":"uint256"},{"type":"int256","name":"rewardDebt","internalType":"int256"}],"name":"userInfo","inputs":[{"type":"uint256","name":"","internalType":"uint256"},{"type":"address","name":"","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"pools","internalType":"uint256"}],"name":"poolLength","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint128","name":"accSymmPerShare","internalType":"uint128"},{"type":"uint64","name":"lastRewardTime","internalType":"uint64"},{"type":"uint64","name":"allocPoint","internalType":"uint64"}],"name":"poolInfo","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"symmPerSecond","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalAllocPoint","inputs":[]}]'

# Rewarder ABI - rewardToken, pendingTokens, rewardPerSecond, poolInfo
ABI_REWARDER = '[{"inputs":[{"internalType":"uint256","name":"pid","type":"uint256"},{"internalType":"address","name":"user","type":"address"},{"internalType":"uint256","name":"","type":"uint256"}],"name":"pendingTokens","outputs":[{"internalType":"contract IERC20[]","name":"rewardTokens","type":"address[]"},{"internalType":"uint256[]","name":"rewardAmounts","type":"uint256[]"}],"stateMutability":"view","type":"function"}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"rewardPerSecond","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint128","name":"accSymmPerShare","internalType":"uint128"},{"type":"uint64","name":"lastRewardTime","internalType":"uint64"},{"type":"uint64","name":"allocPoint","internalType":"uint64"}],"name":"poolInfo","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]}]'

# LP Token ABI - getPoolId, decimals, totalSupply, getReserves, balanceOf
ABI_LPTOKEN = '[{"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# LP Token ABI V1 - getCurrentTokens, totalSupply, balanceOf, getBalance
ABI_LPTOKENV1 = '[{"constant": true,"inputs": [],"name": "getCurrentTokens","outputs": [{"internalType": "address[]","name": "tokens","type": "address[]"}],"payable": false,"stateMutability": "view","type": "function"},\
            {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getReserves","outputs":[{"internalType":"uint112","name":"_reserve0","type":"uint112"},{"internalType":"uint112","name":"_reserve1","type":"uint112"},{"internalType":"uint32","name":"_blockTimestampLast","type":"uint32"}],"stateMutability":"view","type":"function"}, \
            {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"constant": true,"inputs": [{"internalType": "address","name": "token","type": "address"}],"name": "getBalance","outputs": [{"internalType": "uint256","name": "","type": "uint256"}],"payable": false,"stateMutability": "view","type": "function"}]'

# Is BPool?
ABI_BPOOL = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"isBPool","inputs":[{"type":"address","name":"b","internalType":"address"}],"constant":true}]'

SWAP_EVENT_SIGNATURE = 'LOG_SWAP(address,address,address,uint256,uint256)'


DB_FILE = Path(__file__).parent / "db" / "Symmetric_db.json"


def get_vault_contract(web3, block, blockchain):
    """
    :param web3:
    :param block:
    :param blockchain:
    :return:
    """
    if blockchain != XDAI:
        raise BlockchainError(f"{blockchain} not {XDAI}")
    vault_contract = get_contract(VAULT_XDAI, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    return vault_contract


def get_chef_contract(web3, block, blockchain):
    """
    :param web3:
    :param block:
    :param blockchain:
    :return:
    """
    if blockchain != XDAI:
        raise BlockchainError(f"{blockchain} not {XDAI}")
    chef_contract = get_contract(SYMMCHEF_XDAI, blockchain, web3=web3, abi=ABI_CHEF_V2, block=block)

    return chef_contract


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_info
# Output:
# 1 - Dictionary: result['chef_contract'] = chef_contract
#                 result['pool_info'] = {
#                     'poolId': poolID
#                     'allocPoint': allocPoint
#                 }
#                 result['totalAllocPoint']: totalAllocPoint
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_info(web3, lptoken_address, block, blockchain):
    """
    :param web3:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :return:
    """
    result = {}
    with open(DB_FILE, 'r') as db_file:
        db_data = json.load(db_file)

    result['chef_contract'] = get_chef_contract(web3, block, blockchain)

    try:
        result['pool_info'] = {
            'poolId': db_data[blockchain]['pools'][lptoken_address],
            'allocPoint':
                result['chef_contract'].functions.poolInfo(db_data[blockchain]['pools'][lptoken_address]).call(
                    block_identifier=block)[2]
        }
        result['totalAllocPoint'] = result['chef_contract'].functions.totalAllocPoint().call(block_identifier=block)
    except ContractLogicError:
        pass

    return result


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    """
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :return:
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_data = {}

    lptoken_data['contract'] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)
    lptoken_data['poolId'] = lptoken_data['contract'].functions.getPoolId().call()
    lptoken_data['decimals'] = lptoken_data['contract'].functions.decimals().call()
    lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(block_identifier=block)

    return lptoken_data


def get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id):
    """
    :param web3:
    :param block:
    :param blockchain:
    :param chef_contract:
    :param pool_id:
    :return:
    """
    rewarder_contract_address = chef_contract.functions.rewarder(pool_id).call()
    rewarder_contract = get_contract(rewarder_contract_address, blockchain, web3=web3, abi=ABI_REWARDER, block=block)

    return rewarder_contract


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_symm_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - Tuple: [symm_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_symm_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True):
    """
    :param web3:
    :param wallet:
    :param chef_contract:
    :param pool_id:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    symm_address = chef_contract.functions.SYMM().call()
    symm_rewards = chef_contract.functions.pendingSymm(pool_id, wallet).call(block_identifier=block)

    return [symm_address, to_token_amount(symm_address, symm_rewards, blockchain, web3, decimals)]


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=True):
    """
    :param web3:
    :param wallet:
    :param chef_contract:
    :param pool_id:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    rewards = []

    rewarder_contract = get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)

    if rewarder_contract.address != ZERO_ADDRESS:

        pending_tokens_info = rewarder_contract.functions.pendingTokens(pool_id, wallet, 1).call(block_identifier=block)
        pending_tokens_addresses = pending_tokens_info[0]
        pending_token_amounts = pending_tokens_info[1]

        for i in range(len(pending_tokens_addresses)):
            rewards.append([pending_tokens_addresses[i], to_token_amount(pending_tokens_addresses[i],
                                                                         pending_token_amounts[i],
                                                                         blockchain,
                                                                         web3,
                                                                         decimals)])

    return rewards


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'pool_info' = Dictionary -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, pool_info=None):
    """
    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param pool_info:
    :return:
    """
    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if pool_info is None:
        pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

    if pool_info is None:
        logger.error('Incorrect Symmetric LPToken Address: ', lptoken_address)
        # FIXME: Function returns different type values
        return None

    pool_id = pool_info['pool_info']['poolId']
    chef_contract = pool_info['chef_contract']

    symm_rewards = get_symm_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=decimals)
    all_rewards.append(symm_rewards)

    rewards = get_rewards(web3, wallet, chef_contract, pool_id, block, blockchain, decimals=decimals)

    if len(rewards) > 0:
        for reward in rewards:
            all_rewards.append(reward)

    return all_rewards


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, reward=False):
    """
    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :param reward:
    :return:
    """
    result = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    pool_info = get_pool_info(web3, lptoken_address, block, blockchain)
    factory_contract = get_contract(SYMFACTORY_XDAI, blockchain, block=block, web3=web3, abi=ABI_BPOOL)

    if pool_info is None:
        if factory_contract.functions.isBPool(lptoken_address).call():
            lp_token_contract = get_contract(lptoken_address, blockchain, block=block, web3=web3, abi=ABI_LPTOKENV1)
            balance = lp_token_contract.functions.balanceOf(wallet).call()
            totalsupply = lp_token_contract.functions.totalSupply().call()
            current_tokens = lp_token_contract.functions.getCurrentTokens().call()
            for token in current_tokens:
                balance_token = lp_token_contract.functions.getBalance(token).call()
                amount = balance / Decimal(totalsupply) * to_token_amount(token, balance_token, blockchain, web3, decimals)
                result.append([token, amount])
        else:
            logger.error('Incorrect Symmetric LPToken Address: ', lptoken_address)
            result = []
    else:
        pool_id = pool_info['pool_info']['poolId']
        chef_contract = pool_info['chef_contract']

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

        vault_contract = get_vault_contract(web3, block, blockchain)
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = pool_tokens_data[1]

        pool_balance_fraction = Decimal(lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block))
        pool_balance_fraction /= Decimal(lptoken_data['totalSupply'])
        pool_staked_fraction = Decimal(chef_contract.functions.userInfo(pool_id, wallet).call(block_identifier=block)[0])
        pool_staked_fraction /= Decimal(lptoken_data['totalSupply'])

        for token_address, pool_balance in zip(pool_tokens, pool_balances):
            token_balance = to_token_amount(token_address, pool_balance, blockchain, web3, decimals)
            result.append([token_address, token_balance * pool_balance_fraction, token_balance * pool_staked_fraction])

    if reward is True:
        all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                      pool_info=pool_info)

        result = [result]  # FIXME remove this
        result.append(all_rewards)

    return result


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 element:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):
    """
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)
    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)
    pool_id = lptoken_contract.functions.getPoolId().call()

    vault_contract = get_vault_contract(web3, block, blockchain)
    pool_tokens_data = vault_contract.functions.getPoolTokens(pool_id).call(block_identifier=block)
    pool_tokens = pool_tokens_data[0]
    pool_balances = pool_tokens_data[1]

    for token_address, pool_balance in zip(pool_tokens, pool_balances):
        balances.append([token_address, to_token_amount(token_address, pool_balance, blockchain, web3, decimals)])

    return balances

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards_per_unit
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards_per_unit(lptoken_address, blockchain, web3=None, block='latest'):
    """
    :param lptoken_address:
    :param blockchain:
    :param web3:
    :param block:
    :return:
    """
    result = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)
    pool_info = get_pool_info(web3, lptoken_address, block, blockchain)

    if pool_info is None:
        logger.error('Incorrect Symmetric LPToken Address: ', lptoken_address)
        # FIXME: Function returns different type values
        return None

    chef_contract = pool_info['chef_contract']
    pool_id = pool_info['pool_info']['poolId']

    symm_reward_data = {
        'symm_address': chef_contract.functions.SYMM().call(),
        'symmPerSecond': Decimal(chef_contract.functions.symmPerSecond().call(block_identifier=block)) * pool_info['pool_info']['allocPoint'] / pool_info['totalAllocPoint']
    }
    result.append(symm_reward_data)

    try:
        reward_data = {}

        rewarder_contract = get_rewarder_contract(web3, block, blockchain, chef_contract, pool_id)
        rewarder_pool_info = rewarder_contract.functions.poolInfo(pool_id).call(block_identifier=block)
        rewarder_alloc_point = rewarder_pool_info[2]

        # Rewarder Total Allocation Point Calculation
        rewarder_total_alloc_point = 0
        for i in range(chef_contract.functions.poolLength().call()):
            rewarder_total_alloc_point += rewarder_contract.functions.poolInfo(i).call(block_identifier=block)[2]

        reward_data['reward_address'] = rewarder_contract.functions.pendingTokens(pool_id, ZERO_ADDRESS, 1).call(block_identifier=block)[0][0]

        try:
            reward_data['rewardPerSecond'] = Decimal(rewarder_contract.functions.rewardPerSecond().call(block_identifier=block))
            reward_data['rewardPerSecond'] *= Decimal(rewarder_alloc_point) / Decimal(rewarder_total_alloc_point)
        except ContractLogicError:
            reward_data['rewardPerSecond'] = Decimal(0)

        result.append(reward_data)

    except ContractLogicError:
        pass

    return result


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # get_apr
# # 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# # 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# # 'web3' = web3 (Node) -> Improves performance
# # 'block' = block identifier
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# def get_apr(lptoken_address, blockchain, web3=None, execution=1, index=0, block='latest'):

#     # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
#     if execution > MAX_EXECUTIONS:
#         return None

#     try:
#         if web3 == None:
#             web3 = get_node(blockchain, block=block, index=index)

#         data = get_rewards_per_unit(lptoken_address, blockchain, block=block, web3=web3)

#         symm_price = Prices.get_price(data[0]['symm_address'], block, blockchain, web3=web3)
#         symm_decimals = get_decimals(data[0]['symm_address'], blockchain, web3=web3)

#         symm_per_second = data[0]['symmPerSecond']
#         symm_per_year = symm_per_second * (3600 * 24 * 365) / (10**symm_decimals)

#         try:
#             reward_price = Prices.get_price(data[1]['reward_address'], block, blockchain, web3=web3)
#             reward_decimals = get_decimals(data[1]['reward_address'], blockchain, web3=web3)

#             reward_per_year = data[1]['rewardPerSecond'] * (3600 * 24 * 365) / (10**reward_decimals)
#         except:
#             reward_price = 0
#             reward_per_year = 0

#         balances = pool_balances(lptoken_address, block, blockchain)
#         token_addresses = [balances[i][0] for i in range(len(balances))]
#         token_prices = [Prices.get_price(token_addresses[i], block, blockchain) for i in range(len(token_addresses))]
#         tvl = sum([balances[i][1] * token_prices[i] for i in range(len(token_addresses))])

#         apr = ((symm_per_year * symm_price + reward_per_year * reward_price) / tvl) * 100

#         return apr

#     except GetNodeIndexError:
#         index = 0

#         return get_apr(lptoken_address, blockchain, block=block, index=index, execution=execution + 1)

#     except GetNodeIndexError:
#         index = 0

#         return get_apr(lptoken_address, blockchain, block=block, index=index, execution=execution + 1)

#     except Exception as Ex:
#         traceback.print_exc()
#         return get_apr(lptoken_address, blockchain, block=block, index=index + 1, execution=execution)


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# # update_db
# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db(output_file=DB_FILE):
    try:
        with open(DB_FILE, 'r') as db_file:
            db_data = json.load(db_file)
    except:
        db_data = {XDAI: {
            'pools': {}
        }}

    web3 = get_node(XDAI)

    symm_chef = get_chef_contract(web3, 'latest', XDAI)
    db_pool_length = len(db_data[XDAI]['pools'])
    pools_delta = symm_chef.functions.poolLength().call() - db_pool_length

    updated = False
    if pools_delta > 0:
        updated = True
        for i in range(pools_delta):
            lptoken_address = symm_chef.functions.lpToken(db_pool_length + i).call()
            db_data[XDAI]['pools'][lptoken_address] = db_pool_length + i

        with open(output_file, 'w') as db_file:
            json.dump(db_data, db_file)

    return updated


def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):
    """
    :param lptoken_address:
    :param block_start:
    :param block_end:
    :param blockchain:
    :param web3:
    :param decimals:
    :return:
    """
    result = {}
    hash_overlap = []

    if web3 is None:
        web3 = get_node(blockchain, block=block_start)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKENV1, block=block_start)
    from IPython import embed; embed()
    token0 = lptoken_contract.functions.getCurrentTokens().call()[0]
    token1 = lptoken_contract.functions.getCurrentTokens().call()[1]
    result['swaps'] = []

    decimals0 = get_decimals(token0, blockchain, web3=web3) if decimals else 0
    decimals1 = get_decimals(token1, blockchain, web3=web3) if decimals else 0

    get_logs_bool = True
    block_from = block_start
    block_to = block_end

    swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()

    while get_logs_bool:
        swap_logs = get_logs(block_from, block_to, lptoken_address, swap_event, blockchain)

        log_count = len(swap_logs)

        if log_count != 0:
            last_block = int(
                swap_logs[log_count - 1]['blockNumber'][2:len(swap_logs[log_count - 1]['blockNumber'])], 16)

            for swap_log in swap_logs:
                block_number = int(swap_log['blockNumber'][2:len(swap_log['blockNumber'])], 16)

                if swap_log['transactionHash'] in swap_log:
                    continue

                if block_number == last_block:
                    hash_overlap.append(swap_log['transactionHash'])

                if int(swap_log['data'][2:66], 16) == 0:
                    swap_data = {
                        'block': block_number,
                        'token': token1,
                        'amount': Decimal(int(swap_log['data'][67:130], 16)) / Decimal(10 ** decimals1) * Decimal(0.003)
                    }
                else:
                    swap_data = {
                        'block': block_number,
                        'token': token0,
                        'amount': Decimal(int(swap_log['data'][2:66], 16)) / Decimal(10 ** decimals0) * Decimal(0.003)
                    }

                result['swaps'].append(swap_data)

        if log_count < 1000:
            get_logs_bool = False

        else:
            block_from = block_number

    return result
