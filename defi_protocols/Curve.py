from typing import Union
from datetime import datetime, timedelta

from defi_protocols.functions import get_node, get_contract, get_decimals, balance_of, get_logs, date_to_block, block_to_date, get_contract_abi, GetNodeIndexError
from defi_protocols.constants import ETHEREUM, MAX_EXECUTIONS, ZERO_ADDRESS, X3CRV_ETH, CRV_ETH, XDAI, CRV_XDAI, E_ADDRESS, X3CRV_XDAI

from web3.exceptions import ContractLogicError
from defi_protocols.prices.prices import get_price

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# PROVIDER ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PROVIDER_ADDRESS = '0x0000000022D53366457F9d5E68Ec105046FC4383'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# X-CHAIN GAUGE FACTORY ADDRESS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
X_CHAIN_GAUGE_FACTORY_ADDRESS = '0xabC000d88f23Bb45525E447528DBF656A9D55bf5'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Provider ABI - get_address
ABI_PROVIDER = '[{"name":"get_address","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":"_id"}],"stateMutability":"view","type":"function","gas":1308}]'

# X-Chain Gauge Factory ABI - get_gauge_from_lp_token
ABI_X_CHAIN_GAUGE_FACTORY_ADDRESS = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":""}],"name":"get_gauge_from_lp_token","inputs":[{"type":"address","name":"arg0"}]}]'

# Registry for Regular Pools ABI - get_gauges, get_pool_from_lp_token, pool_list, pool_count, get_lp_token, get_n_coins, is_meta, get_coins, get_underlying_coins
ABI_REGISTRY_REGULAR_POOLS = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address[10]","name":""},{"type":"int128[10]","name":""}],"name":"get_gauges","inputs":[{"type":"address","name":"_pool"}],"gas":28534}, {"stateMutability":"view","type":"function","name":"get_pool_from_lp_token","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":2443}, {"stateMutability":"view","type":"function","name":"pool_list","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":2217}, {"stateMutability":"view","type":"function","name":"pool_count","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":2138}, {"stateMutability":"view","type":"function","name":"get_lp_token","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":2473}, {"stateMutability":"view","type":"function","name":"get_n_coins","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"uint256[2]"}],"gas":1521}, {"stateMutability":"view","type":"function","name":"is_meta","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"bool"}],"gas":1900}, {"stateMutability":"view","type":"function","name":"get_coins","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address[8]"}],"gas":12102}, {"stateMutability":"view","type":"function","name":"get_underlying_coins","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address[8]"}],"gas":12194}]'

# Registry for Factory Pools ABI - get_gauge, pool_list, pool_count, get_base_pool, get_meta_n_coins, is_meta, base_pool_list, base_pool_count
ABI_REGISTRY_FACTORY_POOLS = '[{"stateMutability":"view","type":"function","name":"get_gauge","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":3089}, {"stateMutability":"view","type":"function","name":"pool_list","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3573}, {"stateMutability":"view","type":"function","name":"pool_count","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":3558}, {"stateMutability":"view","type":"function","name":"get_base_pool","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":2663}, {"stateMutability":"view","type":"function","name":"get_meta_n_coins","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"gas":5201}, {"stateMutability":"view","type":"function","name":"is_meta","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"bool"}],"gas":3152}, {"stateMutability":"view","type":"function","name":"base_pool_list","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3633}, {"stateMutability":"view","type":"function","name":"base_pool_count","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":3618}]'

# Registry for Crypto V2 Pools ABI - get_gauges, get_pool_from_lp_token, pool_list, pool_count, get_lp_token, get_zap, get_n_coins
ABI_REGISTRY_CRYPTO_V2_POOLS = '[{"stateMutability":"view","type":"function","name":"get_gauges","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address[10]"},{"name":"","type":"int128[10]"}],"gas":26055}, {"stateMutability":"view","type":"function","name":"get_pool_from_lp_token","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":3548}, {"stateMutability":"view","type":"function","name":"pool_list","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3201}, {"stateMutability":"view","type":"function","name":"pool_count","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":3186}, {"stateMutability":"view","type":"function","name":"get_lp_token","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":3578}, {"stateMutability":"view","type":"function","name":"get_zap","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":3608}, {"stateMutability":"view","type":"function","name":"get_n_coins","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":2834}]'

# Registry for Crypto Factory Pools ABI - get_gauge, pool_list, pool_count
ABI_REGISTRY_CRYPTO_FACTORY_POOLS = '[{"stateMutability":"view","type":"function","name":"get_gauge","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address"}],"gas":3089}, {"stateMutability":"view","type":"function","name":"pool_list","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3573}, {"stateMutability":"view","type":"function","name":"pool_count","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":3558}]'

# LP Token ABI - decimals, totalSupply, minter, balanceOf
ABI_LPTOKEN = '[{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"decimals","inputs":[],"gas":288}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"totalSupply","inputs":[],"gas":2808}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":""}],"name":"minter","inputs":[],"gas":2838}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"balanceOf","inputs":[{"type":"address","name":"arg0"}],"gas":2963}]'

# Pool ABI - coins, balances, fee, underlying_coins, token
ABI_POOL = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":""}],"name":"coins","inputs":[{"type":"uint256","name":"arg0"}],"gas":1917}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"balances","inputs":[{"type":"uint256","name":"arg0"}],"gas":1947}, {"name":"fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2051}, {"name":"underlying_coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2160}, {"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]}]'

