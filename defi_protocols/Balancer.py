from datetime import datetime, timedelta
from decimal import Decimal
from itertools import groupby
from operator import itemgetter
from typing import Union
from web3.exceptions import ContractLogicError, BadFunctionCallOutput
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, get_decimals, block_to_date, date_to_block, balance_of, get_logs, to_token_amount
from defi_protocols.constants import ETHEREUM, XDAI, BAL_ETH, BAL_ARB, BAL_XDAI, BB_A_USD_OLD_ETH, BB_A_USD_ETH, POLYGON, ARBITRUM, BAL_POL, ZERO_ADDRESS
from defi_protocols.prices.prices import get_price

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BALANCER VAULT
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault Contract Address
VAULT = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LIQUIDITY GAUGE FACTORY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ETHEREUM = '0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC'

# Polygon Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_POLYGON = '0x3b8cA519122CdD8efb272b0D3085453404B25bD0'

# Arbitrum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ARBITRUM = '0xb08E16cFc07C684dAA2f93C70323BAdb2A6CBFd2'

# GC Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_XDAI = "0x809B79b53F18E9bc08A961ED4678B901aC93213a"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL Contract Address
VEBAL = '0xC128a9954e6c874eA3d62ce62B468bA073093F25'

# veBAL Fee Distributor Contract
VEBAL_FEE_DISTRIBUTOR = '0xD3cf852898b21fc233251427c2DC93d3d604F3BB'
# VEBAL_FEE_DISTRIBUTOR = '0x26743984e3357eFC59f2fd6C1aFDC310335a61c9' #DEPRECATED

# veBAL Reward Tokens - BAL, bb-a-USD old deployment, bb-a-USD
VEBAL_REWARD_TOKENS = [BAL_ETH, BB_A_USD_OLD_ETH, BB_A_USD_ETH]

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHILD CHAIN GAUGE REWARD HELPER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GC Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_XDAI = '0xf7D5DcE55E6D47852F054697BAB6A1B48A00ddbd'

# Polygon Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_POLYGON = '0xaEb406b0E430BF5Ea2Dc0B9Fe62E4E53f74B3a33'

# Arbitrum Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_ARBITRUM = '0xA0DAbEBAAd1b243BBb243f933013d560819eB66f'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault ABI - getPoolTokens, getPool
ABI_VAULT = '[{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPoolTokens","outputs":[{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"enum IVault.PoolSpecialization","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# Liquidity Gauge Factory ABI - getPoolGauge
ABI_LIQUIDITY_GAUGE_FACTORY = '[{"inputs":[{"internalType":"address","name":"pool","type":"address"}],"name":"getPoolGauge","outputs":[{"internalType":"contract ILiquidityGauge","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# veBAL ABI - locked, token
ABI_VEBAL = '[{"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"locked","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"tuple","components":[{"name":"amount","type":"int128"},{"name":"end","type":"uint256"}]}]}]'

# veBAL Fee Distributor ABI - claimTokens
ABI_VEBAL_FEE_DISTRIBUTOR = '[{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"}],"name":"claimTokens","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"}]'

# LP Token ABI - getPoolId, decimals, getActualSupply, getVirtualSupply, totalSupply, getBptIndex, balanceOf, getSwapFeePercentage, getRate, getScalingFactors
ABI_LPTOKEN = '[{"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getActualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getVirtualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getBptIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getSwapFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getScalingFactors","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]'

# Gauge ABI - claimable_tokens, claimable_reward, reward_count, reward_tokens, reward_contract
ABI_GAUGE = '[{"stateMutability":"nonpayable","type":"function","name":"claimable_tokens","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"claimable_reward","inputs":[{"name":"_user","type":"address"},{"name":"_reward_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_tokens","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"reward_contract","inputs":[],"outputs":[{"name":"","type":"address"}]}]'

# ABI Pool Tokens - decimals, getRate, UNDERLYING_ASSET_ADDRESS, rate, stETH
ABI_POOL_TOKENS_BALANCER = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getMainToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"UNDERLYING_ASSET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"stETH","outputs":[{"internalType":"contract IStETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# ABI Child Gauge Reward Helper - getPendingRewards
ABI_CHILD_CHAIN_GAUGE_REWARD_HELPER = '[{"inputs":[{"internalType":"contract IRewardsOnlyGauge","name":"gauge","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"token","type":"address"}],"name":"getPendingRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]'

