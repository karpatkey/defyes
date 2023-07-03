from datetime import datetime, timedelta
from decimal import Decimal
from itertools import groupby
from operator import itemgetter
from typing import Union

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.cache import const_call
from defyes.constants import (
    ARBITRUM,
    BAL_ARB,
    BAL_ETH,
    BAL_POL,
    BAL_XDAI,
    BB_A_USD_ETH,
    BB_A_USD_OLD_ETH,
    ETHEREUM,
    POLYGON,
    XDAI,
    ZERO_ADDRESS,
)
from defyes.functions import (
    balance_of,
    block_to_date,
    date_to_block,
    get_contract,
    get_decimals,
    get_logs_web3,
    get_node,
    last_block,
    to_token_amount,
)
from defyes.prices.prices import get_price

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# BALANCER VAULT
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Balancer Vault Contract Address
VAULT = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LIQUIDITY GAUGE FACTORY
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum Liquidity Gauge Factory Contract Address
LIQUIDITY_GAUGE_FACTORY_ETHEREUM = "0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC"  # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_ETHEREUM_V2 = "0xf1665E19bc105BE4EDD3739F88315cC699cc5b65"

# Polygon Liquidity Gauge Factory Contract Address
# LIQUIDITY_GAUGE_FACTORY_POLYGON = '0x3b8cA519122CdD8efb272b0D3085453404B25bD0' # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_POLYGON = "0x22625eEDd92c81a219A83e1dc48f88d54786B017"

# Arbitrum Liquidity Gauge Factory Contract Address
# LIQUIDITY_GAUGE_FACTORY_ARBITRUM = '0xb08E16cFc07C684dAA2f93C70323BAdb2A6CBFd2' # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_ARBITRUM = "0x6817149cb753BF529565B4D023d7507eD2ff4Bc0"

# GC Liquidity Gauge Factory Contract Address
# LIQUIDITY_GAUGE_FACTORY_XDAI = '0x809B79b53F18E9bc08A961ED4678B901aC93213a' # DEPRECATED
LIQUIDITY_GAUGE_FACTORY_XDAI = "0x83E443EF4f9963C77bd860f94500075556668cb8"

# Block number of gauge factory creation
BLOCKCHAIN_START_BLOCK = {
    "ethereumv1": 14457664,
    ETHEREUM: 15399251,
    POLYGON: 40687417,
    ARBITRUM: 72942741,
    XDAI: 27088528,
}

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# veBAL Contract Address
VEBAL = "0xC128a9954e6c874eA3d62ce62B468bA073093F25"

# veBAL Fee Distributor Contract
VEBAL_FEE_DISTRIBUTOR = "0xD3cf852898b21fc233251427c2DC93d3d604F3BB"
# VEBAL_FEE_DISTRIBUTOR = '0x26743984e3357eFC59f2fd6C1aFDC310335a61c9' #DEPRECATED

# veBAL Reward Tokens - BAL, bb-a-USD old deployment, bb-a-USD
VEBAL_REWARD_TOKENS = [BAL_ETH, BB_A_USD_OLD_ETH, BB_A_USD_ETH]

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHILD CHAIN GAUGE REWARD HELPER
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# GC Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_XDAI = "0xf7D5DcE55E6D47852F054697BAB6A1B48A00ddbd"

# Polygon Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_POLYGON = "0xaEb406b0E430BF5Ea2Dc0B9Fe62E4E53f74B3a33"

# Arbitrum Child Gauge Reward Helper
CHILD_CHAIN_GAUGE_REWARD_HELPER_ARBITRUM = "0xA0DAbEBAAd1b243BBb243f933013d560819eB66f"

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

# LP Token ABI - getPoolId, decimals, getActualSupply, getVirtualSupply, totalSupply, getBptIndex, balanceOf, getSwapFeePercentage, getRate, getScalingFactors, POOL_ID
ABI_LPTOKEN = '[{"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getActualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getVirtualSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getBptIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getSwapFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getScalingFactors","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"POOL_ID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"}]'

# Gauge ABI - claimable_tokens, claimable_reward, reward_count, reward_tokens, reward_contract
ABI_GAUGE = '[{"stateMutability":"nonpayable","type":"function","name":"claimable_tokens","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"claimable_reward","inputs":[{"name":"_user","type":"address"},{"name":"_reward_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}, {"stateMutability":"view","type":"function","name":"reward_tokens","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"reward_contract","inputs":[],"outputs":[{"name":"","type":"address"}]}]'

