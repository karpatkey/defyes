import logging
from contextlib import suppress
from decimal import Decimal
from typing import Union

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr
from karpatkit.cache import const_call
from karpatkit.constants import Address
from karpatkit.explorer import ChainExplorer
from karpatkit.helpers import suppress_error_codes
from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.functions import balance_of, get_contract, get_decimals, get_logs_web3, to_token_amount
from defyes.lazytime import Duration, Time
from defyes.prices.prices import get_price

logger = logging.getLogger(__name__)

PROVIDER_ADDRESS = "0x0000000022D53366457F9d5E68Ec105046FC4383"

X_CHAIN_GAUGE_FACTORY_ADDRESS = "0xabC000d88f23Bb45525E447528DBF656A9D55bf5"

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

# Registry for Crypto Factory V2 Pools ABI - get_gauge, pool_list, pool_count
ABI_REGISTRY_CRYPTO_FACTORY_V2_POOLS = '[{"stateMutability":"view","type":"function","name":"get_gauge","inputs":[{"name":"_pool","type":"address"}],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"pool_list","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}]}, {"stateMutability":"view","type":"function","name":"pool_count","inputs":[],"outputs":[{"name":"","type":"uint256"}]}]'

# LP Token ABI - decimals, totalSupply, minter, balanceOf
ABI_LPTOKEN = '[{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"decimals","inputs":[],"gas":288}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"totalSupply","inputs":[],"gas":2808}, {"type":"function","stateMutability":"view","outputs":[{"type":"address","name":""}],"name":"minter","inputs":[],"gas":2838}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"balanceOf","inputs":[{"type":"address","name":"arg0"}],"gas":2963}]'

# Pool ABI - coins, balances, fee, underlying_coins, token
ABI_POOL = '[{"type":"function","stateMutability":"view","outputs":[{"type":"address","name":""}],"name":"coins","inputs":[{"type":"uint256","name":"arg0"}],"gas":1917}, {"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":""}],"name":"balances","inputs":[{"type":"uint256","name":"arg0"}],"gas":1947}, {"name":"fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2051}, {"name":"underlying_coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2160}, {"stateMutability":"view","type":"function","name":"token","inputs":[],"outputs":[{"name":"","type":"address"}]}]'

# Alternative Pool ABI - coins, balances, fee, underlying_coins
ABI_POOL_ALTERNATIVE = '[{"name":"coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2130}, {"name":"balances","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2190}, {"name":"fee","outputs":[{"type":"uint256","name":""}],"inputs":[],"constant":true,"payable":false,"type":"function","gas":2051}, {"name":"underlying_coins","outputs":[{"type":"address","name":""}],"inputs":[{"type":"int128","name":"arg0"}],"constant":true,"payable":false,"type":"function","gas":2160}]'

# Gauge ABI - crv_token, claimable_tokens, rewarded_token, claimable_reward, claimed_rewards_for, reward_tokens, claimable_reward, claimable_reward_write, decimals, version, minter
ABI_GAUGE = '[{"name":"crv_token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1451}, {"name":"claimable_tokens","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"nonpayable","type":"function","gas":1989612}, {"name":"rewarded_token","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":2201}, {"name":"claimable_reward","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"addr"}],"stateMutability":"view","type":"function","gas":7300}, {"name":"claimed_rewards_for","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"arg0"}],"stateMutability":"view","type":"function","gas":2475}, {"name":"reward_tokens","outputs":[{"type":"address","name":""}],"inputs":[{"type":"uint256","name":"arg0"}],"stateMutability":"view","type":"function","gas":2550}, {"name":"claimable_reward","outputs":[{"type":"uint256","name":""}],"inputs":[{"type":"address","name":"_addr"},{"type":"address","name":"_token"}],"stateMutability":"nonpayable","type":"function","gas":1017930}, {"stateMutability":"nonpayable","type":"function","name":"claimable_reward_write","inputs":[{"name":"_addr","type":"address"},{"name":"_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":1211002}, {"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":288}, {"stateMutability":"view","type":"function","name":"version","inputs":[],"outputs":[{"name":"","type":"string"}]}, {"name":"minter","outputs":[{"type":"address","name":""}],"inputs":[],"stateMutability":"view","type":"function","gas":1421}]'