# Alternative Pool ABI - coins, balances, fee, underlying_coins
ABI_POOL_ALTERNATIVE = '[{"name":"coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2130}, {"name":"balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2190}, {"name":"fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2051}, {"name":"underlying_coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2160}]'

# Gauge ABI - crv_token, claimable_tokens, rewarded_token, claimable_reward, claimed_rewards_for, reward_tokens, claimable_reward, claimable_reward_write, decimals, version, minter
ABI_GAUGE = '[{"name":"crv_token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1451}, {"name":"claimable_tokens","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"nonpayable","type":"function","gas":1989612}, {"name":"rewarded_token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2201}, {"name":"claimable_reward","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"view","type":"function","gas":7300}, {"name":"claimed_rewards_for","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":2475}, {"name":"reward_tokens","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2550}, {"name":"claimable_reward","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"_addr"},{"type":"address","name":"_token"}],"stateMutability":"nonpayable","type":"function","gas":1017930}, {"stateMutability":"nonpayable","type":"function","name":"claimable_reward_write","inputs":[{"name":"_addr","type":"address"},{"name":"_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":1211002}, {"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":288}, {"stateMutability":"view","type":"function","name":"version","inputs":[],"outputs":[{"name":"","type":"string"}]}, {"name":"minter","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1421}]'

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# EVENT SIGNATURES
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# TokenExchange Event Signatures
TOKEN_EXCHANGE_EVENT_SIGNATURES = ['TokenExchange(address,int128,uint256,int128,uint256)',
                                   'TokenExchange(address,uint256,uint256,uint256,uint256)']

# TokenExchangeUnderlying Event Signatures
TOKEN_EXCHANGE_UNDERLYING_EVENT_SIGNATURES = ['TokenExchangeUnderlying(address,int128,uint256,int128,uint256)',
                                              'TokenExchangeUnderlying(address,uint256,uint256,uint256,uint256)']


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_registry_contract
# id = 0 -> Registry for Regular Pools
# id = 3 -> Registry for Factory Pools
# id = 5 -> Registry for Crypto V2 Pools
# id = 6 -> Registry for Crypto Factory Pools
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_registry_contract(web3, id, block, blockchain):
    """

    :param web3:
    :param id:
    :param block:
    :param blockchain:
    :return:
    """
    provider_contract = get_contract(PROVIDER_ADDRESS, blockchain, web3=web3, abi=ABI_PROVIDER, block=block)

    registry_address = provider_contract.functions.get_address(id).call()

    if id == 0:
        abi = ABI_REGISTRY_REGULAR_POOLS
    elif id == 3:
        abi = ABI_REGISTRY_FACTORY_POOLS
    elif id == 5:
        abi = ABI_REGISTRY_CRYPTO_V2_POOLS
    elif id == 6:
        abi = ABI_REGISTRY_CRYPTO_FACTORY_POOLS
    else:
        abi = ABI_REGISTRY_REGULAR_POOLS

    return get_contract(registry_address, blockchain, web3=web3, abi=abi, block=block)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_gauge_address
