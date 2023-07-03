import json
import logging
from decimal import Decimal
from pathlib import Path

from web3 import Web3

from defyes import Curve
from defyes.cache import const_call
from defyes.constants import CVX_ETH, CVXCRV_ETH, ETHEREUM
from defyes.functions import get_contract, get_contract_creation, get_node, last_block, to_token_amount

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BACKLOG LIST
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rewards when you stake CVX

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BOOSTER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster (Main Deposit Contract) Address
BOOSTER = "0xF403C135812408BFbE8713b5A23a04b3D48AAE31"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX REWARDS TOKEN ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX rewards token address
CVX_STAKER = "0xCF50b810E57Ac33B91dCF525C6ddd9881B139332"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX LOCKER TOKEN ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CVX locker token address
CVX_LOCKER = "0x72a19342e8F1838460eBFCCEf09F6585e32db86E"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Booster ABI - poolInfo, poolLength
ABI_BOOSTER = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"address","name":"lptoken","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"gauge","type":"address"},{"internalType":"address","name":"crvRewards","type":"address"},{"internalType":"address","name":"stash","type":"address"},{"internalType":"bool","name":"shutdown","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Rewards ABI - balanceOf, totalSupply, earned, rewardToken, extraRewardsLength, extraRewards
ABI_REWARDS = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# CVX ABI - reductionPerCliff, totalCliffs, maxSupply, totalSupply
ABI_CVX = '[{"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"maxSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

DB_FILE = Path(__file__).parent / "db" / "Convex_db.json"


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_rewarders
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_rewarders(lptoken_address, block):
    if isinstance(block, str):
        if block == "latest":
            block = last_block(ETHEREUM)
        else:
            raise ValueError("Incorrect block.")

    with open(DB_FILE, "r") as db_file:
        db_data = json.load(db_file)

    rewarders = []
    if lptoken_address in db_data["pools"].keys():
        blocks = list(db_data["pools"][lptoken_address].keys())[::-1]
        for iblock in blocks:
            if block >= int(iblock):
                rewarders.append(db_data["pools"][lptoken_address][iblock]["rewarder"])

    else:
        booster_contract = get_contract(BOOSTER, ETHEREUM, abi=ABI_BOOSTER, block=block)
        number_of_pools = booster_contract.functions.poolLength().call(block_identifier=block)

        for pool_id in range(number_of_pools):
            pool_info = booster_contract.functions.poolInfo(pool_id).call(block_identifier=block)
            address = pool_info[0]

            if address == lptoken_address:
                rewarders.append(pool_info[3])
            else:
                continue

    return rewarders


def get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):
    """
    Output:
        Tuples: [token_address, balance]
    """
    reward_token_address = const_call(rewarder_contract.functions.rewardToken())
    bal_rewards = rewarder_contract.functions.earned(wallet).call(block_identifier=block)

    return [reward_token_address, to_token_amount(reward_token_address, bal_rewards, blockchain, web3, decimals)]


def get_extra_rewards(web3, crv_rewards_contract, wallet, block, blockchain, decimals=True):
    """
    Output: List of Tuples: [reward_token_address, balance]
    """
    extra_rewards = []

    extra_rewards_length = crv_rewards_contract.functions.extraRewardsLength().call(block_identifier=block)

    for i in range(extra_rewards_length):
        extra_reward_contract_address = crv_rewards_contract.functions.extraRewards(i).call(block_identifier=block)
        extra_reward_contract = get_contract(
            extra_reward_contract_address, blockchain, web3=web3, abi=ABI_REWARDS, block=block
        )

        extra_reward_token_address = const_call(extra_reward_contract.functions.rewardToken())
        extra_reward = extra_reward_contract.functions.earned(wallet).call(block_identifier=block)

        extra_rewards.append(
            [
                extra_reward_token_address,
                to_token_amount(extra_reward_token_address, extra_reward, blockchain, web3, decimals),
            ]
        )

    return extra_rewards


def get_cvx_mint_amount(web3, crv_earned, block, blockchain, decimals=True):
    """
    Output:
        Tuple: [cvx_token_address, minted_amount]
    """
    cvx_amount = 0

    cvx_contract = get_contract(CVX_ETH, blockchain, web3=web3, abi=ABI_CVX, block=block)

    cliff_size = cvx_contract.functions.reductionPerCliff().call(block_identifier=block)
    cliff_count = cvx_contract.functions.totalCliffs().call(block_identifier=block)
    max_supply = cvx_contract.functions.maxSupply().call(block_identifier=block)

    cvx_total_supply = cvx_contract.functions.totalSupply().call(block_identifier=block)

    current_cliff = cvx_total_supply / cliff_size

    if current_cliff < cliff_count:
        remaining = cliff_count - current_cliff
        cvx_amount = crv_earned * Decimal(remaining / cliff_count)
        amount_till_max = max_supply - cvx_total_supply

        if cvx_amount > amount_till_max:
            cvx_amount = amount_till_max

    return [CVX_ETH, cvx_amount]


def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, rewarders=[]):
    """
    Output:
        List of Tuples: [reward_token_address, balance]
    """
    all_rewards = {}

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if rewarders == []:
        rewarders = get_pool_rewarders(lptoken_address, block)

    for rewarder in rewarders:
        rewarder_contract = get_contract(rewarder, blockchain, web3=web3, abi=ABI_REWARDS, block=block)

        crv_rewards = get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=decimals)
        if crv_rewards[0] in all_rewards.keys():
            all_rewards[crv_rewards[0]] += crv_rewards[1]
        else:
            all_rewards[crv_rewards[0]] = crv_rewards[1]

        # crv_rewards[1] = crv_rewards_amount - cvx_mint_amount is calculated using the crv_rewards_amount
        if crv_rewards[1] >= 0:
            cvx_mint_amount = get_cvx_mint_amount(web3, crv_rewards[1], block, blockchain, decimals=decimals)

            if len(cvx_mint_amount) > 0:
                if cvx_mint_amount[0] in all_rewards.keys():
                    all_rewards[cvx_mint_amount[0]] += cvx_mint_amount[1]
                else:
                    all_rewards[cvx_mint_amount[0]] = cvx_mint_amount[1]

        extra_rewards = get_extra_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=decimals)

        if len(extra_rewards) > 0:
            for extra_reward in extra_rewards:
                if extra_reward[0] in all_rewards.keys():
                    all_rewards[extra_reward[0]] += extra_reward[1]
                else:
                    all_rewards[extra_reward[0]] = extra_reward[1]

    return all_rewards