# TokenExchange Event Signatures
TOKEN_EXCHANGE_EVENT_SIGNATURES = [
    "TokenExchange(address,int128,uint256,int128,uint256)",
    "TokenExchange(address,uint256,uint256,uint256,uint256)",
]

# TokenExchangeUnderlying Event Signatures
TOKEN_EXCHANGE_UNDERLYING_EVENT_SIGNATURES = [
    "TokenExchangeUnderlying(address,int128,uint256,int128,uint256)",
    "TokenExchangeUnderlying(address,uint256,uint256,uint256,uint256)",
]


def get_registry_contract(web3, id, block, blockchain):
    provider_contract = get_contract(PROVIDER_ADDRESS, blockchain, web3=web3, abi=ABI_PROVIDER)

    registry_address = const_call(provider_contract.functions.get_address(id))

    if id == 0:
        abi = ABI_REGISTRY_REGULAR_POOLS
    elif id == 3:
        abi = ABI_REGISTRY_FACTORY_POOLS
    elif id == 5:
        abi = ABI_REGISTRY_CRYPTO_V2_POOLS
    elif id == 6:
        abi = ABI_REGISTRY_CRYPTO_FACTORY_POOLS
    elif id == 11:
        abi = ABI_REGISTRY_CRYPTO_FACTORY_V2_POOLS
    else:
        abi = ABI_REGISTRY_REGULAR_POOLS

    return get_contract(registry_address, blockchain, web3=web3, abi=abi)


def get_pool_gauge_address(web3, pool_address, lptoken_address, block, blockchain):
    gauge_address = None

    # 1: Try to retrieve the gauge address assuming the pool is a Regular Pool
    registry_contract = get_registry_contract(web3, 0, block, blockchain)

    if registry_contract.address != Address.ZERO:
        gauge_address = const_call(registry_contract.functions.get_gauges(pool_address))[0][0]

    # 2: Try to retrieve the gauge address assuming the pool is a Factory Pool
    if gauge_address == Address.ZERO:
        registry_contract = get_registry_contract(web3, 3, block, blockchain)

        if registry_contract.address != Address.ZERO:
            gauge_address = const_call(registry_contract.functions.get_gauge(pool_address))

    # 3: Try to retrieve the gauge address assuming the pool is a Crypto V2 Pool
    if gauge_address == Address.ZERO:
        registry_contract = get_registry_contract(web3, 5, block, blockchain)

        if registry_contract.address != Address.ZERO:
            gauge_address = const_call(registry_contract.functions.get_gauges(pool_address))[0][0]

    # 4: Try to retrieve the gauge address assuming the pool is a Crypto Factory Pool
    if gauge_address == Address.ZERO:
        registry_contract = get_registry_contract(web3, 6, block, blockchain)

        if registry_contract.address != Address.ZERO:
            gauge_address = const_call(registry_contract.functions.get_gauge(pool_address))

    # 5: Try to retrieve the gauge address assuming the pool is a Crypto V2 Factory Pool
    if gauge_address == Address.ZERO:
        registry_contract = get_registry_contract(web3, 11, block, blockchain)

        if registry_contract.address != Address.ZERO:
            gauge_address = const_call(registry_contract.functions.get_gauge(pool_address))

    # Pools which don't have their gauge registered in none of the registries
    if gauge_address == Address.ZERO and blockchain != Chain.ETHEREUM:
        x_chain_factory_contract = get_contract(
            X_CHAIN_GAUGE_FACTORY_ADDRESS, blockchain, web3=web3, abi=ABI_X_CHAIN_GAUGE_FACTORY_ADDRESS, block=block
        )
        gauge_address = const_call(x_chain_factory_contract.functions.get_gauge_from_lp_token(lptoken_address))

    return gauge_address