# Output: gauge_address
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_gauge_address(web3, pool_address, lptoken_address, block, blockchain):
    """

    :param web3:
    :param pool_address:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :return:
    """
    gauge_address = None

    # 1: Try to retrieve the gauge address assuming the pool is a Regular Pool
    registry_contract = get_registry_contract(web3, 0, block, blockchain)

    if registry_contract.address != ZERO_ADDRESS:
        gauge_address = registry_contract.functions.get_gauges(pool_address).call()[0][0]

    # 2: Try to retrieve the gauge address assuming the pool is a Factory Pool
    if gauge_address == ZERO_ADDRESS:
        registry_contract = get_registry_contract(web3, 3, block, blockchain)

        if registry_contract.address != ZERO_ADDRESS:
            gauge_address = registry_contract.functions.get_gauge(pool_address).call()

    # 3: Try to retrieve the gauge address assuming the pool is a Crypto V2 Pool
    if gauge_address == ZERO_ADDRESS:
        registry_contract = get_registry_contract(web3, 5, block, blockchain)

        if registry_contract.address != ZERO_ADDRESS:
            gauge_address = registry_contract.functions.get_gauges(pool_address).call()[0][0]

    # 4: Try to retrieve the gauge address assuming the pool is a Crypto Factory Pool
    if gauge_address == ZERO_ADDRESS:
        registry_contract = get_registry_contract(web3, 6, block, blockchain)

        if registry_contract.address != ZERO_ADDRESS:
            gauge_address = registry_contract.functions.get_gauge(pool_address).call()

    # Pools which don't have their gauge registered in none of the registries
    if gauge_address == ZERO_ADDRESS and blockchain != ETHEREUM:
        x_chain_factory_contract = get_contract(X_CHAIN_GAUGE_FACTORY_ADDRESS, blockchain, web3=web3,
                                                abi=ABI_X_CHAIN_GAUGE_FACTORY_ADDRESS, block=block)
        gauge_address = x_chain_factory_contract.functions.get_gauge_from_lp_token(lptoken_address).call()

    return gauge_address


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_gauge_version
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'only_version' = True -> return just the gauge_version / 'only_version' = False -> return [gauge_contract, gauge_version]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_gauge_version(gauge_address, block, blockchain, web3=None, execution=1, index=0, only_version=True):
    """

    :param gauge_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param only_version:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        # The ABI used to get the Gauge Contract is a general ABI for all types. This is because some gauges do not have
        # their ABIs available in the explorers
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)

        try:
            gauge_contract.functions.version().call()

            if blockchain != ETHEREUM:
                if only_version is True:
                    return 'ChildGauge'
                else:
                    return ['ChildGauge', gauge_contract]

            if only_version is True:
                return 'LiquidityGaugeV5'
            else:
                return ['LiquidityGaugeV5', gauge_contract]
        except:
            pass

        try:
            gauge_contract.functions.claimable_reward_write(ZERO_ADDRESS, ZERO_ADDRESS).call()

            try:
                gauge_contract.functions.crv_token().call()

                if only_version is True:
                    return 'LiquidityGaugeV3'
                else:
                    return ['LiquidityGaugeV3', gauge_contract]

            except:
                if only_version is True:
                    return 'RewardsOnlyGauge'
                else:
                    return ['RewardsOnlyGauge', gauge_contract]

        except:
            pass

        try:
            gauge_contract.functions.minter().call()

            try:
                gauge_contract.functions.decimals().call()

                if only_version is True:
                    return 'LiquidityGaugeV2'
                else:
                    return ['LiquidityGaugeV2', gauge_contract]

            except:
                try:
                    gauge_contract.functions.claimable_reward(ZERO_ADDRESS).call()
                    if only_version is True:
                        return 'LiquidityGaugeReward'
                    else:
                        return ['LiquidityGaugeReward', gauge_contract]

                except:
                    if only_version is True:
                        return 'LiquidityGauge'
                    else:
                        return ['LiquidityGauge', gauge_contract]

        except:
            if only_version is True:
                return 'LiquidityGaugeV4'
            else:
                return ['LiquidityGaugeV4', gauge_contract]

    except GetNodeIndexError:
        return get_gauge_version(gauge_address, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_gauge_version(gauge_address, block, blockchain, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_address
# IMPORTANT: "crypto factory" pools are not considered because the pool address is retrieved by the function get_lptoken_data (minter function)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_address(web3, lptoken_address, block, blockchain):
    """

    :param web3:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :return:
    """
    # 1: Try to retrieve the pool address assuming the pool is a Regular Pool
    registry_contract = get_registry_contract(web3, 0, block, blockchain)

    if registry_contract.address != ZERO_ADDRESS:
        pool_address = registry_contract.functions.get_pool_from_lp_token(lptoken_address).call()

    # 2: Try to retrieve the pool address assuming the pool is a Crypto V2 Pool
    if pool_address == ZERO_ADDRESS:
        registry_contract = get_registry_contract(web3, 5, block, blockchain)

        if registry_contract.address != ZERO_ADDRESS:
            pool_address = registry_contract.functions.get_pool_from_lp_token(lptoken_address).call()

    # 3: If the pool is not a Regular Pool or a V2 Pool then it's a Factory Pool
    if pool_address == ZERO_ADDRESS:
        pool_address = lptoken_address

    return pool_address


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_pool_data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_pool_data(web3, minter, block, blockchain):
    """

    :param web3:
    :param minter:
    :param block:
    :param blockchain:
    :return:
    """
    pool_data = {
        'contract': None,
        'is_metapool': False,
        'coins': {}
    }

    pool_data['contract'] = get_contract(minter, blockchain, web3=web3, block=block, abi=ABI_POOL)

    try:
        pool_data['contract'].functions.underlying_coins(0).call()
        pool_data['is_metapool'] = True
    except:
        pass

    next_token = True
    i = 0
    j = 0
    while (next_token is True):

        try:
            token_address = pool_data['contract'].functions.coins(i).call(block_identifier=block)

        except ContractLogicError:

            # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALETRNATIVE
            if i == 0:
                pool_data['contract'] = get_contract(minter, blockchain, web3=web3, block=block,
                                                     abi=ABI_POOL_ALTERNATIVE)
            else:
                next_token = False

            continue

        except ValueError:
            next_token = False
            continue

        # IMPORTANT: AD-HOC FIX UNTIL WE FIND A WAY TO SOLVE HOW META POOLS WORK FOR DIFFERENT POOL TYPES AND SIDE-CHAINS
        # if token_address == X3CRV_ETH or token_address == X3CRV_POL or token_address == X3CRV_XDAI:
        if token_address == X3CRV_ETH:
            pool_data['is_metapool'] = True

            x3crv_minter = get_pool_address(web3, token_address, block, blockchain)
            x3crv_pool_contract = get_contract(x3crv_minter, blockchain, web3=web3, block=block, abi=ABI_POOL)

            x3crv_next_token = True
            while (x3crv_next_token is True):

                try:
                    token_address = x3crv_pool_contract.functions.coins(j).call(block_identifier=block)

                except ContractLogicError:

                    # If the query fails when j == 0 -> the pool contract must be retrieved with the ABI_POOL_ALETRNATIVE
                    if i == 0:
                        x3crv_pool_contract = get_contract(x3crv_minter, blockchain, web3=web3, block=block,
                                                           abi=ABI_POOL_ALTERNATIVE)
                    else:
                        x3crv_next_token = False

                    continue

                except ValueError:
                    x3crv_next_token = False
                    continue

                pool_data['coins'][i + j] = token_address
                j += 1

        else:
            pool_data['coins'][i + j] = token_address

        i += 1

    return pool_data


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_lptoken_data
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

        try:
            lptoken_data['minter'] = lptoken_data['contract'].functions.minter().call()
        except:
            lptoken_data['minter'] = None

        lptoken_data['decimals'] = lptoken_data['contract'].functions.decimals().call()
        lptoken_data['totalSupply'] = lptoken_data['contract'].functions.totalSupply().call(block_identifier=block)

        return lptoken_data

    except GetNodeIndexError:
        return get_lptoken_data(lptoken_address, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_lptoken_data(lptoken_address, block, blockchain, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_all_rewards
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'gauge_address' = gauge_address -> Improves performance
# Output:
# 1 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True,
                    gauge_address=None):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param gauge_address:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    all_rewards = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        if gauge_address is None:
            minter = get_pool_address(web3, lptoken_address, block, blockchain)

            gauge_address = get_pool_gauge_address(web3, minter, lptoken_address, block, blockchain)

        if gauge_address is None:
            return []

        gauge_data = get_gauge_version(gauge_address, block, blockchain, only_version=False)

        gauge_version = gauge_data[0]
        gauge_contract = gauge_data[1]

        if gauge_version == 'LiquidityGaugeV5' or gauge_version == 'LiquidityGaugeV4' or gauge_version == 'LiquidityGaugeV2' or gauge_version == 'ChildGauge':

            next_token = True
            i = 0
            while (next_token is True):

                token_address = gauge_contract.functions.reward_tokens(i).call()

                if token_address != ZERO_ADDRESS:

                    if decimals is True:
                        token_decimals = get_decimals(token_address, blockchain, web3=web3)
                    else:
                        token_decimals = 0

                    token_reward = gauge_contract.functions.claimable_reward(wallet, token_address).call(
                        block_identifier=block) / (10 ** token_decimals)

                    all_rewards.append([token_address, token_reward])

                    i += 1

                else:
                    next_token = False
                    break

            # CRV rewards
            if blockchain == ETHEREUM:
                token_address = CRV_ETH
            elif blockchain == XDAI:
                token_address = CRV_XDAI

            if decimals is True:
                token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_decimals = 0

            token_reward = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block) / (
                        10 ** token_decimals)

            all_rewards.append([token_address, token_reward])

        elif gauge_version == 'LiquidityGaugeV3' or gauge_version == 'RewardsOnlyGauge':

            next_token = True
            i = 0
            while (next_token is True):
                token_address = gauge_contract.functions.reward_tokens(i).call()

                if token_address != ZERO_ADDRESS:

                    if decimals is True:
                        token_decimals = get_decimals(token_address, blockchain, web3=web3)
                    else:
                        token_decimals = 0

                    token_reward = gauge_contract.functions.claimable_reward_write(wallet, token_address).call(
                        block_identifier=block) / (10 ** token_decimals)

                    all_rewards.append([token_address, token_reward])

                    i += 1

                else:
                    next_token = False
                    break

            if gauge_version == 'LiquidityGaugeV3':
                # CRV rewards
                if blockchain == ETHEREUM:
                    token_address = CRV_ETH
                elif blockchain == XDAI:
                    token_address = CRV_XDAI

                if decimals is True:
                    token_decimals = get_decimals(token_address, blockchain, web3=web3)
                else:
                    token_decimals = 0

                token_reward = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block) / (
                            10 ** token_decimals)

                all_rewards.append([token_address, token_reward])

        elif gauge_version == 'LiquidityGaugeReward' or gauge_version == 'LiquidityGauge':

            token_address = gauge_contract.functions.crv_token().call()

            if decimals is True:
                token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_decimals = 0

            token_reward = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block) / (
                        10 ** token_decimals)

            all_rewards.append([token_address, token_reward])

            if gauge_version == 'LiquidityGaugeReward':
                # Additional rewards
                token_address = gauge_contract.functions.rewarded_token().call()

                if decimals is True:
                    token_decimals = get_decimals(token_address, blockchain, web3=web3)
                else:
                    token_decimals = 0

                token_reward = (gauge_contract.function.claimable_reward(wallet).call(
                    block_identifier=block) - gauge_contract.claimed_rewards_for(wallet).call(
                    block_identifier=block)) / (10 ** token_decimals)

                all_rewards.append([token_address, token_reward])

        return all_rewards

    except GetNodeIndexError:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, gauge_address=gauge_address,
                               decimals=decimals, index=0, execution=execution + 1)

    except:
        return get_all_rewards(wallet, lptoken_address, block, blockchain, gauge_address=gauge_address,
                               decimals=decimals, index=index + 1, execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# underlying
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'reward' = True -> retrieves the rewards / 'reward' = False or not passed onto the function -> no reward retrieval
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'convex_staked' = Staked LP Token Balance in Convex
# 'gauge_address' = gauge_address
# Output: a list with 2 elements:
# 1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
# 2 - List of Tuples: [reward_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def underlying(wallet, lptoken_address, block, blockchain, web3=None, execution=1, index=0, reward=False, decimals=True,
               convex_staked=None, gauge_address=None):
    """

    :param wallet:
    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param reward:
    :param decimals:
    :param convex_staked:
    :param gauge_address:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    result = []
    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3, index=index)

        lptoken_data['balanceOf'] = lptoken_data['contract'].functions.balanceOf(wallet).call(block_identifier=block)

        if lptoken_data['minter'] is None:
            lptoken_data['minter'] = get_pool_address(web3, lptoken_address, block, blockchain)

        if gauge_address is not None:
            lptoken_data['gauge'] = gauge_address
        else:
            lptoken_data['gauge'] = get_pool_gauge_address(web3, lptoken_data['minter'], lptoken_address, block,
                                                           blockchain)

        if lptoken_data['gauge'] is not None:
            lptoken_data['staked'] = balance_of(wallet, lptoken_data['gauge'], block, blockchain, web3=web3,
                                                decimals=False)
        else:
            lptoken_data['staked'] = 0

        pool_contract = get_contract(lptoken_data['minter'], blockchain, web3=web3, block=block, abi=ABI_POOL)

        pool_balance_fraction = lptoken_data['balanceOf'] / lptoken_data['totalSupply']
        pool_staked_fraction = lptoken_data['staked'] / lptoken_data['totalSupply']

        next_token = True
        i = 0
        while (next_token is True):

            try:
                token_address = pool_contract.functions.coins(i).call(block_identifier=block)

            except ContractLogicError:

                # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALETRNATIVE
                if i == 0:
                    pool_contract = get_contract(lptoken_data['minter'], blockchain, web3=web3, block=block,
                                                 abi=ABI_POOL_ALTERNATIVE)
                else:
                    next_token = False

                continue

            except ValueError:
                next_token = False
                continue

            if decimals is True:
                if token_address == E_ADDRESS:
                    token_decimals = get_decimals(ZERO_ADDRESS, blockchain, web3=web3)
                else:
                    token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_decimals = 0

            balance = pool_contract.functions.balances(i).call(block_identifier=block)

            if convex_staked is None:
                token_balance = balance / (10 ** token_decimals) * (pool_balance_fraction)
                token_staked = balance / (10 ** token_decimals) * (pool_staked_fraction)

                balances.append([token_address, token_balance, token_staked])

            else:
                convex_pool_fraction = convex_staked / lptoken_data['totalSupply']
                token_staked = balance / (10 ** token_decimals) * convex_pool_fraction

                balances.append([token_address, token_staked])

            i += 1

        if reward is True:

            all_rewards = get_all_rewards(wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals,
                                          gauge_address=lptoken_data['gauge'])

            result.append(balances)
            result.append(all_rewards)

        else:
            result = balances

        return result

    except GetNodeIndexError:
        return underlying(wallet, lptoken_address, block, blockchain, convex_staked=convex_staked,
                          gauge_address=gauge_address, reward=reward, decimals=decimals, index=0,
                          execution=execution + 1)

    except:
        return underlying(wallet, lptoken_address, block, blockchain, convex_staked=convex_staked,
                          gauge_address=gauge_address, reward=reward, decimals=decimals, index=index + 1,
                          execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# unwrap
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# Output: a list with 1 element:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def unwrap(lptoken_amount, lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True):
    """

    :param lptoken_amount:
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

        lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3, index=index)

        if lptoken_data['minter'] is None:
            lptoken_data['minter'] = get_pool_address(web3, lptoken_address, block, blockchain)

        pool_contract = get_contract(lptoken_data['minter'], blockchain, web3=web3, block=block)
        pool_fraction = lptoken_amount / lptoken_data['totalSupply'] * (10 ** lptoken_data['decimals'])

        next_token = True
        i = 0
        while (next_token is True):

            try:
                token_address = pool_contract.functions.coins(i).call(block_identifier=block)

            except ContractLogicError:

                # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALTERNATIVE
                if i == 0:
                    pool_contract = get_contract(lptoken_data['minter'], blockchain, web3=web3, block=block,
                                                 abi=ABI_POOL_ALTERNATIVE)
                else:
                    next_token = False

                continue

            except ValueError:
                next_token = False
                continue

            if decimals is True:
                if token_address == E_ADDRESS:
                    token_decimals = get_decimals(ZERO_ADDRESS, blockchain, web3=web3)
                else:
                    token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_decimals = 0

            # We subtract the admin fees from the pool balances
            balance = pool_contract.functions.balances(i).call(
                block_identifier=block) - pool_contract.functions.admin_balances(i).call(block_identifier=block)

            token_balance = balance / (10 ** token_decimals) * pool_fraction

            balances.append([token_address, token_balance])

            i += 1

        return balances

    except GetNodeIndexError:
        return unwrap(lptoken_amount, lptoken_address, block, blockchain, decimals=decimals, index=0,
                      execution=execution + 1)

    except:
        return unwrap(lptoken_amount, lptoken_address, block, blockchain, decimals=decimals, index=index + 1,
                      execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# pool_balances
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# 'meta' = indicates if the pool is meta or not
# Output: a list with 1 elements:
# 1 - List of Tuples: [liquidity_token_address, balance]
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def pool_balances(lptoken_address, block, blockchain, web3=None, execution=1, index=0, decimals=True, meta=False):
    """

    :param lptoken_address:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param decimals:
    :param meta:
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

        try:
            minter = lptoken_contract.functions.minter().call()
        except:
            minter = None

        if minter is None:
            minter = get_pool_address(web3, lptoken_address, block, blockchain)

        pool_contract = get_contract(minter, blockchain, web3=web3, block=block, abi=ABI_POOL)

        next_token = True
        i = 0
        while (next_token is True):

            try:
                token_address = pool_contract.functions.coins(i).call(block_identifier=block)

            except ContractLogicError:

                # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALTERNATIVE
                if i == 0:
                    pool_contract = get_contract(minter, blockchain, web3=web3, block=block, abi=ABI_POOL_ALTERNATIVE)
                else:
                    next_token = False

                continue

            except ValueError:
                next_token = False
                continue

            if decimals is True:
                if token_address == E_ADDRESS:
                    token_decimals = get_decimals(ZERO_ADDRESS, blockchain, web3=web3)
                else:
                    token_decimals = get_decimals(token_address, blockchain, web3=web3)
            else:
                token_decimals = 0

            balance = pool_contract.functions.balances(i).call(block_identifier=block)

            token_balance = balance / (10 ** token_decimals)

            # Fetches the 3CR underlying balances in the 3pool
            if token_address != X3CRV_ETH and token_address != X3CRV_XDAI:
                balances.append([token_address, token_balance])
            else:
                if meta is False:
                    balances.append([token_address, token_balance])
                else:
                    underlying = unwrap(token_balance, token_address, block, blockchain)
                    for element in underlying:
                        balances.append([element[0], element[1]])

            i += 1

        return balances

    except GetNodeIndexError:
        return pool_balances(lptoken_address, block, blockchain, meta=meta, decimals=decimals, index=0,
                             execution=execution + 1)

    except:
        return pool_balances(lptoken_address, block, blockchain, meta=meta, decimals=decimals, index=index + 1,
                             execution=execution)


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# swap_fees
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# IMPORTANT: THIS FUNCTIONS MUST BE MODIFIED IN ORDER TO WROK PROPERLY. A DEEP RESEARCH MUST BE DONE TO GET THE SWAP FEES FOR META POOLS (FOR
# EVERY POOL TYPE). THE "GET_POOL_DATA" FUNCTION MUST BE CHANGED AS WELL.
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block_start, index=index)

        lptoken_address = web3.to_checksum_address(lptoken_address)

        lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN, block=block_start)

        try:
            minter = lptoken_contract.functions.minter().call()
        except:
            minter = None

        if minter is None:
            minter = get_pool_address(web3, lptoken_address, block_start, blockchain)

        pool_data = get_pool_data(web3, minter, block_start, blockchain)

        result['swaps'] = []

        exchange_event_signatures = []

        # IMPORTANT: AD-HOC FIX UNTIL WE FIND A WAY TO SOLVE HOW META POOLS WORK FOR DIFFERENT POOL TYPES AND SIDE-CHAINS
        # if pool_data['is_metapool'] is True:
        #     exchange_event_signatures = TOKEN_EXCHANGE_EVENT_SIGNATURES + TOKEN_EXCHANGE_UNDERLYING_EVENT_SIGNATURES
        # else:
        #     exchange_event_signatures = TOKEN_EXCHANGE_EVENT_SIGNATURES
        exchange_event_signatures = TOKEN_EXCHANGE_EVENT_SIGNATURES + TOKEN_EXCHANGE_UNDERLYING_EVENT_SIGNATURES + TOKEN_EXCHANGE_EVENT_SIGNATURES

        for exchange_event_signature in exchange_event_signatures:

            get_logs_bool = True
            block_from = block_start
            block_to = block_end
            hash_overlap = []

            exchange_event = web3.keccak(text=exchange_event_signature).hex()

            while get_logs_bool:
                swap_logs = get_logs(block_from, block_to, minter, exchange_event, blockchain)

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

                        token_out = pool_data['coins'][int(swap_log['data'][-128:-64], 16)]
                        token_out_decimals = get_decimals(token_out, blockchain, web3=web3)

                        swap_fee = pool_data['contract'].functions.fee().call(block_identifier=block_number) / (
                                    10 ** 10)

                        swap_data = {
                            'block': block_number,
                            'tokenOut': token_out,
                            'amountOut': swap_fee * int(swap_log['data'][-64:], 16) / (10 ** token_out_decimals)
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


def get_base_apr(lptoken_address: str, blockchain: str, block_end: Union[int, str] = 'latest', web3=None, days: int = 1,
                 apy: bool = False, execution: int = 1, index: int = 0) -> int:
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block_end, index=index)

        block_start = date_to_block(datetime.strftime(
            datetime.strptime(block_to_date(block_end, blockchain), '%Y-%m-%d %H:%M:%S') - timedelta(days=days),
            '%Y-%m-%d %H:%M:%S'), blockchain)
        lptoken_address = web3.to_checksum_address(lptoken_address)
        address_abi = get_contract_abi(lptoken_address, blockchain)

        lp_contract = get_contract(lptoken_address, blockchain, web3, abi=address_abi, block=block_end)

        try:
            xcp_profit = lp_contract.functions.xcp_profit().call(block_identifier=block_end)
            xcp_profit_a = lp_contract.functions.xcp_profit_a().call(block_identifier=block_end)
            xcp_profit_prev = lp_contract.functions.xcp_profit().call(block_identifier=block_start)
            xcp_profit_a_prev = lp_contract.functions.xcp_profit_a().call(block_identifier=block_start)
            growth = ((xcp_profit / 2) + (xcp_profit_a / 2) + 1 ** 18) / 2
            growth_prev = ((xcp_profit_prev / 2) + (xcp_profit_a_prev / 2) + 1 ** 18) / 2
            rate = ((growth - growth_prev) / growth_prev) / 2
            return rate

        except:
            virt_price = lp_contract.functions.get_virtual_price().call(block_identifier=block_end)
            virt_price_prev = lp_contract.functions.get_virtual_price().call(block_identifier=block_start)
            rate = (virt_price - virt_price_prev) / virt_price_prev
            return rate

    except GetNodeIndexError:
        return get_base_apr(lptoken_address, blockchain, block_end, web3, days, apy, execution=execution + 1, index=0)
    except:
        return get_base_apr(lptoken_address, blockchain, block_end, web3, days, apy, index=index + 1,
                            execution=execution)