def get_locked(wallet, block, blockchain, web3=None, reward=False, decimals=True):
    """
    Output:
    1 - List of Tuples: [cvx_token_address, locked_balance]
    2 - List of Tuples: [reward_token_address, balance]
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    cvx_locker_contract = get_contract(CVX_LOCKER, blockchain, web3=web3, block=block)
    cvx_locker = cvx_locker_contract.functions.balances(wallet).call(block_identifier=block)[0]

    result = [[CVX_ETH, to_token_amount(CVX_ETH, cvx_locker, blockchain, web3, decimals)]]

    if reward:
        rewards = []
        cvx_locker_rewards = cvx_locker_contract.functions.claimableRewards(wallet).call(block_identifier=block)

        for cvx_locker_reward in cvx_locker_rewards:
            if cvx_locker_reward[1] > 0:
                rewards.append(
                    [
                        cvx_locker_reward[0],
                        to_token_amount(cvx_locker_contract[0], cvx_locker_reward[1], blockchain, web3, decimals),
                    ]
                )

        result += rewards

    return result


def get_staked(wallet, block, blockchain, web3=None, reward=False, decimals=True):
    """
    Output:
    1 - List of Tuples: [cvx_token_address, staked_balance]
    2 - List of Tuples: [reward_token_address, balance]
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    cvx_staking_contract = get_contract(CVX_STAKER, blockchain, web3=web3, block=block)
    cvx_staked = cvx_staking_contract.functions.balanceOf(wallet).call(block_identifier=block)

    result = [[CVX_ETH, to_token_amount(CVX_ETH, cvx_staked, blockchain, web3, decimals)]]

    if reward:
        rewards = []
        cvx_staked_rewards = cvx_staking_contract.functions.earned(wallet).call(block_identifier=block)

        if cvx_staked_rewards > 0:
            rewards.append([CVXCRV_ETH, to_token_amount(CVXCRV_ETH, cvx_staked_rewards, blockchain, web3, decimals)])

        result += rewards

    return result


def underlying(
    wallet, lptoken_address, block, blockchain, web3=None, reward=False, decimals=True, no_curve_underlying=False
):
    """
    'no_curve_underlying' = True -> retrieves the LP Token balance /
    'no_curve_underlying' = False or not passed onto the function -> retrieves the balance of the underlying Curve tokens
    Output: a list with 2 elements:
    1 - List of Tuples: [liquidity_token_address, balance, staked_balance] | [liquidity_token_address, staked_balance] -> depending on 'no_curve_underlying' value
    2 - List of Tuples: [reward_token_address, balance]
    """
    result = {}
    balances = {}

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    rewarders = get_pool_rewarders(lptoken_address, block)

    for rewarder in rewarders:
        rewarder_contract = get_contract(rewarder, blockchain, web3=web3, abi=ABI_REWARDS, block=block)
        lptoken_staked = rewarder_contract.functions.balanceOf(wallet).call(block_identifier=block)

        if no_curve_underlying is False:
            curve_data = Curve.underlying(
                wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals, convex_staked=lptoken_staked
            )
            for i in range(len(curve_data)):
                if curve_data[i][0] in balances.keys():
                    balances[curve_data[i][0]] += curve_data[i][1]
                else:
                    balances[curve_data[i][0]] = curve_data[i][1]
        else:
            balances[lptoken_address] = to_token_amount(lptoken_address, lptoken_staked, blockchain, web3, decimals)

        result["balances"] = balances

        if reward and rewarders != []:
            all_rewards = get_all_rewards(
                wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals, rewarders=rewarders
            )

            result["rewards"] = all_rewards

    return result


def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):
    """
    # Output: a list with 2 elements:
    # 1 - List of Tuples: [liquidity_token_address, balance]
    """
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    balances = Curve.pool_balances(lptoken_address, block, blockchain, web3=web3, decimals=decimals)

    return balances


def update_db(output_file=DB_FILE, block="latest"):
    db_data = {"pools": {}}

    web3 = get_node(ETHEREUM, block=block)
    booster = get_contract(BOOSTER, ETHEREUM, web3=web3, abi=ABI_BOOSTER, block=block)
    pools_length = booster.functions.poolLength().call(block_identifier=block)

    for i in range(pools_length):
        pool_info = booster.functions.poolInfo(i).call(block_identifier=block)  # can't be const_call!

        rewarder_data = get_contract_creation(pool_info[3], ETHEREUM)
        rewarder_creation_tx = web3.eth.get_transaction(rewarder_data[0]["txHash"])

        if pool_info[0] in db_data["pools"].keys():
            db_data["pools"][pool_info[0]][rewarder_creation_tx["blockNumber"]] = {
                "poolId": i,
                "rewarder": pool_info[3],
            }
        else:
            db_data["pools"][pool_info[0]] = {
                rewarder_creation_tx["blockNumber"]: {"poolId": i, "rewarder": pool_info[3]}
            }

    with open(output_file, "w") as db_file:
        json.dump(db_data, db_file, indent=2)

    return db_data
