import logging
from decimal import Decimal

from defabipedia import Chain
from karpatkit.cache import const_call
from karpatkit.constants import Address
from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import ContractLogicError

from defyes.functions import BlockchainError, get_contract, last_block, to_token_amount

logger = logging.getLogger(__name__)

# xDAI - Symmetric Vault Contract Address
VAULT_GNOSIS = "0x24F87b37F4F249Da61D89c3FF776a55c321B2773"
VAULT_OLD_GNOSIS = "0x901E0dC02f64C42F73F0Bdbf3ef21aFc96CF50be"
# xDAI - SymmChef Contract Address
SYMMCHEF_GNOSIS = "0xdf667DeA9F6857634AaAf549cA40E06f04845C03"

# xDAI - SymmChef Contract Address
SYMFACTORY_GNOSIS = "0x9B4214FD41cD24347A25122AC7bb6B479BED72Ac"

SYMM = "0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84"

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

SWAP_EVENT_SIGNATURE = "LOG_SWAP(address,address,address,uint256,uint256)"


pool_ids_farming = {
    Chain.GNOSIS: {
        "0x8B78873717981F18C9B8EE67162028BD7479142b": 0,
        "0x650f5d96E83d3437bf5382558cB31F0ac5536684": 1,
        "0x08f605D222Ca0FB58a102796Ff539d710cDF4B27": 2,
        "0x71EE8c46d222Dd0f1F50B76f5fbf809bb944105F": 3,
        "0x313FB6426D4b24E1e4Fc2C3521efbEde581d16A3": 4,
        "0x3F6F3eda8aE4F81ebcE3d58E09BBA0a6F9E25bd9": 5,
        "0x3B62617AcC31Ad559dF9f7954679DC19FfF2C353": 6,
        "0xa2F08DfF399ed1eF1cb5228C998e256CBC9515C6": 7,
        "0xa4c8c4485eC50748c4B470d26B5C7BC112cA7C30": 8,
        "0xdF82E3bD7B5B30b6084b5e945924358D7D5f31D1": 9,
        "0xd3078c1568Ece597f2dF457A4Bbf670FB8076e71": 10,
        "0xA13d7B2Ff0300Fc32Aa3d1A596221Bc6724Ac9DD": 11,
        "0xa4458034865bA70E4D0fB6f3353D9fa57Df2eAB5": 12,
    }
}


def get_pool_ids_farming():
    web3 = get_node(Chain.GNOSIS)

    chef_contract = web3.eth.contract(address=SYMMCHEF_GNOSIS, abi=ABI_CHEF_V2)
    poolLength = chef_contract.functions.poolLength().call(block_identifier="latest")

    for i in range(poolLength):
        lptoken_address = const_call(chef_contract.functions.lpToken(i))
        pool_ids_farming[Chain.GNOSIS][lptoken_address] = i

    return pool_ids_farming


def get_all_rewards(
    wallet: str, lptoken_address: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True
) -> dict:
    """
    Returns the unclaimed rewards accrued by the wallet holding funds in the pool with the LP token address.

    Args:
        wallet (str): The address of the wallet holding the position.
        lptoken_address (str): The LP token address of the pool.
        block (int or str): The block number at which the data is queried.
        blockchain (str): The blockchain name.
        web3 (Web3, optional): An already instantiated web3 object.
        decimals (bool, optional): Specifies whether balances are returned as int if set to False, or Decimal type with the appropriate decimals if set to True.

    Returns:
        dict: A dictionary containing the following information:
            - 'protocol' (str): The protocol name.
            - 'blockchain' (str): The blockchain name.
            - 'lptoken_address' (str): The LP token address.
            - 'block' (int or str): The block number.
            - 'rewards' (list): A list of dictionaries representing the rewards. Each dictionary contains:
                - 'token' (str): The token address.
                - 'balance' (Decimal): The reward balance.

    Example:
        {
            'protocol': 'Symmetric',
            'blockchain': Chain.GNOSIS,
            'lptoken_address': '0x650f5d96E83d3437bf5382558cB31F0ac5536684',
            'block': 26502427,
            'rewards': [
                {
                    'token': '0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84',
                    'balance': Decimal('97.408879919684859779')
                },
                {
                    'token': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                    'balance': Decimal('0')
                }
            ]
        }
    """
    if blockchain != Chain.GNOSIS:
        raise BlockchainError(f"{blockchain} not {Chain.GNOSIS}")

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    result = {
        "protocol": "Symmetric",
        "blockchain": blockchain,
        "lptoken_address": lptoken_address,
        "block": block if block != "latest" else last_block(Chain.GNOSIS),
        "rewards": [],
    }

    if lptoken_address not in pool_ids_farming[Chain.GNOSIS]:
        return result

    pool_id_farming = pool_ids_farming[Chain.GNOSIS][lptoken_address]
    chef_contract = web3.eth.contract(address=SYMMCHEF_GNOSIS, abi=ABI_CHEF_V2)
    symm_rewards = chef_contract.functions.pendingSymm(pool_id_farming, wallet).call(block_identifier=block)
    result["rewards"].append(
        {"token": SYMM, "balance": to_token_amount(SYMM, symm_rewards, Chain.GNOSIS, web3=web3, decimals=decimals)}
    )

    rewarder_contract_address = const_call(chef_contract.functions.rewarder(pool_id_farming))
    if rewarder_contract_address != Address.ZERO:
        rewarder_contract = get_contract(rewarder_contract_address, blockchain, web3=web3, abi=ABI_REWARDER)

        pending_tokens_info = rewarder_contract.functions.pendingTokens(pool_id_farming, wallet, 1).call(
            block_identifier=block
        )
        pending_tokens_addresses = pending_tokens_info[0]
        pending_token_amounts = pending_tokens_info[1]

        for token_address, token_amount in zip(pending_tokens_addresses, pending_token_amounts):
            result["rewards"].append(
                {
                    "token": token_address,
                    "balance": to_token_amount(token_address, token_amount, blockchain, web3=web3, decimals=decimals),
                }
            )

    return result