def swap_fees_v2(lptoken_address: str, blockchain: str, block_end: Union[int, str] = 'latest', web3=None, days: int = 1,
                 apy: bool = False, execution: int = 1, index: int = 0) -> int:
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block_end, index=index)
        rate = get_base_apr(lptoken_address, blockchain, block_end, web3, days, apy, execution, index)
        lptoken_address = web3.to_checksum_address(lptoken_address)
        address_abi = get_contract_abi(lptoken_address, blockchain)
        lp_contract = get_contract(lptoken_address, blockchain, web3, abi=address_abi, block=block_end)
        balance = []
        for i in range(0, 5):
            try:
                balance_token = lp_contract.functions.balances(i).call(block_identifier=block_end)
                address_token = lp_contract.functions.coins(i).call()
                tvl_token = (balance_token / 10 ** get_decimals(address_token, blockchain)) * \
                            get_price(address_token, block_end, blockchain)[0]

                balance.append(tvl_token)
            except:
                break
        fees = rate * sum(balance)
        return fees

    except GetNodeIndexError:
        return swap_fees_v2(lptoken_address, blockchain, block_end, web3, days, apy, execution=execution + 1, index=0)
    except:
        return swap_fees_v2(lptoken_address, blockchain, block_end, web3, days, apy, index=index + 1,
                            execution=execution)


def get_swap_fees_APR(lptoken_address: str, blockchain: str, block_end: Union[int, str] = 'latest', web3=None,
                      days: int = 1, apy: bool = False, execution: int = 1, index: int = 0) -> int:
    rate = get_base_apr(lptoken_address, blockchain, block_end, web3, days, apy, execution, index)
    apr = ((1 + rate) ** (365 / days) - 1) * 100
    seconds_per_year = 365 * 24 * 60 * 60
    if apy == True:
        apy = (1 + (apr / seconds_per_year)) ** (seconds_per_year) - 1
        return apy
    else:
        return apr

    # blockchain = ETHEREUM
# lptoken = '0xd51a44d3fae010294c616388b506acda1bfaae46'
# blockstart = date_to_block('2023-03-02 00:00:00',blockchain)
# blockend = date_to_block('2023-02-20 19:24:00',blockchain)

# feess = swap_fees_v2(lptoken,blockchain,blockstart)
# print(feess)

# feesss = get_swap_fees_APR(lptoken,blockchain,blockstart)
# print(feesss)