def working_version_request(gauge_contract):
    with suppress(ContractLogicError):
        version = const_call(gauge_contract.functions.version())
        if gauge_contract.w3._network_name != Chain.ETHEREUM:
            return "ChildGauge"
        else:
            if "v6" in version:
                return "LiquidityGaugeV6"
            elif "v5" in version:
                return "LiquidityGaugeV5"

    with suppress(ContractLogicError):
        const_call(gauge_contract.functions.claimable_reward_write(Address.ZERO, Address.ZERO))
        const_call(gauge_contract.functions.crv_token())
        return "LiquidityGaugeV3"

    with suppress(ContractLogicError):
        const_call(gauge_contract.functions.claimable_reward_write(Address.ZERO, Address.ZERO))
        return "RewardsOnlyGauge"

    with suppress(ContractLogicError):
        const_call(gauge_contract.functions.minter())
        const_call(gauge_contract.functions.decimals())
        const_call(gauge_contract.functions.claimable_reward(Address.ZERO))
        return "LiquidityGaugeReward"

    with suppress(ContractLogicError):
        const_call(gauge_contract.functions.minter())
        const_call(gauge_contract.functions.decimals())
        const_call(gauge_contract.functions.decimals())
        return "LiquidityGaugeV2"

    with suppress(ContractLogicError):
        const_call(gauge_contract.functions.minter())
        return "LiquidityGauge"

    return "LiquidityGaugeV4"


def get_gauge_version(gauge_address, block, blockchain, web3=None, only_version=True):
    if web3 is None:
        web3 = get_node(blockchain)

    # The ABI used to get the Gauge Contract is a general ABI for all types. This is because some gauges do not have
    # their ABIs available in the explorers
    gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE)
    version = working_version_request(gauge_contract)
    if only_version:
        return version
    return [version, gauge_contract]


def get_pool_address(web3, lptoken_address, block, blockchain):
    """
    IMPORTANT: "crypto factory" pools are not considered
                because the pool address is retrieved by
                the function get_lptoken_data (minter function)
    """
    # 1: Try to retrieve the pool address assuming the pool is a Regular Pool
    registry_contract = get_registry_contract(web3, 0, block, blockchain)

    if registry_contract.address != Address.ZERO:
        pool_address = const_call(registry_contract.functions.get_pool_from_lp_token(lptoken_address))

    # 2: Try to retrieve the pool address assuming the pool is a Crypto V2 Pool
    if pool_address == Address.ZERO:
        registry_contract = get_registry_contract(web3, 5, block, blockchain)

        if registry_contract.address != Address.ZERO:
            pool_address = const_call(registry_contract.functions.get_pool_from_lp_token(lptoken_address))

    # 3: If the pool is not a Regular Pool or a V2 Pool then it's a Factory Pool
    if pool_address == Address.ZERO:
        pool_address = lptoken_address

    return pool_address


def get_pool_data(web3, minter, block, blockchain):
    pool_data = {
        "contract": get_contract(minter, blockchain, web3=web3),
        "is_metapool": False,
        "coins": {},
    }

    try:
        const_call(pool_data["contract"].functions.underlying_coins(0))
        pool_data["is_metapool"] = True
    except ContractLogicError:
        pass

    next_token = True
    i = 0
    j = 0
    while next_token:
        try:
            token_address = pool_data["contract"].functions.coins(i).call(block_identifier=block)

        except ContractLogicError:
            # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALETRNATIVE
            if i == 0:
                pool_data["contract"] = get_contract(
                    minter, blockchain, web3=web3, block=block, abi=ABI_POOL_ALTERNATIVE
                )
            else:
                next_token = False

            continue

        except ValueError:
            next_token = False
            continue

        # IMPORTANT: AD-HOC FIX UNTIL WE FIND A WAY TO SOLVE HOW META POOLS WORK FOR DIFFERENT POOL TYPES AND SIDE-CHAINS
        # if token_address == EthereumTokenAddr.X3CRV or token_address == X3CRV_POL or token_address == GnosisTokenAddr.x3CRV:
        if token_address == EthereumTokenAddr.X3CRV:
            pool_data["is_metapool"] = True

            x3crv_minter = get_pool_address(web3, token_address, block, blockchain)
            x3crv_pool_contract = get_contract(x3crv_minter, blockchain, web3=web3)

            x3crv_next_token = True
            while x3crv_next_token:
                try:
                    token_address = x3crv_pool_contract.functions.coins(j).call(block_identifier=block)

                except ContractLogicError:
                    # If the query fails when j == 0 -> the pool contract must be retrieved with the ABI_POOL_ALETRNATIVE
                    if i == 0:
                        x3crv_pool_contract = get_contract(
                            x3crv_minter, blockchain, web3=web3, block=block, abi=ABI_POOL_ALTERNATIVE
                        )
                    else:
                        x3crv_next_token = False

                    continue

                except ValueError:
                    x3crv_next_token = False
                    continue

                pool_data["coins"][i + j] = token_address
                j += 1

        else:
            pool_data["coins"][i + j] = token_address

        i += 1

    return pool_data


