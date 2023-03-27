import os
import json
import math
from pathlib import Path

from tqdm import tqdm

from defi_protocols.functions import get_node, get_contract, get_decimals, get_logs, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS, ETHEREUM, XDAI

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# STAKING REWARDS CONTRACT ADDRESSES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETHEREUM
SRC_ETHEREUM = '0x156F0568a6cE827e5d39F6768A5D24B694e1EA7b'

# XDAI
SRC_XDAI = '0xa039793Af0bb060c597362E8155a0327d9b8BEE8'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Staking Rewards Contract ABI - distributions, getDistributionsAmount
ABI_SRC = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"distributions","outputs":[{"internalType":"contract IERC20StakingRewardsDistribution","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getDistributionsAmount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# Distribution ABI - stakableToken, stakers, getRewardTokens, claimableRewards
ABI_DISTRIBUTION = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":"","internalType":"contract IERC20"}],"name":"stakableToken","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"stake","internalType":"uint256"}],"name":"stakers","inputs":[{"type":"address","name":"","internalType":"address"}]}, {"type":"function","stateMutability":"view","outputs":[{"type":"address[]","name":"","internalType":"address[]"}],"name":"getRewardTokens","inputs":[]}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256[]","name":"","internalType":"uint256[]"}],"name":"claimableRewards","inputs":[{"type":"address","name":"_account","internalType":"address"}]}]'

