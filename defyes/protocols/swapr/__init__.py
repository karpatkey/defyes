import json
from decimal import Decimal
from pathlib import Path
from typing import List, Tuple

from defabipedia import Chain
from karpatkit.cache import const_call
from karpatkit.node import get_node
from tqdm import tqdm
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.functions import get_contract, get_decimals, get_logs_web3

# Staking Rewards Contract ETHEREUM
SRC_ETHEREUM = "0x156F0568a6cE827e5d39F6768A5D24B694e1EA7b"

# Staking Rewards Contract GNOSIS
SRC_GNOSIS = "0xa039793Af0bb060c597362E8155a0327d9b8BEE8"

# Staking Rewards Contract ABI - distributions, getDistributionsAmount
ABI_SRC = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"distributions","outputs":[{"internalType":"contract IERC20StakingRewardsDistribution","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getDistributionsAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Distribution ABI - stakableToken, stakers, getRewardTokens, claimableRewards
ABI_DISTRIBUTION = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"stakableToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"stake","internalType":"uint256"}],"name":"stakers","inputs":[{"type":"address","name":"","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address[]","name":"","internalType":"address[]"}],"name":"getRewardTokens","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"","internalType":"uint256[]"}],"name":"claimableRewards","inputs":[{"type":"address","name":"_account","internalType":"address"}]}]'

# LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast, swapFee
ABI_LPTOKEN = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true}, {"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint32","name":"","internalType":"uint32"}],"name":"swapFee","inputs":[],"constant":true}]'

# Swap Event Signature
SWAP_EVENT_SIGNATURE = "Swap(address,uint256,uint256,uint256,uint256,address)"


DB_FILE = Path(__file__).parent / "db.json"


def get_staking_rewards_contract(web3, block, blockchain):
    if blockchain == Chain.ETHEREUM:
        staking_rewards_contract = get_contract(SRC_ETHEREUM, blockchain, web3=web3, abi=ABI_SRC)

    elif blockchain == Chain.GNOSIS:
        staking_rewards_contract = get_contract(SRC_GNOSIS, blockchain, web3=web3, abi=ABI_SRC)

    return staking_rewards_contract


def get_distribution_contracts(web3, lptoken_address, staking_rewards_contract, campaigns, block, blockchain, db):
    distribution_contracts = []
    # FIXME: campaigns can be an int and a string

    if campaigns != 0:
        if db is True:
            with open(DB_FILE) as db_file:
                db_data = json.load(db_file)

            try:
                db_data[blockchain][lptoken_address]
                for i in range(campaigns):
                    try:
                        distribution_contracts.append(
                            get_contract(
                                db_data[blockchain][lptoken_address][i],
                                blockchain,
                                web3=web3,
                                abi=ABI_DISTRIBUTION,
                            )
                        )
                    except (ContractLogicError, BadFunctionCallOutput):
                        pass
            except KeyError:
                pass
        else:
            campaign_counter = 0

            distributions_amount = staking_rewards_contract.functions.getDistributionsAmount().call(
                block_identifier=block
            )

            for i in range(distributions_amount):
                # FIXME: this takes forever
                distribution_address = staking_rewards_contract.functions.distributions(
                    distributions_amount - (i + 1)
                ).call(block_identifier=block)
                distribution_contract = get_contract(distribution_address, blockchain, web3=web3, abi=ABI_DISTRIBUTION)
                stakable_token = distribution_contract.functions.stakableToken().call(block_identifier=block)

                if stakable_token.lower() == lptoken_address.lower():
                    distribution_contracts.append(distribution_contract)
                    campaign_counter += 1

                    # FIXME: it's unclear when this loop finishes
                    if campaigns == "all" or campaign_counter < campaigns:
                        continue
                    else:
                        break

    return distribution_contracts


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
    root_k_last = Decimal(lptoken_data["kLast"]).sqrt()

    if root_k > root_k_last:
        lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"] * 6 * root_k / (5 * root_k + root_k_last)
    else:
        lptoken_data["virtualTotalSupply"] = lptoken_data["totalSupply"]

    return lptoken_data


def get_all_rewards(
    wallet,
    lptoken_address,
    block,
    blockchain,
    web3=None,
    decimals=True,
    campaigns=1,
    distribution_contracts=None,
    db=True,
) -> List[Tuple]:
    """Get all Rewards

    Args:
        campaigns (int, optional): Number of campaigns from which the data is retrieved.
            if 0 it does not search for any campaign nor distribution contract.
            if "all" retrieves data from all campaigns Defaults to 1.

    Returns:
        List: List of (reward_token_address, balance)
    """
    all_rewards = []
    rewards = {}

    if web3 is None:
        web3 = get_node(blockchain)

    if distribution_contracts is None:
        staking_rewards_contract = get_staking_rewards_contract(web3, block, blockchain)
        distribution_contracts = get_distribution_contracts(
            web3, lptoken_address, staking_rewards_contract, campaigns, block, blockchain, db
        )

    if distribution_contracts == []:
        return []

    else:
        for distribution_contract in distribution_contracts:
            # TODO: check if const_call can bu used
            reward_tokens = distribution_contract.functions.getRewardTokens().call(block_identifier=block)
            claimable_rewards = distribution_contract.functions.claimableRewards(wallet).call(block_identifier=block)

            for i in range(len(reward_tokens)):
                reward_token_decimals = get_decimals(reward_tokens[i], blockchain, web3=web3) if decimals else 0

                reward_token_amount = Decimal(claimable_rewards[i]) / Decimal(10**reward_token_decimals)

                try:
                    rewards[reward_tokens[i]] += reward_token_amount
                except KeyError:
                    rewards[reward_tokens[i]] = reward_token_amount

        for key in rewards.keys():
            all_rewards.append([key, rewards[key]])

        return all_rewards