def get_lptoken_data(lptoken_address, block, blockchain, web3=None):
    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_data = {}

    lptoken_data["contract"] = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    lptoken_data["minter"] = None
    with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
        lptoken_data["minter"] = const_call(lptoken_data["contract"].functions.minter())

    lptoken_data["decimals"] = const_call(lptoken_data["contract"].functions.decimals())
    lptoken_data["totalSupply"] = lptoken_data["contract"].functions.totalSupply().call(block_identifier=block)

    return lptoken_data


def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, gauge_address=None):
    """
    Output:
    List of Tuples: [reward_token_address, balance]
    """

    all_rewards = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if gauge_address is None:
        minter = get_pool_address(web3, lptoken_address, block, blockchain)

        gauge_address = get_pool_gauge_address(web3, minter, lptoken_address, block, blockchain)

    if gauge_address is None:
        return []

    gauge_data = get_gauge_version(gauge_address, block, blockchain, only_version=False)

    gauge_version = gauge_data[0]
    gauge_contract = gauge_data[1]

    if gauge_version in ["LiquidityGaugeV6", "LiquidityGaugeV5", "LiquidityGaugeV4", "LiquidityGaugeV2", "ChildGauge"]:
        i = 0
        while True:
            token_address = const_call(gauge_contract.functions.reward_tokens(i))

            if token_address != Address.ZERO:
                token_reward = gauge_contract.functions.claimable_reward(wallet, token_address).call(
                    block_identifier=block
                )
                all_rewards.append(
                    [token_address, to_token_amount(token_address, token_reward, blockchain, web3, decimals)]
                )
                i += 1
            else:
                break

        # CRV rewards
        if blockchain == Chain.ETHEREUM:
            token_address = EthereumTokenAddr.CRV
        elif blockchain == Chain.GNOSIS:
            token_address = GnosisTokenAddr.CRV

        token_reward = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block)
        all_rewards.append([token_address, to_token_amount(token_address, token_reward, blockchain, web3, decimals)])

    elif gauge_version in ["LiquidityGaugeV3", "RewardsOnlyGauge"]:
        i = 0
        while True:
            token_address = const_call(gauge_contract.functions.reward_tokens(i))
            if token_address != Address.ZERO:
                token_reward = gauge_contract.functions.claimable_reward_write(wallet, token_address).call(
                    block_identifier=block
                )
                all_rewards.append(
                    [token_address, to_token_amount(token_address, token_reward, blockchain, web3, decimals)]
                )
                i += 1
            else:
                break

        if gauge_version == "LiquidityGaugeV3":
            # CRV rewards
            if blockchain == Chain.ETHEREUM:
                token_address = EthereumTokenAddr.CRV
            elif blockchain == Chain.GNOSIS:
                token_address = GnosisTokenAddr.CRV

            token_reward = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block)
            all_rewards.append(
                [token_address, to_token_amount(token_address, token_reward, blockchain, web3, decimals)]
            )

    elif gauge_version in ["LiquidityGaugeReward", "LiquidityGauge"]:
        token_address = const_call(gauge_contract.functions.crv_token())
        token_reward = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block)
        all_rewards.append([token_address, to_token_amount(token_address, token_reward, blockchain, web3, decimals)])

        if gauge_version == "LiquidityGaugeReward":
            # Additional rewards
            token_address = const_call(gauge_contract.functions.rewarded_token())
            token_reward = gauge_contract.function.claimable_reward(wallet).call(block_identifier=block)
            token_reward -= gauge_contract.claimed_rewards_for(wallet).call(block_identifier=block)

            all_rewards.append(
                [token_address, to_token_amount(token_address, token_reward, blockchain, web3, decimals)]
            )

    return all_rewards