# ABI Pool Tokens - decimals, getRate, UNDERLYING_ASSET_ADDRESS, rate, stETH, UNDERLYING
ABI_POOL_TOKENS_BALANCER = '[{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"pure","type":"function"}, {"inputs":[],"name":"getRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"getMainToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"UNDERLYING_ASSET_ADDRESS","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"stETH","outputs":[{"internalType":"contract IStETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"UNDERLYING","outputs":[{"internalType":"contract IERC20Upgradeable","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# ABI Child Gauge Reward Helper - getPendingRewards
ABI_CHILD_CHAIN_GAUGE_REWARD_HELPER = '[{"inputs":[{"internalType":"contract IRewardsOnlyGauge","name":"gauge","type":"address"},{"internalType":"address","name":"user","type":"address"},{"internalType":"address","name":"token","type":"address"}],"name":"getPendingRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]'

# ABI Child Chain Streamer - reward_count
ABI_CHILD_CHAIN_STREAMER = '[{"stateMutability":"view","type":"function","name":"reward_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}]'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EVENT SIGNATURES
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Swap Event Signature
SWAP_EVENT_SIGNATURE = "Swap(bytes32,address,address,uint256,uint256)"

# Gauge Created Event Signature
GAUGE_CREATED_EVENT_SIGNATURE = "GaugeCreated(address)"


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# call_contract_method
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def call_contract_method(method, block):
    try:
        return method.call(block_identifier=block)
    except Exception as e:
        if (
            type(e) == ContractLogicError
            or type(e) == BadFunctionCallOutput
            or (type(e) == ValueError and (e.args[0]["code"] == -32000 or e.args[0]["code"] == -32015))
        ):
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
    if isinstance(block, str):
        if block == "latest":
            block = last_block(ETHEREUM)
        else:
            raise ValueError("Incorrect block.")

    gauge_factory_address = get_gauge_factory_address(blockchain)

    gauge_address = ZERO_ADDRESS
    if blockchain == ETHEREUM:
        gauge_factory_contract = get_contract(
            gauge_factory_address, blockchain, web3=web3, abi=ABI_LIQUIDITY_GAUGE_FACTORY, block=block
        )
        gauge_address = const_call(gauge_factory_contract.functions.getPoolGauge(lptoken_addr))
        if gauge_address == ZERO_ADDRESS:
            gauge_factory_address = LIQUIDITY_GAUGE_FACTORY_ETHEREUM_V2

    if gauge_factory_address != LIQUIDITY_GAUGE_FACTORY_ETHEREUM:
        block_from = BLOCKCHAIN_START_BLOCK[blockchain]
        gauge_created_event = web3.keccak(text=GAUGE_CREATED_EVENT_SIGNATURE).hex()

        if block >= block_from:
            logs = get_logs_web3(
                address=gauge_factory_address,
                blockchain=blockchain,
                block_start=block_from,
                block_end=block,
                topics=[gauge_created_event],
            )
            for log in logs:
                tx = web3.eth.get_transaction(log["transactionHash"])
                if lptoken_addr[2 : len(lptoken_addr)].lower() in tx["input"]:
                    gauge_address = Web3.to_checksum_address(f"0x{log['topics'][1].hex()[-40:]}")
                    break

        return gauge_address

    return gauge_address


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_data = {}

    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block)

    try:
        lptoken_data["poolId"] = const_call(lptoken_data["contract"].functions.getPoolId())
    except ContractLogicError:
        try:
            lptoken_data["poolId"] = const_call(lptoken_data["contract"].functions.POOL_ID())
        except ContractLogicError:
            lptoken_data["poolId"] = None

    lptoken_data["decimals"] = const_call(lptoken_data["contract"].functions.decimals())

    try:
        lptoken_data["totalSupply"] = lptoken_data["contract"].functions.getActualSupply().call(block_identifier=block)
        lptoken_data["isBoosted"] = True
    except:
        try:
            lptoken_data["totalSupply"] = (
                lptoken_data["contract"].functions.getVirtualSupply().call(block_identifier=block)
            )
            lptoken_data["isBoosted"] = True
        except:
            lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)
            lptoken_data["isBoosted"] = False

    if lptoken_data["isBoosted"]:
        try:
            lptoken_data["bptIndex"] = const_call(lptoken_data["contract"].functions.getBptIndex())
        except:
            lptoken_data["isBoosted"] = False
            lptoken_data["bptIndex"] = None
    else:
        lptoken_data["bptIndex"] = None

    try:
        lptoken_data["scalingFactors"] = (
            lptoken_data["contract"].functions.getScalingFactors().call(block_identifier=block)
        )
    except:
        lptoken_data["scalingFactors"] = None

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

    # if blockchain == ETHEREUM:
    reward_count = gauge_contract.functions.reward_count().call(block_identifier=block)
    # else:
    # child_chain_streamer_contract = get_contract(gauge_contract.functions.reward_contract().call(), blockchain,
    #                                              web3=web3, abi=ABI_CHILD_CHAIN_STREAMER, block=block)
    # reward_count = child_chain_streamer_contract.functions.reward_count().call(block_identifier=block)

    for i in range(reward_count):
        token_address = const_call(gauge_contract.functions.reward_tokens(i))

        if blockchain == ETHEREUM:
            token_rewards = gauge_contract.functions.claimable_reward(wallet, token_address).call(
                block_identifier=block
            )
        else:
            child_chain_reward_helper_contract = get_contract(
                get_child_chain_reward_helper_address(blockchain),
                blockchain,
                web3=web3,
                abi=ABI_CHILD_CHAIN_GAUGE_REWARD_HELPER,
                block=block,
            )
            token_rewards = child_chain_reward_helper_contract.functions.getPendingRewards(
                gauge_contract.address, wallet, token_address
            ).call(block_identifier=block)

        rewards.append([token_address, to_token_amount(token_address, token_rewards, blockchain, web3, decimals)])

    return rewards


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_vebal_rewards
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_vebal_rewards(web3, wallet, block, blockchain, decimals=True):
    vebal_rewards = []

    fee_distributor_contract = get_contract(
        VEBAL_FEE_DISTRIBUTOR, blockchain, web3=web3, abi=ABI_VEBAL_FEE_DISTRIBUTOR, block=block
    )
    claim_tokens = fee_distributor_contract.functions.claimTokens(wallet, VEBAL_REWARD_TOKENS).call(
        block_identifier=block
    )

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

        if lptoken_address == const_call(vebal_contract.functions.token()):
            vebal_rewards = get_vebal_rewards(web3, wallet, block, blockchain, decimals=decimals)

            if len(vebal_rewards) > 0:
                for vebal_reward in vebal_rewards:
                    all_rewards.append(vebal_reward)

    if gauge_address != ZERO_ADDRESS:
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)

        # if blockchain == ETHEREUM:
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

    gauge_address = get_gauge_address(blockchain, block, web3, lptoken_address)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)
    lptoken_data["balanceOf"] = Decimal(
        lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block)
    )

    if gauge_address != ZERO_ADDRESS:
        lptoken_data["staked"] = balance_of(wallet, gauge_address, block, blockchain, web3=web3, decimals=False)
    else:
        lptoken_data["staked"] = Decimal(0)

    lptoken_data["locked"] = Decimal(0)
    if blockchain == ETHEREUM:
        vebal_contract = get_contract(VEBAL, blockchain, web3=web3, abi=ABI_VEBAL, block=block)

        if lptoken_address == const_call(vebal_contract.functions.token()):
            try:
                lptoken_data["locked"] = Decimal(
                    vebal_contract.functions.locked(wallet).call(block_identifier=block)[0]
                )
            except:
                pass

    if lptoken_data["poolId"] is not None:
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data["poolId"]).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

        pool_balance_fraction = lptoken_data["balanceOf"] / lptoken_data["totalSupply"]
        pool_staked_fraction = lptoken_data["staked"] / lptoken_data["totalSupply"]
        pool_locked_fraction = lptoken_data["locked"] / lptoken_data["totalSupply"]
        for i in range(len(pool_tokens)):
            if i == lptoken_data["bptIndex"]:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(
                token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block
            )

            token_decimals = const_call(token_contract.functions.decimals())

            unwrapped_balances = []

            if call_contract_method(token_contract.functions.getRate(), block) is not None:
                unwrapped_balances = unwrap(
                    pool_balances[i] / (10**token_decimals),
                    token_address,
                    block,
                    blockchain,
                    web3=web3,
                    decimals=decimals,
                )
            else:
                is_wsteth = False
                main_token = call_contract_method(token_contract.functions.UNDERLYING(), block)
                if main_token is None:
                    main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
                    if main_token is None:
                        main_token = token_address
                        stETH = call_contract_method(token_contract.functions.stETH(), block)
                        if stETH is not None:
                            is_wsteth = True
                        # The previous 4 lines can be replaced by the commented code below to have stETH being returned instead of stETH
                        # stETH = call_contract_method(token_contract.functions.stETH(), block)
                        # if stETH is not None:
                        #    if lptoken_data["scalingFactors"] is not None and lptoken_data["scalingFactors"][i] != (
                        #        10**18
                        #    ):
                        #        main_token = stETH
                        #    else:
                        #        main_token = token_address
                        # else:
                        #    main_token = token_address

                # if lptoken_data["scalingFactors"] is not None:
                if lptoken_data["scalingFactors"] is not None and not is_wsteth:
                    token_balance = (
                        pool_balances[i] * lptoken_data["scalingFactors"][i] / (10 ** (2 * 18 - token_decimals))
                    )
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
                    aura_pool_fraction = Decimal(aura_staked) / lptoken_data["totalSupply"]
                    token_staked = token_balance * aura_pool_fraction

                token_locked = token_balance * pool_locked_fraction
                token_balance = token_balance * pool_balance_fraction

                balances.append([main_token, token_balance, token_staked, token_locked])

        if reward is True:
            all_rewards = get_all_rewards(
                wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals, gauge_address=gauge_address
            )

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

    if lptoken_data["poolId"] is not None:
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data["poolId"]).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

        for i in range(len(pool_tokens)):
            if i == lptoken_data["bptIndex"]:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(
                token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block
            )

            token_decimals = const_call(token_contract.functions.decimals())

            unwrapped_balances = []
            if call_contract_method(token_contract.functions.getRate(), block) is not None:
                unwrapped_balances = unwrap(
                    pool_balances[i] / Decimal(10**token_decimals),
                    token_address,
                    block,
                    blockchain,
                    web3=web3,
                    decimals=decimals,
                )
            else:
                is_wsteth = False
                main_token = call_contract_method(token_contract.functions.UNDERLYING(), block)
                if main_token is None:
                    main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
                    if main_token is None:
                        main_token = token_address
                        stETH = call_contract_method(token_contract.functions.stETH(), block)
                        if stETH is not None:
                            is_wsteth = True
                        # The previous 4 lines can be replaced by the commented code below to have stETH being returned instead of stETH
                        # stETH = call_contract_method(token_contract.functions.stETH(), block)
                        # if stETH is not None:
                        #    if lptoken_data["scalingFactors"] is not None and lptoken_data["scalingFactors"][i] != (
                        #        10**18
                        #    ):
                        #        main_token = stETH
                        #    else:
                        #        main_token = token_address
                        # else:
                        #    main_token = token_address

                # if lptoken_data["scalingFactors"] is not None:
                if lptoken_data["scalingFactors"] is not None and not is_wsteth:
                    token_balance = (
                        pool_balances[i] * lptoken_data["scalingFactors"][i] / Decimal(10 ** (2 * 18 - token_decimals))
                    )
                else:
                    main_token = pool_tokens[i]
                    token_balance = pool_balances[i]

                unwrapped_balances.append(
                    [main_token, to_token_amount(main_token, token_balance, blockchain, web3, decimals)]
                )

            for main_token, token_balance in unwrapped_balances:
                balances.append([main_token, token_balance])

        first = itemgetter(0)
        balances = [[k, sum(item[1] for item in tups_to_sum)] for k, tups_to_sum in groupby(balances, key=first)]

    return balances


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(
    lptoken_amount: Decimal,
    lptoken_address: str,
    block: int | str,
    blockchain: str,
    web3: Web3 = None,
    decimals: bool = True,
) -> Decimal:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    vault_contract = get_contract(VAULT, blockchain, web3=web3, abi=ABI_VAULT, block=block)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    if lptoken_data["poolId"] is not None:
        pool_tokens_data = vault_contract.functions.getPoolTokens(lptoken_data["poolId"]).call(block_identifier=block)
        pool_tokens = pool_tokens_data[0]
        pool_balances = [Decimal(balance) for balance in pool_tokens_data[1]]

        pool_balance_fraction = (
            Decimal(lptoken_amount) * Decimal(10 ** lptoken_data["decimals"]) / lptoken_data["totalSupply"]
        )

        for i in range(len(pool_tokens)):
            if i == lptoken_data["bptIndex"]:
                continue

            token_address = pool_tokens[i]
            token_contract = get_contract(
                token_address, blockchain, web3=web3, abi=ABI_POOL_TOKENS_BALANCER, block=block
            )

            token_decimals = const_call(token_contract.functions.decimals())

            unwrapped_balances = []
            if call_contract_method(token_contract.functions.getRate(), block) is not None:
                unwrapped_balances = unwrap(
                    pool_balances[i] / Decimal(10**token_decimals),
                    token_address,
                    block,
                    blockchain,
                    web3=web3,
                    decimals=decimals,
                )
            else:
                is_wsteth = False
                main_token = call_contract_method(token_contract.functions.UNDERLYING(), block)
                if main_token is None:
                    main_token = call_contract_method(token_contract.functions.UNDERLYING_ASSET_ADDRESS(), block)
                    if main_token is None:
                        main_token = token_address
                        stETH = call_contract_method(token_contract.functions.stETH(), block)
                        if stETH is not None:
                            is_wsteth = True
                        # The previous 4 lines can be replaced by the commented code below to have stETH being returned instead of stETH
                        # stETH = call_contract_method(token_contract.functions.stETH(), block)
                        # if stETH is not None:
                        #    if lptoken_data["scalingFactors"] is not None and lptoken_data["scalingFactors"][i] != (
                        #        10**18
                        #    ):
                        #        main_token = stETH
                        #    else:
                        #        main_token = token_address
                        # else:
                        #    main_token = token_address

                # if lptoken_data["scalingFactors"] is not None:
                if lptoken_data["scalingFactors"] is not None and not is_wsteth:
                    token_balance = (
                        pool_balances[i] * lptoken_data["scalingFactors"][i] / (10 ** (2 * 18 - token_decimals))
                    )
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

    if web3 is None:
        web3 = get_node(blockchain, block=block_end)

    lptoken_address = Web3.to_checksum_address(lptoken_address)
    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)
    try:
        pool_id = const_call(lptoken_contract.functions.getPoolId())
    except ContractLogicError:
        try:
            pool_id = const_call(lptoken_contract.functions.POOL_ID())
        except ContractLogicError:
            pool_id = None

    if pool_id is not None:
        pool_id = "0x" + pool_id.hex()
        result["swaps"] = []
        swap_event = web3.keccak(text=SWAP_EVENT_SIGNATURE).hex()
        swap_logs = get_logs_web3(
            address=VAULT,
            blockchain=blockchain,
            block_start=block_start,
            block_end=block_end,
            topics=[swap_event, pool_id],
        )

        for swap_log in swap_logs:
            token_in = Web3.to_checksum_address(f"0x{swap_log['topics'][2].hex()[-40:]}")
            lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
            swap_fee = Decimal(
                lptoken_contract.functions.getSwapFeePercentage().call(block_identifier=swap_log["blockNumber"])
            )
            swap_fee /= Decimal(10**lptoken_decimals)
            swap_fee *= int(swap_log["data"].hex()[2:66], 16)

            swap_data = {
                "block": swap_log["blockNumber"],
                "tokenIn": token_in,
                "amountIn": to_token_amount(token_in, swap_fee, blockchain, web3, decimals),
            }

            result["swaps"].append(swap_data)

    return result


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_swap_fees_APR
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_swap_fees_APR(
    lptoken_address: str,
    blockchain: str,
    block_end: Union[int, str] = "latest",
    web3=None,
    days: int = 1,
    apy: bool = False,
) -> Decimal:
    block_start = date_to_block(
        datetime.strftime(
            datetime.strptime(block_to_date(block_end, blockchain), "%Y-%m-%d %H:%M:%S") - timedelta(days=days),
            "%Y-%m-%d %H:%M:%S",
        ),
        blockchain,
    )

    if block_start < BLOCKCHAIN_START_BLOCK[blockchain]:
        block_start = BLOCKCHAIN_START_BLOCK[blockchain]

    fees = swap_fees(lptoken_address, block_start, block_end, blockchain, web3)
    # create a dictionary to store the total amountIn for each tokenIn
    totals_dict = {}

    for swap in fees["swaps"]:
        token_in = swap["tokenIn"]
        amount_in = swap["amountIn"]
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
    for balance in pool_balance:
        tvl += balance[1] * Decimal(get_price(balance[0], block_end, blockchain, web3)[0])

    rate = Decimal(fee / tvl)
    apr = (((1 + rate) ** Decimal(365 / days) - 1) * 100) / 2
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        return (1 + (apr / seconds_per_year)) ** seconds_per_year - 1
    else:
        return apr