# ABI Child Chain Streamer - reward_count
ABI_CHILD_CHAIN_STREAMER = '[{"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}]'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EVENT SIGNATURES
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Swap Event Signature
SWAP_EVENT_SIGNATURE = 'Swap(bytes32,address,address,uint256,uint256)'


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# call_contract_method
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def call_contract_method(method, block):
    try:
        return method.call(block_identifier = block)
    except Exception as e:
        if type(e) == ContractLogicError or type(e) == BadFunctionCallOutput or \
                (type(e) == ValueError and (e.args[0]['code'] == -32000 or e.args[0]['code'] == -32015)):
            return None
        else:
            raise e
        

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_gauge_factory_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_gauge_factory_address(blockchain):
    if blockchain == ETHEREUM:
        return LIQUIDITY_GAUGE_FACTORY_ETHEREUM

    elif blockchain == POLYGON:
        return LIQUIDITY_GAUGE_FACTORY_POLYGON

    elif blockchain == ARBITRUM:
        return LIQUIDITY_GAUGE_FACTORY_ARBITRUM

    elif blockchain == XDAI:
        return LIQUIDITY_GAUGE_FACTORY_XDAI


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_gauge_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_gauge_address(blockchain, block, web3, lptoken_addr):
    gauge_factory_address = get_gauge_factory_address(blockchain)
    gauge_factory_contract = get_contract(gauge_factory_address, blockchain, web3=web3,
                                          abi=ABI_LIQUIDITY_GAUGE_FACTORY, block=block)

    return gauge_factory_contract.functions.getPoolGauge(lptoken_addr).call()


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None):

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_data = {}

    lptoken_data['contract'] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)
    lptoken_data['poolId'] = lptoken_data['contract'].functions.getPoolId().call()
    lptoken_data['decimals'] = lptoken_data['contract'].functions.decimals().call()

    try:
        lptoken_data['totalSupply'] = lptoken_data['contract'].functions.getActualSupply().call(
            block_identifier=block)
        lptoken_data['isBoosted'] = True
    except:
        try:
            lptoken_data['totalSupply'] = lptoken_data['contract'].functions.getVirtualSupply().call(
                block_identifier=block)
            lptoken_data['isBoosted'] = True
        except:
            lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(
                block_identifier=block)
            lptoken_data['isBoosted'] = False

    if lptoken_data['isBoosted'] == True:
        try:
            lptoken_data['bptIndex'] = lptoken_data['contract'].functions.getBptIndex().call()
        except:
            lptoken_data['isBoosted'] = False
            lptoken_data['bptIndex'] = None
    else:
        lptoken_data['bptIndex'] = None
    
    try:
        lptoken_data['scalingFactors'] = lptoken_data['contract'].functions.getScalingFactors().call(block_identifier=block)
    except:
        lptoken_data['scalingFactors'] = None

    return lptoken_data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_address(blockchain):
    if blockchain == ETHEREUM:
        return BAL_ETH
    elif blockchain == POLYGON:
        return BAL_POL
    elif blockchain == ARBITRUM:
        return BAL_ARB
    elif blockchain == XDAI:
        return BAL_XDAI


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_child_chain_reward_helper_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_child_chain_reward_helper_address(blockchain):
    if blockchain == XDAI:
        return CHILD_CHAIN_GAUGE_REWARD_HELPER_XDAI
    elif blockchain == POLYGON: 
        return CHILD_CHAIN_GAUGE_REWARD_HELPER_POLYGON
    elif blockchain == ARBITRUM:
        return CHILD_CHAIN_GAUGE_REWARD_HELPER_ARBITRUM
    

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_bal_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_bal_rewards(web3, gauge_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param gauge_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    bal_address = get_bal_address(blockchain)
    bal_rewards = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block)

    return [bal_address, to_token_amount(bal_address, bal_rewards, blockchain, web3, decimals)]


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rewards(web3, gauge_contract, wallet, block, blockchain, decimals=True):
    """

    :param web3:
    :param gauge_contract:
    :param wallet:
    :param block:
    :param blockchain:
    :param decimals:
    :return:
    """
    rewards = []

    if blockchain == ETHEREUM:
        reward_count = gauge_contract.functions.reward_count().call(block_identifier=block)
    else:
        child_chain_streamer_contract = get_contract(gauge_contract.functions.reward_contract().call(), blockchain, 
                                                     web3=web3, abi=ABI_CHILD_CHAIN_STREAMER, block=block)
        reward_count = child_chain_streamer_contract.functions.reward_count().call(block_identifier=block)

    for i in range(reward_count):

        token_address = gauge_contract.functions.reward_tokens(i).call()

        if blockchain == ETHEREUM:
            token_rewards = gauge_contract.functions.claimable_reward(wallet, token_address).call(block_identifier=block)
        else:
            child_chain_reward_helper_contract = get_contract(get_child_chain_reward_helper_address(blockchain), blockchain, 
                                                 web3=web3, abi=ABI_CHILD_CHAIN_GAUGE_REWARD_HELPER, block=block)
            token_rewards = child_chain_reward_helper_contract.functions.getPendingRewards(gauge_contract.address, 
                                                                        wallet, token_address).call(block_identifier=block)

        rewards.append([token_address, to_token_amount(token_address, token_rewards, blockchain, web3, decimals)])

    return rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vebal_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vebal_rewards(web3, wallet, block, blockchain, decimals=True):
    vebal_rewards = []

    fee_distributor_contract = get_contract(VEBAL_FEE_DISTRIBUTOR, blockchain, web3=web3, abi=ABI_VEBAL_FEE_DISTRIBUTOR,
                                            block=block)
    claim_tokens = fee_distributor_contract.functions.claimTokens(wallet, VEBAL_REWARD_TOKENS).call(
        block_identifier=block)

    for i in range(len(VEBAL_REWARD_TOKENS)):
        token_address = VEBAL_REWARD_TOKENS[i]
        token_rewards = claim_tokens[i]

        vebal_rewards.append([token_address, to_token_amount(token_address, token_rewards, blockchain, web3, decimals)])

    return vebal_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, gauge_address=None):

    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if gauge_address is None:
        gauge_address = get_gauge_address(blockchain, block, web3, lptoken_address)

    # veBAL Rewards
    if blockchain == ETHEREUM:
        vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

        if (lptoken_address == vebal_contract.functions.token().call()):
            vebal_rewards = get_vebal_rewards(web3, wallet, block, blockchain, decimals=decimals)

            if len(vebal_rewards) > 0:
                for vebal_reward in vebal_rewards:
                    all_rewards.append(vebal_reward)

    if gauge_address != ZERO_ADDRESS:
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)

        if blockchain == ETHEREUM:
            bal_rewards = get_bal_rewards(web3, gauge_contract, wallet, block, blockchain)
            all_rewards.append(bal_rewards)

        # In side-chains, BAL rewards are retrieved with the get_rewards function too
        rewards = get_rewards(web3, gauge_contract, wallet, block, blockchain)

        if len(rewards) > 0:
            for reward in rewards:
                all_rewards.append(reward)

    return all_rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, reward=False, aura_staked=None, decimals=True):

    result = []
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    gauge_factory_address = get_gauge_factory_address(blockchain)
    gauge_factory_contract = get_contract(gauge_factory_address, blockchain, web3=web3,
                                            abi=ABI_LIQUIDITY_GAUGE_FACTORY, block=block)

    gauge_address = gauge_factory_contract.functions.getPoolGauge(lptoken_address).call()

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)
    lptoken_data['balanceOf'] = Decimal(lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block))

    if gauge_address != ZERO_ADDRESS:
        lptoken_data['staked'] = balance_of(wallet, gauge_address, block, blockchain, web3=web3, decimals=False)
    else:
        lptoken_data['staked'] = Decimal(0)

    lptoken_data['locked'] = Decimal(0)
    if blockchain == ETHEREUM:
        vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

        if lptoken_address == vebal_contract.functions.token().call():
            try:
                lptoken_data['locked'] = Decimal(vebal_contract.functions.locked(wallet).call(block_identifier=block)[0])
            except:
                pass

    pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
    pool_tokens = pool_tokens_data[0]
    pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

    pool_balance_fraction = lptoken_data['balanceOf'] / lptoken_data['totalSupply']
    pool_staked_fraction = lptoken_data['staked'] / lptoken_data['totalSupply']
    pool_locked_fraction = lptoken_data['locked'] / lptoken_data['totalSupply']

    for i in range(len(pool_tokens)):

        if i == lptoken_data['bptIndex']:
            continue

        token_address = pool_tokens[i]
        token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER,
                                        block=block)

        token_decimals = token_contract.functions.decimals().call()
        
        unwrapped_balances = []

        if call_contract_method(token_contract.functions.getRate(), block) is not None:
            unwrapped_balances = unwrap(pool_balances[i] / (10**token_decimals), token_address, block, blockchain, web3=web3, decimals=decimals)
        else:
            main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
            if main_token is None:
                stETH = call_contract_method(token_contract.functions.stETH(), block)
                if stETH is not None:
                    if lptoken_data['scalingFactors'] is not None and lptoken_data['scalingFactors'][i] != (10**18):
                        main_token = stETH
                    else:
                        main_token = token_address
                else:
                    main_token = token_address

            if lptoken_data['scalingFactors'] is not None:
                token_balance = pool_balances[i] * lptoken_data['scalingFactors'][i] / (10 ** (2 * 18 - token_decimals))
            else:
                token_balance = pool_balances[i]
        
            if decimals is True:
                token_balance = token_balance / (10**token_decimals)

            unwrapped_balances.append([main_token, token_balance])

        for main_token, token_balance in unwrapped_balances:
            token_balance = Decimal(token_balance)
            
            if aura_staked is None:
                token_staked = token_balance * pool_staked_fraction
            else:
                aura_pool_fraction = Decimal(aura_staked) / lptoken_data['totalSupply']
                token_staked = token_balance * aura_pool_fraction

            token_locked = token_balance * pool_locked_fraction
            token_balance = token_balance * pool_balance_fraction

            balances.append([main_token, token_balance, token_staked, token_locked])

    if reward is True:
        all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                        gauge_address=gauge_address)

        result.append(balances)
        result.append(all_rewards)

    else:
        result = balances

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True):

    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
    pool_tokens = pool_tokens_data[0]
    pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

    for i in range(len(pool_tokens)):

        if i == lptoken_data['bptIndex']:
            continue

        token_address = pool_tokens[i]
        token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER,
                                        block=block)

        token_decimals = token_contract.functions.decimals().call()

        unwrapped_balances = []
        if call_contract_method(token_contract.functions.getRate(), block) is not None:
            unwrapped_balances = unwrap(pool_balances[i] / Decimal(10**token_decimals), token_address, block, blockchain, web3=web3, decimals=decimals)
        else:
            main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
            if main_token is None:
                stETH = call_contract_method(token_contract.functions.stETH(), block)
                if stETH is not None:
                    if lptoken_data['scalingFactors'] is not None and lptoken_data['scalingFactors'][i] != (10**18):
                        main_token = stETH
                    else:
                        main_token = token_address
                else:
                    main_token = token_address

            if lptoken_data['scalingFactors'] is not None:
                token_balance = pool_balances[i] * lptoken_data['scalingFactors'][i] / Decimal(10 ** (2 * 18 - token_decimals))
            else:
                main_token = pool_tokens[i]
                token_balance = pool_balances[i]

            unwrapped_balances.append([main_token, to_token_amount(main_token, token_balance, blockchain, web3, decimals)])
        
        for main_token, token_balance in unwrapped_balances:
            balances.append([main_token, token_balance])
    
    first = itemgetter(0)
    balances = [[k, sum(item[1] for item in tups_to_sum)] for k, tups_to_sum in groupby(balances, key=first)]

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(lptoken_amount: Decimal, lptoken_address: str, block: int | str, blockchain: str, web3: Web3 = None, decimals:bool = True) -> Decimal:

    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data['poolId']).call(block_identifier=block)
    pool_tokens = pool_tokens_data[0]
    pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

    pool_balance_fraction = Decimal(lptoken_amount) * Decimal(10 ** lptoken_data['decimals']) / lptoken_data['totalSupply']

    for i in range(len(pool_tokens)):

        if i == lptoken_data['bptIndex']:
            continue

        token_address = pool_tokens[i]
        token_contract = get_contract(token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER,
                                        block=block)

        token_decimals = token_contract.functions.decimals().call()

        unwrapped_balances = []
        if call_contract_method(token_contract.functions.getRate(), block) is not None:
            unwrapped_balances = unwrap(pool_balances[i] / Decimal(10**token_decimals), token_address, block, blockchain, web3=web3, decimals=decimals)
        else:
            main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
            if main_token is None:
                stETH = call_contract_method(token_contract.functions.stETH(), block)
                if stETH is not None:
                    if lptoken_data['scalingFactors'] is not None and lptoken_data['scalingFactors'][i] != (10**18):
                        main_token = stETH
                    else:
                        main_token = token_address
                else:
                    main_token = token_address
        
            if lptoken_data['scalingFactors'] is not None:
                token_balance = pool_balances[i] * lptoken_data['scalingFactors'][i] / (10 ** (2 * 18 - token_decimals))
            else:
                token_balance = pool_balances[i]

            if decimals is True:
                token_balance = token_balance / (10**token_decimals)

            unwrapped_balances.append([main_token, token_balance])

        for unwrapped_balance in unwrapped_balances:
            main_token, token_balance = unwrapped_balance
            token_balance = token_balance * pool_balance_fraction

            balances.append([main_token, token_balance])
    
    first = itemgetter(0)
    balances = [[k, sum(item[1] for item in tups_to_sum)] for k, tups_to_sum in groupby(balances, key=first)]

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# swap_fees
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):

    result = {}
    hash_overlap = []

    if web3 is None:
        web3 = get_node(blockchain, block=block_start)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    pool_id = '0x' + lptoken_contract.functions.getPoolId().call().hex()
    result['swaps'] = []

    get_logs_bool = True
    block_from = block_start
    block_to = block_end

    swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()

    while get_logs_bool:
        swap_logs = get_logs(block_from, block_to, VAULT, swap_event, blockchain, topic1=pool_id)

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

                token_in = Web3.to_checksum_address('0x' + swap_log['topics'][2][-40:])
                lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
                swap_fee = Decimal(lptoken_contract.functions.getSwapFeePercentage().call(block_identifier=block_number))
                swap_fee /= Decimal(10 ** lptoken_decimals)
                swap_fee *= int(swap_log['data'][2:66], 16)

                swap_data = {
                    'block': block_number,
                    'tokenIn': token_in,
                    'amountIn': to_token_amount(token_in, swap_fee, blockchain, web3, decimals)
                }

                result['swaps'].append(swap_data)

        if log_count < 1000:
            get_logs_bool = False

        else:
            block_from = block_number

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_swap_fees_APR
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_swap_fees_APR(lptoken_address: str, blockchain: str, block_end: Union[int, str] = 'latest', web3=None,
                      days: int = 1, apy: bool = False) -> Decimal:
    block_start = date_to_block(datetime.strftime(
        datetime.strptime(block_to_date(block_end, blockchain), '%Y-%m-%d %H:%M:%S') - timedelta(days=days),
        '%Y-%m-%d %H:%M:%S'), blockchain)
    fees = swap_fees(lptoken_address, block_start, block_end, blockchain, web3)
    # create a dictionary to store the total amountIn for each tokenIn
    totals_dict = {}

    for swap in fees['swaps']:
        token_in = swap['tokenIn']
        amount_in = swap['amountIn']
        if token_in in totals_dict:
            totals_dict[token_in] += amount_in
        else:
            totals_dict[token_in] = amount_in

    totals_list = [(token_in, amount_in) for token_in, amount_in in totals_dict.items()]

    fee = 0
    for k in totals_list:
        fee += k[1] * Decimal(get_price(k[0], block_end, blockchain, web3)[0])
    pool_balance = pool_balances(lptoken_address, block_end, blockchain)
    tvl = 0
    for l in pool_balance:
        tvl += l[1] * Decimal(get_price(l[0], block_end, blockchain, web3)[0])

    rate = Decimal(fee / tvl)
    apr = (((1 + rate) ** Decimal(365 / days) - 1) * 100) / 2
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        return (1 + (apr / seconds_per_year)) ** seconds_per_year - 1
    else:
        return apr