def underlying(
    wallet,
    lptoken_address,
    block,
    blockchain,
    web3=None,
    reward=False,
    decimals=True,
    convex_staked=None,
    gauge_address=None,
):
    """
    'convex_staked' = Staked LP Token Balance in Convex
    'gauge_address' = gauge_address
    Output: a list with 2 elements:
    1 - List of Tuples: [liquidity_token_address, balance, staked_balance]
    2 - List of Tuples: [reward_token_address, balance]
    """

    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    lptoken_data["balanceOf"] = lptoken_data["contract"].functions.balanceOf(wallet).call(block_identifier=block)

    if lptoken_data["minter"] is None:
        lptoken_data["minter"] = get_pool_address(web3, lptoken_address, block, blockchain)

    if gauge_address is not None:
        lptoken_data["gauge"] = gauge_address
    else:
        lptoken_data["gauge"] = get_pool_gauge_address(web3, lptoken_data["minter"], lptoken_address, block, blockchain)

    if lptoken_data["gauge"] is not None and lptoken_data["gauge"] != Address.ZERO:
        lptoken_data["staked"] = balance_of(wallet, lptoken_data["gauge"], block, blockchain, web3=web3, decimals=False)
    else:
        lptoken_data["staked"] = 0

    pool_contract = get_contract(lptoken_data["minter"], blockchain, web3=web3)

    pool_balance_fraction = lptoken_data["balanceOf"] / lptoken_data["totalSupply"]
    pool_staked_fraction = lptoken_data["staked"] / lptoken_data["totalSupply"]

    next_token = True
    i = 0
    while next_token:
        try:
            token_address = pool_contract.functions.coins(i).call(block_identifier=block)
        except ContractLogicError:
            # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALETRNATIVE
            if i == 0:
                pool_contract = get_contract(
                    lptoken_data["minter"], blockchain, web3=web3, block=block, abi=ABI_POOL_ALTERNATIVE
                )
            else:
                next_token = False
            continue

        except ValueError:
            next_token = False
            continue

        balance = pool_contract.functions.balances(i).call(block_identifier=block)
        balance = to_token_amount(token_address, balance, blockchain, web3, decimals)

        if convex_staked is None:
            balances.append(
                [token_address, balance * Decimal(pool_balance_fraction), balance * Decimal(pool_staked_fraction)]
            )

        else:
            convex_pool_fraction = convex_staked / lptoken_data["totalSupply"]
            balances.append([token_address, balance * Decimal(convex_pool_fraction)])

        i += 1

    result = balances
    if reward:
        all_rewards = get_all_rewards(
            wallet,
            lptoken_address,
            block,
            blockchain,
            web3=web3,
            decimals=decimals,
            gauge_address=lptoken_data["gauge"],
        )

        result.extend(all_rewards)

    return result


def unwrap(lptoken_amount, lptoken_address, block, blockchain, web3=None, decimals=True):
    """
    Output: a list with 1 element:
    1 - List of Tuples: [liquidity_token_address, balance]
    """

    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_data = get_lptoken_data(lptoken_address, block, blockchain, web3=web3)

    if lptoken_data["minter"] is None:
        lptoken_data["minter"] = get_pool_address(web3, lptoken_address, block, blockchain)

    pool_contract = get_contract(lptoken_data["minter"], blockchain, web3=web3)
    pool_fraction = (
        Decimal(lptoken_amount) / Decimal(lptoken_data["totalSupply"]) * Decimal(10 ** lptoken_data["decimals"])
    )

    next_token = True
    i = 0
    while next_token:
        try:
            token_address = pool_contract.functions.coins(i).call(block_identifier=block)
        except ContractLogicError:
            # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALTERNATIVE
            if i == 0:
                pool_contract = get_contract(
                    lptoken_data["minter"], blockchain, web3=web3, block=block, abi=ABI_POOL_ALTERNATIVE
                )
            else:
                next_token = False
            continue
        except ValueError:
            next_token = False
            continue

        if decimals:
            if token_address == Address.E:
                token_decimals = get_decimals(Address.ZERO, blockchain, web3=web3)
            else:
                token_decimals = get_decimals(token_address, blockchain, web3=web3)
        else:
            token_decimals = 0

        # We subtract the admin fees from the pool balances
        balance = pool_contract.functions.balances(i).call(
            block_identifier=block
        ) - pool_contract.functions.admin_balances(i).call(block_identifier=block)

        token_balance = Decimal(balance) / Decimal(10**token_decimals) * Decimal(pool_fraction)

        balances.append([token_address, token_balance])

        i += 1

    return balances