def underlying(
    wallet: str,
    lptoken_address: str,
    block: int | str,
    blockchain: str,
    web3: Web3 = None,
    decimals: bool = True,
    reward: bool = False,
) -> dict:
    """
    Returns the balances of the underlying tokens held by the wallet in the pool with LP token address lptoken_address.

    Parameters:
        wallet (str): Address of the wallet holding the position.
        lptoken_address (str): LP token address of the pool.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (str): Blockchain identifier.
        web3 (Web3, optional): Already instantiated web3 object.
        decimals (bool): Specifies whether balances are returned as int if set to False, or Decimal type with the appropriate decimals if set to True.
        reward (bool): If True, it also includes in the dictionary the balances of unclaimed rewards.

    Returns:
        dict: A dictionary containing the following keys:
            - 'protocol': 'Symmetric'
            - 'blockchain': The blockchain identifier.
            - 'lptoken_address': The LP token address.
            - 'block': The block number.
            - 'unstaked': A list of dictionaries representing the balances of unstaked tokens, each containing the 'token' and 'balance' keys.
            - 'staked': A list of dictionaries representing the balances of staked tokens, each containing the 'token' and 'balance' keys.

    Example:
        {
            'protocol': 'Symmetric',
            'blockchain': Chain.GNOSIS,
            'lptoken_address': '0x650f5d96E83d3437bf5382558cB31F0ac5536684',
            'block': 28440966,
            'unstaked': [
                {
                    'token': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                    'balance': Decimal('0.5151561795132954373125167419')
                },
                {
                    'token': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d',
                    'balance': Decimal('14.04470517028213093498360963')
                }
            ],
            'staked': [
                {
                    'token': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                    'balance': Decimal('0E-18')
                },
                {
                    'token': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d',
                    'balance': Decimal('0E-18')
                }
            ]
        }
    """

    if blockchain != Chain.GNOSIS:
        raise BlockchainError(f"{blockchain} not {Chain.GNOSIS}")

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    factory_contract = get_contract(SYMFACTORY_GNOSIS, blockchain, web3=web3, abi=ABI_BPOOL)

    result = {
        "protocol": "Symmetric",
        "blockchain": blockchain,
        "lptoken_address": lptoken_address,
        "block": block if block != "latest" else last_block(Chain.GNOSIS),
        "unstaked": [],
    }

    if factory_contract.functions.isBPool(lptoken_address).call(block_identifier=block):
        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKENV1)
        balance = lptoken_contract.functions.balanceOf(wallet).call(block_identifier=block)
        totalsupply = lptoken_contract.functions.totalSupply().call(block_identifier=block)
        current_tokens = const_call(lptoken_contract.functions.getCurrentTokens())
        for token in current_tokens:
            balance_token = lptoken_contract.functions.getBalance(token).call(block_identifier=block)
            amount = balance / Decimal(totalsupply) * to_token_amount(token, balance_token, blockchain, web3, decimals)
            result["unstaked"].append({"token": token, "balance": amount})
        return result
    else:
        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)
        pool_id = const_call(lptoken_contract.functions.getPoolId())
        pool_id = "0x" + pool_id.hex()
        try:
            # Checking if it's a pool from the old vault
            vault_contract = web3.eth.contract(address=VAULT_OLD_GNOSIS, abi=ABI_VAULT)
            pool_tokens_data = vault_contract.functions.getPoolTokens(pool_id).call(block_identifier=block)
        except ContractLogicError:
            vault_contract = web3.eth.contract(address=VAULT_GNOSIS, abi=ABI_VAULT)
            pool_tokens_data = vault_contract.functions.getPoolTokens(pool_id).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = pool_tokens_data[1]
        total_supply = lptoken_contract.functions.totalSupply().call(block_identifier=block)
        pool_balance_fraction = Decimal(
            lptoken_contract.functions.balanceOf(wallet).call(block_identifier=block)
        ) / Decimal(total_supply)

        for token_address, pool_balance in zip(pool_tokens, pool_balances):
            amount = to_token_amount(token_address, pool_balance, blockchain, web3, decimals)
            result["unstaked"].append({"token": token_address, "balance": amount * pool_balance_fraction})
        if lptoken_address in pool_ids_farming[Chain.GNOSIS]:
            pool_id_farming = pool_ids_farming[Chain.GNOSIS][lptoken_address]
            chef_contract = web3.eth.contract(address=SYMMCHEF_GNOSIS, abi=ABI_CHEF_V2)
            pool_staked_fraction = Decimal(
                chef_contract.functions.userInfo(pool_id_farming, wallet).call(block_identifier=block)[0]
            ) / Decimal(total_supply)
            result["staked"] = []
            for token_address, pool_balance in zip(pool_tokens, pool_balances):
                amount = to_token_amount(token_address, pool_balance, blockchain, web3, decimals)
                result["staked"].append({"token": token_address, "balance": amount * pool_staked_fraction})

            if reward:
                result["rewards"] = get_all_rewards(
                    wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals
                )["rewards"]
            return result