def underlying(
    wallet, lptoken_address, block, blockchain, web3=None, decimals=True, reward=False, campaigns=1, db=True
) -> List[Tuple]:
    """Get balances for liquidity tokens (staked and unstaked) and reward token.

    Args:
        campaigns (int, optional): Number of campaigns from which the data is retrieved.
            if 0 it does not search for any campaign nor distribution contract.
            if "all" retrieves data from all campaigns Defaults to 1.

    Returns:
        List[Tuple]: List of lists-> (liquidity_token_address, balance, staked_balance), (reward_token_address, balance)
    """
    balances = []
    distribution_contracts = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    staking_rewards_contract = get_staking_rewards_contract(web3, block, blockchain)
    distribution_contracts = get_distribution_contracts(
        web3, lptoken_address, staking_rewards_contract, campaigns, block, blockchain, db
    )

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    lptoken_data["staked"] = 0
    if distribution_contracts != []:
        for distribution_contract in distribution_contracts:
            lptoken_data["staked"] += distribution_contract.functions.stakers(wallet).call(block_identifier=block)

    lptoken_data["balanceOf"] = lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block)

    pool_balance_fraction = lptoken_data["balanceOf"] / lptoken_data["virtualTotalSupply"]
    pool_staked_fraction = lptoken_data["staked"] / lptoken_data["virtualTotalSupply"]

    for i in range(len(lptoken_data["reserves"])):
        try:
            getattr(lptoken_data["contract"].functions, "token" + str(i))
        except AttributeError:
            continue

        token_address = lptoken_data["token" + str(i)]

        token_decimals = get_decimals(token_address, blockchain, web3=web3) if decimals else 0

        token_balance = (
            Decimal(lptoken_data["reserves"][i]) / Decimal(10**token_decimals) * Decimal(pool_balance_fraction)
        )
        token_staked = (
            Decimal(lptoken_data["reserves"][i]) / Decimal(10**token_decimals) * Decimal(pool_staked_fraction)
        )

        balances.append([token_address, token_balance, token_staked])

    result = balances
    if reward:
        all_rewards = get_all_rewards(
            wallet,
            lptoken_address,
            block,
            blockchain,
            web3=web3,
            decimals=decimals,
            distribution_contracts=distribution_contracts,
            db=db,
        )

        result.extend(all_rewards)

    return result


def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True) -> List[Tuple]:
    """Returns: List of (liquidity_token_address, balance)"""
    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    reserves = lptoken_contract.functions.getReserves().call(block_identifier=block)

    for i in range(len(reserves)):
        try:
            func = getattr(lptoken_contract.functions, "token" + str(i))
        except AttributeError:
            continue

        token_address = const_call(func())

        token_decimals = get_decimals(token_address, blockchain, web3=web3) if decimals else 0

        token_balance = Decimal(reserves[i]) / Decimal(10**token_decimals)

        balances.append([token_address, token_balance])

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
        fee = lptoken_contract.functions.swapFee().call(block_identifier=swap_log["blockNumber"])
        if int(swap_log["data"].hex()[2:66], 16) == 0:
            token = token1
            amount = Decimal(fee) / Decimal(10000) * int(swap_log["data"].hex()[67:130], 16) / Decimal(10**decimals1)
        else:
            token = token0
            amount = Decimal(fee) / Decimal(10000) * int(swap_log["data"].hex()[2:66], 16) / Decimal(10**decimals0)

        swap_data = {"block": swap_log["blockNumber"], "token": token, "amount": amount}

        result["swaps"].append(swap_data)

    return result


def update_db(output_file=DB_FILE, block="latest"):
    try:
        with open(DB_FILE, "r") as db_file:
            db_data = json.load(db_file)
    except FileNotFoundError:
        db_data = {Chain.ETHEREUM: {}, Chain.GNOSIS: {}}

    blockchain = ""
    for blockchain in tqdm(db_data, desc="Fetching data from blockchains..."):
        web3 = get_node(blockchain)

        staking_rewards_contract = get_staking_rewards_contract(web3, block, blockchain)

        distributions_amount = staking_rewards_contract.functions.getDistributionsAmount().call(block_identifier=block)

        for i in tqdm(range(distributions_amount), desc="Fetching distributors..."):
            distribution_address = staking_rewards_contract.functions.distributions(
                distributions_amount - (i + 1)
            ).call(block_identifier=block)
            distribution_contract = get_contract(distribution_address, blockchain, web3=web3, abi=ABI_DISTRIBUTION)
            stakable_token = distribution_contract.functions.stakableToken().call(block_identifier=block)

            try:
                db_data[blockchain][stakable_token]
            except KeyError:
                db_data[blockchain][stakable_token] = []

            db_data[blockchain][stakable_token].append(Web3.to_checksum_address(distribution_address))

        with open(output_file, "w") as db_file:
            json.dump(db_data, db_file)