def pool_balances(lptoken_address, block, blockchain, web3=None, decimals=True, meta=False):
    """
    Output: a list with 1 elements:
    1 - List of Tuples: [liquidity_token_address, balance]
    """

    balances = []

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    minter = None
    with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
        minter = const_call(lptoken_contract.functions.minter())

    if minter is None:
        minter = get_pool_address(web3, lptoken_address, block, blockchain)

    pool_contract = get_contract(minter, blockchain, web3=web3)

    next_token = True
    i = 0
    while next_token:
        try:
            token_address = pool_contract.functions.coins(i).call(block_identifier=block)
        except ContractLogicError:
            # If the query fails when i == 0 -> the pool contract must be retrieved with the ABI_POOL_ALTERNATIVE
            if i == 0:
                pool_contract = get_contract(minter, blockchain, web3=web3)
            else:
                next_token = False
            continue

        except ValueError:
            next_token = False
            continue

        balance = pool_contract.functions.balances(i).call(block_identifier=block)
        # Fetches the 3CR underlying balances in the 3pool
        if token_address != EthereumTokenAddr.X3CRV and token_address != GnosisTokenAddr.x3CRV:
            balances.append([token_address, to_token_amount(token_address, balance, blockchain, web3, decimals)])
        else:
            if meta is False:
                balances.append([token_address, to_token_amount(token_address, balance, blockchain, web3, decimals)])
            else:
                underlying = unwrap(
                    to_token_amount(token_address, balance, blockchain, web3, decimals),
                    token_address,
                    block,
                    blockchain,
                )
                for element in underlying:
                    balances.append([element[0], element[1]])

        i += 1

    return balances


def swap_fees(lptoken_address, block_start, block_end, blockchain, web3=None, decimals=True):
    # FIXME: decimals is ignored
    # FIXME:
    """
    IMPORTANT: THIS FUNCTIONS MUST BE MODIFIED IN ORDER TO WORK PROPERLY.
    A DEEP RESEARCH MUST BE DONE TO GET THE SWAP FEES FOR META POOLS
    (FOR EVERY POOL TYPE). THE "GET_POOL_DATA" FUNCTION MUST BE CHANGED AS WELL.
    """

    result = {}

    if web3 is None:
        web3 = get_node(blockchain)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    lptoken_contract = get_contract(lptoken_address, blockchain, web3=web3, abi=ABI_LPTOKEN)

    try:
        minter = const_call(lptoken_contract.functions.minter())
    except ContractLogicError:
        minter = None

    if minter is None:
        minter = get_pool_address(web3, lptoken_address, block_start, blockchain)

    pool_data = get_pool_data(web3, minter, block_start, blockchain)

    result["swaps"] = []

    exchange_event_signatures = []

    # IMPORTANT: AD-HOC FIX UNTIL WE FIND A WAY TO SOLVE HOW META POOLS WORK FOR DIFFERENT POOL TYPES AND SIDE-CHAINS
    # if pool_data['is_metapool']:
    #     exchange_event_signatures = TOKEN_EXCHANGE_EVENT_SIGNATURES + TOKEN_EXCHANGE_UNDERLYING_EVENT_SIGNATURES
    # else:
    #     exchange_event_signatures = TOKEN_EXCHANGE_EVENT_SIGNATURES
    exchange_event_signatures = (
        TOKEN_EXCHANGE_EVENT_SIGNATURES + TOKEN_EXCHANGE_UNDERLYING_EVENT_SIGNATURES + TOKEN_EXCHANGE_EVENT_SIGNATURES
    )

    for exchange_event_signature in exchange_event_signatures:
        exchange_event = web3.keccak(text=exchange_event_signature).hex()
        swap_logs = get_logs_web3(
            blockchain=blockchain, address=minter, block_start=block_start, block_end=block_end, topics=[exchange_event]
        )

        for swap_log in swap_logs:
            token_out = pool_data["coins"][int(swap_log["data"].hex()[-128:-64], 16)]
            token_out_decimals = get_decimals(token_out, blockchain, web3=web3)

            # FIXME: shouldn't the 10 be token_out_decimals???
            swap_fee = Decimal(
                pool_data["contract"].functions.fee().call(block_identifier=swap_log["blockNumber"])
            ) / Decimal(10**10)

            swap_data = {
                "block": swap_log["blockNumber"],
                "tokenOut": token_out,
                "amountOut": swap_fee * int(swap_log["data"].hex()[-64:], 16) / Decimal(10**token_out_decimals),
            }

            result["swaps"].append(swap_data)

    return result