def pool_balances(
    lptoken_address: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True
) -> dict:
    """
    Returns the balances of the tokens in the pool with LP token address lptoken_address.

    Args:
        wallet (str): Address of the wallet holding the position.
        lptoken_address (str): LP token address of the pool.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (bool): If True, the address of the underlying token returned is the Zero address. If False, it is the stETH's address.
        web3 (obj, optional): Already instantiated web3 object.
        decimals (bool): Specifies whether balances are returned as int if set to False, or Decimal type with the appropriate decimals if set to True.

    Returns:
        dict: A dictionary containing the following keys:
            - 'protocol' (str): Name of the protocol ('Symmetric').
            - 'blockchain' (str): Name of the blockchain (Chain.GNOSIS).
            - 'lptoken_address' (str): LP token address.
            - 'block' (int): Block number.
            - 'unstaked' (list): List of dictionaries containing the token address and balance of unstaked tokens.
            - 'staked' (list): List of dictionaries containing the token address and balance of staked tokens.

    Example:
        {
            'protocol': 'Symmetric',
            'blockchain': Chain.GNOSIS,
            'lptoken_address': '0x650f5d96E83d3437bf5382558cB31F0ac5536684',
            'block': 28440966,
            'unstaked': [
                {
                    'token': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                    'balance': Decimal('0.5151561795132954373125167419')
                },
                {
                    'token': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d',
                    'balance': Decimal('14.04470517028213093498360963')
                }
            ],
            'staked': [
                {
                    'token': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                    'balance': Decimal('0E-18')
                },
                {
                    'token': '0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d',
                    'balance': Decimal('0E-18')
                }
            ]
        }
    """

    if blockchain != Chain.GNOSIS:
        raise BlockchainError(f"{blockchain} not {Chain.GNOSIS}")

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    factory_contract = get_contract(SYMFACTORY_GNOSIS, blockchain, web3=web3, abi=ABI_BPOOL)

    result = {
        "protocol": "Symmetric",
        "blockchain": blockchain,
        "lptoken_address": lptoken_address,
        "block": block if block != "latest" else last_block(Chain.GNOSIS),
        "pool_balances": [],
    }

    # Checking if it's a V1 pool
    if factory_contract.functions.isBPool(lptoken_address).call(block_identifier=block):
        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKENV1)
        current_tokens = const_call(lptoken_contract.functions.getCurrentTokens())
        for token in current_tokens:
            balance_token = lptoken_contract.functions.getBalance(token).call(block_identifier=block)
            result["pool_balances"].append(
                {
                    "token": token,
                    "balance": to_token_amount(token, balance_token, blockchain, web3=web3, decimals=decimals),
                }
            )
        return result
    else:
        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)
    pool_id = const_call(lptoken_contract.functions.getPoolId())
    pool_id = "0x" + pool_id.hex()
    try:
        # Checking if it's a pool from the old vault
        vault_contract = web3.eth.contract(address=VAULT_OLD_GNOSIS, abi=ABI_VAULT)
        pool_tokens_data = vault_contract.functions.getPoolTokens(pool_id).call(block_identifier=block)
    except ContractLogicError:
        vault_contract = web3.eth.contract(address=VAULT_GNOSIS, abi=ABI_VAULT)
        pool_tokens_data = vault_contract.functions.getPoolTokens(pool_id).call(block_identifier=block)

    pool_tokens = pool_tokens_data[0]
    pool_balances = pool_tokens_data[1]

    for token_address, pool_balance in zip(pool_tokens, pool_balances):
        result["pool_balances"].append(
            {
                "token": token_address,
                "balance": to_token_amount(token_address, pool_balance, blockchain, web3=web3, decimals=decimals),
            }
        )
    return result