# LP Token ABI - decimals, totalSupply, getReserves, balanceOf, token0, token1, kLast, swapFee
ABI_LPTOKEN = '[{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint8","name":"","internalType":"uint8"}],"name":"decimals","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"totalSupply","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint112","name":"_reserve0","internalType":"uint112"},{"type":"uint112","name":"_reserve1","internalType":"uint112"},{"type":"uint32","name":"_blockTimestampLast","internalType":"uint32"}],"name":"getReserves","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"balanceOf","inputs":[{"type":"address","name":"","internalType":"address"}],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token0","inputs":[],"constant":true}, {"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"address","name":"","internalType":"address"}],"name":"token1","inputs":[],"constant":true}, {"inputs":[],"name":"kLast","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"type":"function","stateMutability":"view","payable":false,"outputs":[{"type":"uint32","name":"","internalType":"uint32"}],"name":"swapFee","inputs":[],"constant":true}]'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EVENT SIGNATURES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Swap Event Signature
SWAP_EVENT_SIGNATURE = 'Swap(address,uint256,uint256,uint256,uint256,address)'


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_staking_rewards_contract
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_staking_rewards_contract(web3, block, blockchain):
    """

    :param web3:
    :param block:
    :param blockchain:
    :return:
    """
    if blockchain == ETHEREUM:
        staking_rewards_contract = get_contract(SRC_ETHEREUM, blockchain, web3=web3, abi=ABI_SRC, block=block)

    elif blockchain == XDAI:
        staking_rewards_contract = get_contract(SRC_XDAI, blockchain, web3=web3, abi=ABI_SRC, block=block)

    return staking_rewards_contract


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_distribution_contracts
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_distribution_contracts(web3, lptoken_address, staking_rewards_contract, campaigns, block, blockchain, db):
    """

    :param web3:
    :param lptoken_address:
    :param staking_rewards_contract:
    :param campaigns:
    :param block:
    :param blockchain:
    :return:
    """
    distribution_contracts = []

    if campaigns != 0:
        if db is True:
            with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Swapr_db.json', 'r') as db_file:
                db_data = json.load(db_file)

            try:
                db_data[blockchain][lptoken_address]
                for i in range(campaigns):
                    try:
                        distribution_contracts.append(
                            get_contract(db_data[blockchain][lptoken_address][i], blockchain, web3=web3,
                                         abi=ABI_DISTRIBUTION, block=block))
                    except:
                        pass
            except:
                pass
        else:
            campaign_counter = 0

            distributions_amount = staking_rewards_contract.functions.getDistributionsAmount().call(
                block_identifier=block)

            for i in range(distributions_amount):
                distribution_address = staking_rewards_contract.functions.distributions(
                    distributions_amount - (i + 1)).call(block_identifier=block)
                distribution_contract = get_contract(distribution_address, blockchain, web3=web3, abi=ABI_DISTRIBUTION,
                                                     block=block)
                stakable_token = distribution_contract.functions.stakableToken().call()

                if stakable_token.lower() == lptoken_address.lower():
                    distribution_contracts.append(distribution_contract)
                    campaign_counter += 1

                    if campaigns == 'all' or campaign_counter < campaigns:
                        continue
                    else:
                        break

    return distribution_contracts


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None, execution=1, index=0):
    """

    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lptoken_data = {}

        lptoken_data['contract'] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

        lptoken_data['decimals'] = lptoken_data['contract'].functions.decimals().call()
        lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(block_identifier=block)
        lptoken_data['token0'] = lptoken_data['contract'].functions.token0().call()
        lptoken_data['token1'] = lptoken_data['contract'].functions.token1().call()
        lptoken_data['reserves'] = lptoken_data['contract'].functions.getReserves().call(block_identifier=block)
        lptoken_data['kLast'] = lptoken_data['contract'].functions.kLast().call(block_identifier=block)

        root_k = math.sqrt(lptoken_data['reserves'][0] * lptoken_data['reserves'][1])
        root_k_last = math.sqrt(lptoken_data['kLast'])

        if root_k > root_k_last:
            lptoken_data['virtualTotalSupply'] = lptoken_data['totalSupply'] * 6 * root_k / (5 * root_k + root_k_last)
        else:
            lptoken_data['virtualTotalSupply'] = lptoken_data['totalSupply']

        return lptoken_data

    except GetNodeIndexError:
        return get_lptoken_data(lptoken_address, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_lptoken_data(lptoken_address, block, blockchain, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'distribution_contracts' -> Improves performance
# 'campaigns' = number of campaigns from which the data is retrieved /
# 'campaigns' = 0 it does not search for any campaign nor distribution contract
# 'campaigns' = 'all' retrieves the data from all campaigns
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True,
                    campaigns=1, distribution_contracts=None, db=True):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param campaigns:
    :param distribution_contracts:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    all_rewards = []
    rewards = {}

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        if distribution_contracts == None:
            staking_rewards_contract = get_staking_rewards_contract(web3, block, blockchain)
            distribution_contracts = get_distribution_contracts(web3, lptoken_address, staking_rewards_contract,
                                                                campaigns, block, blockchain, db)

        if distribution_contracts == []:
            return []

        else:
            for distribution_contract in distribution_contracts:
                reward_tokens = distribution_contract.functions.getRewardTokens().call()
                claimable_rewards = distribution_contract.functions.claimableRewards(wallet).call(
                    block_identifier=block)

                for i in range(len(reward_tokens)):

                    if decimals is True:
                        reward_token_decimals = get_decimals(reward_tokens[i], blockchain, web3=web3)
                    else:
                        reward_token_decimals = 0

                    reward_token_amount = claimable_rewards[i] / (10 ** reward_token_decimals)

                    try:
                        rewards[reward_tokens[i]] += reward_token_amount
                    except:
                        rewards[reward_tokens[i]] = reward_token_amount

            for key in rewards.keys():
                all_rewards.append([key, rewards[key]])

            return all_rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, campaigns=campaigns,
                               distribution_contracts=distribution_contracts, db=db, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, campaigns=campaigns,
                               distribution_contracts=distribution_contracts, db=db, index=index + 1,
                               execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'campaigns' = number of campaigns from which the data is retrieved /
# 'campaigns' = 0 it does not search for any campaign nor distribution contract
# 'campaigns' = 'all' retrieves the data from all campaigns
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, reward=False,
               campaigns=1, db=True):
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
    :param campaigns:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    result = []
    balances = []
    distribution_contracts = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        staking_rewards_contract = get_staking_rewards_contract(web3, block, blockchain)
        distribution_contracts = get_distribution_contracts(web3, lptoken_address, staking_rewards_contract, campaigns,
                                                            block, blockchain, db)

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

        lptoken_data['staked'] = 0
        if distribution_contracts != []:
            for distribution_contract in distribution_contracts:
                lptoken_data['staked'] += distribution_contract.functions.stakers(wallet).call(block_identifier=block)

        lptoken_data['balanceOf'] = lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)

        pool_balance_fraction = lptoken_data['balanceOf'] / lptoken_data['virtualTotalSupply']
        pool_staked_fraction = lptoken_data['staked'] / lptoken_data['virtualTotalSupply']

        for i in range(len(lptoken_data['reserves'])):
            try:
                getattr(lptoken_data['contract'].functions, 'token' + str(i))
            except:
                continue

            token_address = lptoken_data['token' + str(i)]

            if decimals is True:
                token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_decimals = 0

            token_balance = lptoken_data['reserves'][i] / (10 ** token_decimals) * (pool_balance_fraction)
            token_staked = lptoken_data['reserves'][i] / (10 ** token_decimals) * (pool_staked_fraction)

            balances.append([token_address, token_balance, token_staked])

        if reward is True:
            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                          distribution_contracts=distribution_contracts, db=db)

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying(wallet, lptoken_address, block, blockchain, campaigns=campaigns, reward=reward, db=db,
                          decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying(wallet, lptoken_address, block, blockchain, campaigns=campaigns, reward=reward, db=db,
                          decimals=decimals, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 element:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

        reserves = lptoken_contract.functions.getReserves().call(block_identifier=block)

        for i in range(len(reserves)):
            try:
                func = getattr(lptoken_contract.functions, 'token' + str(i))
            except:
                continue

            token_address = func().call()

            if decimals is True:
                token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_balance = 0

            token_balance = reserves[i] / (10 ** token_decimals)

            balances.append([token_address, token_balance])

        return balances

    except GetNodeIndexError:
        return pool_balances(lptoken_address, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return pool_balances(lptoken_address, block, blockchain, decimals=decimals, index=index + 1,
                             execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# swap_fees
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param lptoken_address:
    :param block_start:
    :param block_end:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    result = {}
    hash_overlap = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block_start, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block_start)

        token0 = lptoken_contract.functions.token0().call()
        token1 = lptoken_contract.functions.token1().call()
        result['swaps'] = []

        if decimals is True:
            decimals0 = get_decimals(token0, blockchain, web3=web3)
            decimals1 = get_decimals(token1, blockchain, web3=web3)
        else:
            decimals0 = 0
            decimals1 = 0

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

                    fee = lptoken_contract.functions.swapFee().call(block_identifier=block_number)

                    if int(swap_log['data'][2:66], 16) == 0:
                        swap_data = {
                            'block': block_number,
                            'token': token1,
                            'amount': fee / 10000 * int(swap_log['data'][67:130], 16) / (10 ** decimals1)
                        }
                    else:
                        swap_data = {
                            'block': block_number,
                            'token': token0,
                            'amount': fee / 10000 * int(swap_log['data'][2:66], 16) / (10 ** decimals0)
                        }

                    result['swaps'].append(swap_data)

            if log_count < 1000:
                get_logs_bool = False

            else:
                block_from = block_number

        return result

    except GetNodeIndexError:
        return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals=decimals, index=0,
                         execution=execution + 1)

    except:
        return swap_fees(lptoken_address, block_start, block_end, blockchain, decimals=decimals, index=index + 1,
                         execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_db
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db():
    """

    :return:
    """
    try:
        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Swapr_db.json', 'r') as db_file:
            db_data = json.load(db_file)
    except:
        db_data = {
            ETHEREUM: {},
            XDAI: {}
        }

    blockchain = ''
    for blockchain in tqdm(db_data, desc='Fetching data from blockchains...'):

        web3 = get_node(blockchain)

        staking_rewards_contract = get_staking_rewards_contract(web3, 'latest', blockchain)

        distributions_amount = staking_rewards_contract.functions.getDistributionsAmount().call()

        for i in tqdm(range(distributions_amount), desc='Fetching distributors...'):
            distribution_address = staking_rewards_contract.functions.distributions(
                distributions_amount - (i + 1)).call()
            distribution_contract = get_contract(distribution_address, blockchain, web3=web3, abi=ABI_DISTRIBUTION)
            stakable_token = distribution_contract.functions.stakableToken().call()

            try:
                db_data[blockchain][stakable_token]
            except:
                db_data[blockchain][stakable_token] = []

            db_data[blockchain][stakable_token].append(web3.to_checksum_address(distribution_address))

        with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Swapr_db.json', 'w') as db_file:
            json.dump(db_data, db_file)