def get_base_apr(
    lptoken_address: str,
    blockchain: str,
    block_end: Union[int, str] = "latest",
    web3=None,
    days: int = 1,
    apy: bool = False,
) -> int:
    if web3 is None:
        web3 = get_node(blockchain)

    chain_explorer = ChainExplorer(blockchain)
    block_start = chain_explorer.block_from_time(Time(chain_explorer.time_from_block(block_end)) - Duration.days(days))
    lptoken_address = Web3.to_checksum_address(lptoken_address)
    address_abi = chain_explorer.abi_from_address(lptoken_address)

    lp_contract = get_contract(lptoken_address, blockchain, web3, abi=address_abi)

    try:
        xcp_profit = lp_contract.functions.xcp_profit().call(block_identifier=block_end)
        xcp_profit_a = lp_contract.functions.xcp_profit_a().call(block_identifier=block_end)
        xcp_profit_prev = lp_contract.functions.xcp_profit().call(block_identifier=block_start)
        xcp_profit_a_prev = lp_contract.functions.xcp_profit_a().call(block_identifier=block_start)
        growth = ((xcp_profit / 2) + (xcp_profit_a / 2) + Decimal(1**18)) / 2
        growth_prev = ((xcp_profit_prev / 2) + (xcp_profit_a_prev / 2) + Decimal(1**18)) / 2
        rate = ((growth - growth_prev) / growth_prev) / 2
        return rate
    except (ContractLogicError, BadFunctionCallOutput):
        virt_price = lp_contract.functions.get_virtual_price().call(block_identifier=block_end)
        virt_price_prev = lp_contract.functions.get_virtual_price().call(block_identifier=block_start)
        rate = (virt_price - virt_price_prev) / Decimal(virt_price_prev)
        return rate


def swap_fees_v2(
    lptoken_address: str,
    blockchain: str,
    block_end: Union[int, str] = "latest",
    web3=None,
    days: int = 1,
    apy: bool = False,
) -> int:
    if web3 is None:
        web3 = get_node(blockchain)
    rate = get_base_apr(lptoken_address, blockchain, block_end, web3, days, apy)
    lptoken_address = Web3.to_checksum_address(lptoken_address)
    address_abi = ChainExplorer(blockchain).abi_from_address(lptoken_address)
    lp_contract = get_contract(lptoken_address, blockchain, web3, abi=address_abi)
    balance = []
    for i in range(0, 5):
        try:
            balance_token = lp_contract.functions.balances(i).call(block_identifier=block_end)
            address_token = const_call(lp_contract.functions.coins(i))
            tvl_token = to_token_amount(address_token, balance_token, blockchain, web3, decimals=True)
            tvl_token *= Decimal(get_price(address_token, block_end, blockchain)[0])
            balance.append(tvl_token)
        except (ContractLogicError, BadFunctionCallOutput):
            break
    fees = rate * sum(balance)
    return fees


# FIXME: this looks unfinished
def get_swap_fees_APR(
    lptoken_address: str,
    blockchain: str,
    block_end: Union[int, str] = "latest",
    web3=None,
    days: int = 1,
    apy: bool = False,
) -> int:
    rate = get_base_apr(lptoken_address, blockchain, block_end, web3, days, apy)
    apr = ((1 + rate) ** (365 / days) - 1) * 100
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        apy = (1 + (apr / seconds_per_year)) ** (seconds_per_year) - 1
        return apy
    else:
        return apr