def get_rewards_per_second(
    lptoken_address: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True
) -> dict:
    """
    Returns the rewards per second accrued by staking the LP token with address lptoken_address.

    Args:
        lptoken_address (str): LP token address of the pool.
        block (int or str): Block number at which the data is queried.
        blockchain (str): Blockchain name.
        web3 (Web3, optional): Already instantiated web3 object.
        decimals (bool): Specifies whether balances are returned as int if set to False, or Decimal type with the appropriate decimals if set to True.

    Returns:
        dict: A dictionary containing the following keys:
            - 'protocol' (str): Protocol name.
            - 'blockchain' (str): Blockchain name.
            - 'lptoken_address' (str): LP token address.
            - 'block' (int or str): Block number.
            - 'reward_rates' (list): A list of dictionaries containing the following keys:
                - 'token' (str): Token address.
                - 'rewards_per_second' (Decimal): Rewards per second.

    Example:
        {
            'protocol': 'Symmetric',
            'blockchain': Chain.GNOSIS,
            'lptoken_address': '0x650f5d96E83d3437bf5382558cB31F0ac5536684',
            'block': 25502427,
            'reward_rates': [
                {
                    'token': '0xC45b3C1c24d5F54E7a2cF288ac668c74Dd507a84',
                    'rewards_per_second': Decimal('0.00006326935536119204081632653061')
                },
                {
                    'token': '0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb',
                    'rewards_per_second': Decimal('0')
                }
            ]
        }
    """

    if blockchain != Chain.GNOSIS:
        raise BlockchainError(f"{blockchain} not {Chain.GNOSIS}")

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    result = {
        "protocol": "Symmetric",
        "blockchain": blockchain,
        "lptoken_address": lptoken_address,
        "block": block if block != "latest" else last_block(Chain.GNOSIS),
        "reward_rates": [],
    }

    if lptoken_address not in pool_ids_farming[Chain.GNOSIS]:
        return result

    pool_id_farming = pool_ids_farming[Chain.GNOSIS][lptoken_address]
    chef_contract = web3.eth.contract(address=SYMMCHEF_GNOSIS, abi=ABI_CHEF_V2)
    alloc_point = chef_contract.functions.poolInfo(pool_id_farming).call(block_identifier=block)[2]
    total_alloc_point = chef_contract.functions.totalAllocPoint().call(block_identifier=block)
    symm_per_second = (
        Decimal(chef_contract.functions.symmPerSecond().call(block_identifier=block)) * alloc_point / total_alloc_point
    )
    result["reward_rates"].append(
        {
            "token": SYMM,
            "rewards_per_second": to_token_amount(SYMM, symm_per_second, blockchain, web3=web3, decimals=decimals),
        }
    )

    rewarder_contract_address = chef_contract.functions.rewarder(pool_id_farming).call(block_identifier=block)

    if rewarder_contract_address != Address.ZERO:
        rewarder_contract = get_contract(rewarder_contract_address, blockchain, web3=web3, abi=ABI_REWARDER)

        rewarder_pool_info = rewarder_contract.functions.poolInfo(pool_id_farming).call(block_identifier=block)
        rewarder_alloc_point = rewarder_pool_info[2]

        # Rewarder Total Allocation Point Calculation
        rewarder_total_alloc_point = 0
        for i in range(chef_contract.functions.poolLength().call(block_identifier=block)):
            rewarder_total_alloc_point += rewarder_contract.functions.poolInfo(i).call(block_identifier=block)[2]

        reward_address = rewarder_contract.functions.pendingTokens(pool_id_farming, Address.ZERO, 1).call(
            block_identifier=block
        )[0][0]

        try:
            reward_per_second = (
                Decimal(rewarder_contract.functions.rewardPerSecond().call(block_identifier=block))
                * Decimal(rewarder_alloc_point)
                / Decimal(rewarder_total_alloc_point)
            )
        except ContractLogicError:
            reward_per_second = 0

        result["reward_rates"].append(
            {
                "token": reward_address,
                "rewards_per_second": to_token_amount(
                    reward_address, reward_per_second, blockchain, web3=web3, decimals=decimals
                ),
            }
        )

    return result
