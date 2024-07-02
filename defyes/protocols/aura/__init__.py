import json
from decimal import Decimal
from pathlib import Path

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.cache import const_call
from karpatkit.helpers import call_contract_method
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, get_decimals, get_logs_web3, last_block, to_token_amount

from .. import balancer

# Booster (Main Deposit Contract) - Mainnet
# BOOSTER = '0x7818A1DA7BD1E64c199029E86Ba244a9798eEE10' (Old Version)
BOOSTER = "0xA57b8d98dAE62B26Ec3bcC4a365338157060B234"

# Booster Lite for side-chains
BOOSTER_LITE = "0x98Ef32edd24e2c92525E59afc4475C1242a30184"

# Mainnet Addresses
stkauraBAL = "0xfAA2eD111B4F580fCb85C48E6DC6782Dc5FCD7a6"  # mainnet

AURA_LOCKER = "0x3Fa73f1E5d8A792C80F426fc8F84FBF7Ce9bBCAC"

# AURABAL_REWARDER = '0x5e5ea2048475854a5702f5b8468a51ba1296efcc' (Old Version)
AURABAL_REWARDER = "0x00A7BA8Ae7bca0B10A32Ea1f8e2a1Da980c6CAd2"

REWARD_POOL_DEPOSIT_WRAPPER = "0xB188b1CB84Fb0bA13cb9ee1292769F903A9feC59"

# Extra Rewards are from those that claimed the initial AURA airdrop to their wallet instead of locking it
EXTRA_REWARDS_DISTRIBUTOR = "0xA3739b206097317c72EF416F0E75BB8f58FbD308"

# This dict holds the block in which each deployed Rewarder Factory was created
REWARDER_FACTORIES = {
    Chain.ETHEREUM: {"0xBC8d9cAf4B6bf34773976c5707ad1F2778332DcA": 16176243},
    Chain.POLYGON: {"0xB292BE31649A0b079DBdb772FCf5c7a02a6E0144": 45241040},
    Chain.ARBITRUM: {"0xda2e6bA0B1aBBCA925b70E9747AFbD481C16e7dB": 101062073},
    Chain.GNOSIS: {"0x0F641b291Ba374Ec9B17a878c54B98005a0BAcaE": 29283300},
    Chain.OPTIMISM: {"0x2F4CdF0D46F4E3E6D4d37836E73073046138D4f7": 106269709},
}


# Ethereum Rewarder Factory Contract Address
REWARDER_FACTORY_ETHEREUM = "0xBC8d9cAf4B6bf34773976c5707ad1F2778332DcA"
REWARDER_FACTORY_ETHEREUM_V2 = "0xBC8d9cAf4B6bf34773976c5707ad1F2778332DcB"

# Polygon Rewarder Factory Contract Address
REWARDER_FACTORY_POLYGON = "0xB292BE31649A0b079DBdb772FCf5c7a02a6E0144"

# Arbitrum Rewarder Factory Contract Address
REWARDER_FACTORY_ARBITRUM = "0xda2e6bA0B1aBBCA925b70E9747AFbD481C16e7dB"

# Optimism Rewarder Factory Contract Address
REWARDER_FACTORY_OPTIMISM = "0x2F4CdF0D46F4E3E6D4d37836E73073046138D4f7"

# Gnosis Chain Rewarder Factory Contract Address
REWARDER_FACTORY_XDAI = "0x0F641b291Ba374Ec9B17a878c54B98005a0BAcaE"

# Booster ABI - poolInfo, poolLength, rewardFactory, minter, getRewardMultipliers, REWARD_MULTIPLIER_DENOMINATOR
ABI_BOOSTER = '[{"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"poolInfo","outputs":[{"internalType":"address","name":"lptoken","type":"address"},{"internalType":"address","name":"token","type":"address"},{"internalType":"address","name":"gauge","type":"address"},{"internalType":"address","name":"crvRewards","type":"address"},{"internalType":"address","name":"stash","type":"address"},{"internalType":"bool","name":"shutdown","type":"bool"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"poolLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardFactory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"minter","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"getRewardMultipliers","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"REWARD_MULTIPLIER_DENOMINATOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# REWARDER ABI - balanceOf, earned, extraRewards, extraRewardsLength, rewardToken, rewards, stakingToken, totalSupply
ABI_REWARDER = '[{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"earned","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"rewardToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"rewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"stakingToken","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# stkauraBAL ABI - balanceOfUnderlying, underlying, extraRewards, extraRewardsLength
ABI_STKAURABAL = '[{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"balanceOfUnderlying","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"underlying","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"extraRewards","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"extraRewardsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA ABI - EMISSIONS_MAX_SUPPLY, INIT_MINT_AMOUNT, decimals, reductionPerCliff, totalCliffs, totalSupply
ABI_AURA = '[{"inputs":[],"name":"EMISSIONS_MAX_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"INIT_MINT_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"reductionPerCliff","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalCliffs","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# AURA LOCKER ABI - balances, claimableRewards
ABI_AURA_LOCKER = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint112","name":"locked","type":"uint112"},{"internalType":"uint32","name":"nextUnlockIndex","type":"uint32"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"address","name":"_account","type":"address"}],"name":"claimableRewards","outputs":[{"components":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"internalType":"struct AuraLocker.EarnedData[]","name":"userRewards","type":"tuple[]"}],"stateMutability":"view","type":"function"}]'

# EXTRA REWARDS DISTRIBUTOR ABI - claimableRewards
ABI_EXTRA_REWARDS_DISTRIBUTOR = '[{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"address","name":"_token","type":"address"}],"name":"claimableRewards","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# EXTRA REWARD TOKEN ABI - baseToken
ABI_EXTRA_REWARDS_TOKEN = '[{"inputs":[],"name":"baseToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

# L2COORDINATOR ABI - auraOFT, mintRate
ABI_L2COORDINATOR = '[{"inputs":[],"name":"auraOFT","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"mintRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# DB
# Format
# { balancerLPcontractAddr: {
#     "poolId": poolId,
#     "token": auraLPtoken,
#     "gauge": balancerLPGauge,
#     "crvRewards": auraBaseRewardPool,
#     "stash": auraExtraRewardStash,
#     "shutdown": bool  # deprecated pool
#     },
# }
DB_FILE = Path(__file__).parent / "db.json"

# Reward Pool Created Event Signature
REWARD_POOL_CREATED_EVENT_SIGNATURE = "RewardPoolCreated(address,uint256,address)"


def get_pool_rewarders(booster_contract, lptoken_address, blockchain, block):
    if isinstance(block, str):
        if block == "latest":
            block = last_block(blockchain)
        else:
            raise ValueError("Incorrect block.")

    with open(DB_FILE, "r") as db_file:
        db_data = json.load(db_file)

    rewarders = []
    if lptoken_address in db_data[blockchain].keys():
        blocks = list(db_data[blockchain][lptoken_address].keys())[::-1]
        for iblock in blocks:
            if block >= int(iblock):
                rewarders.append(db_data[blockchain][lptoken_address][iblock]["rewarder"])

    else:
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
    reward_token_address = const_call(rewarder_contract.functions.rewardToken())
    bal_rewards = rewarder_contract.functions.earned(wallet).call(block_identifier=block)

    return [reward_token_address, to_token_amount(reward_token_address, bal_rewards, blockchain, web3, decimals)]


def get_extra_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=True):
    extra_rewards = []

    extra_rewards_length = rewarder_contract.functions.extraRewardsLength().call(block_identifier=block)
    for n in range(extra_rewards_length):
        extra_reward_contract_address = rewarder_contract.functions.extraRewards(n).call(block_identifier=block)
        extra_reward_contract = get_contract(extra_reward_contract_address, blockchain, web3=web3, abi=ABI_REWARDER)

        extra_reward_token_address = const_call(extra_reward_contract.functions.rewardToken())

        extra_reward_token_contract = get_contract(
            extra_reward_token_address, blockchain, web3=web3, abi=ABI_EXTRA_REWARDS_TOKEN
        )

        base_token = call_contract_method(extra_reward_token_contract.functions.baseToken(), block)
        if base_token is not None:
            extra_reward_token_address = base_token

        extra_reward = extra_reward_contract.functions.earned(wallet).call(block_identifier=block)

        extra_rewards.append(
            [
                extra_reward_token_address,
                to_token_amount(extra_reward_token_address, extra_reward, blockchain, web3, decimals),
            ]
        )

    return extra_rewards


def get_extra_rewards_airdrop(wallet, block, blockchain, web3=None, decimals=True):
    extra_rewards_airdrop = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    extra_rewards_distributor = get_contract(
        EXTRA_REWARDS_DISTRIBUTOR, blockchain, web3=web3, abi=ABI_EXTRA_REWARDS_DISTRIBUTOR
    )

    extra_reward = extra_rewards_distributor.functions.claimableRewards(wallet, EthereumTokenAddr.AURA).call(
        block_identifier=block
    )

    if extra_reward > 0:
        extra_rewards_airdrop = [
            EthereumTokenAddr.AURA,
            to_token_amount(EthereumTokenAddr.AURA, extra_reward, blockchain, web3, decimals),
        ]

    return extra_rewards_airdrop


def get_aura_mint_amount(web3, bal_earned, block, blockchain, rewarder, decimals=True):
    """Check the amount of Aura retrieved"""
    aura_amount = 0

    if blockchain == Chain.ETHEREUM:
        aura_address = EthereumTokenAddr.AURA

        booster_contract = get_contract(BOOSTER, blockchain, web3=web3, abi=ABI_BOOSTER)
        reward_multiplier = booster_contract.functions.getRewardMultipliers(rewarder).call(block_identifier=block)
        REWARD_MULTIPLIER_DENOMINATOR = booster_contract.functions.REWARD_MULTIPLIER_DENOMINATOR().call(
            block_identifier=block
        )

        bal_earned = bal_earned * reward_multiplier / REWARD_MULTIPLIER_DENOMINATOR

        aura_contract = get_contract(aura_address, blockchain, web3=web3, abi=ABI_AURA)

        aura_total_supply = aura_contract.functions.totalSupply().call(block_identifier=block)
        init_mint_amount = aura_contract.functions.INIT_MINT_AMOUNT().call(block_identifier=block)
        reduction_per_cliff = aura_contract.functions.reductionPerCliff().call(block_identifier=block)

        emissions_minted = aura_total_supply - init_mint_amount
        cliff = int(emissions_minted / Decimal(reduction_per_cliff))

        total_cliffs = aura_contract.functions.totalCliffs().call(block_identifier=block)

        if cliff < total_cliffs:
            reduction = int(((total_cliffs - cliff) * Decimal(2.5)) + 700)

            aura_amount = (bal_earned * reduction) / total_cliffs

            amount_till_max = (
                Decimal(aura_contract.functions.EMISSIONS_MAX_SUPPLY().call(block_identifier=block)) - emissions_minted
            )

            if aura_amount > amount_till_max:
                aura_amount = amount_till_max

    else:
        booster_contract = get_contract(BOOSTER_LITE, blockchain, web3=web3, abi=ABI_BOOSTER)
        minter_address = const_call(booster_contract.functions.minter())
        minter_contract = get_contract(minter_address, blockchain, web3=web3, abi=ABI_L2COORDINATOR)
        aura_address = const_call(minter_contract.functions.auraOFT())
        aura_amount = bal_earned * (
            minter_contract.functions.mintRate().call(block_identifier=block) / Decimal(10**18)
        )

    if not decimals:
        aura_decimals = get_decimals(aura_address, blockchain, web3=web3)
        aura_amount = aura_amount * Decimal(10**aura_decimals)

    return [aura_address, aura_amount]


def get_all_rewards(wallet, lptoken_address, block, blockchain, web3=None, decimals=True, rewarders=[]):
    all_rewards = {}

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if rewarders == []:
        if blockchain == Chain.ETHEREUM:
            booster_address = BOOSTER
        else:
            booster_address = BOOSTER_LITE

        booster_contract = get_contract(booster_address, blockchain, web3=web3, abi=ABI_BOOSTER)
        rewarders = get_pool_rewarders(booster_contract, lptoken_address, blockchain, block)

    for rewarder in rewarders:
        rewarder_contract = get_contract(rewarder, blockchain, web3=web3, abi=ABI_REWARDER)

        bal_rewards = get_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=decimals)
        if bal_rewards[0] in all_rewards.keys():
            all_rewards[bal_rewards[0]] += bal_rewards[1]
        else:
            all_rewards[bal_rewards[0]] = bal_rewards[1]

        # bal_rewards[1] = bal_rewards_amount - aura_mint_amount is calculated using the bal_rewards_amount
        if bal_rewards[1] >= 0:
            aura_mint_amount = get_aura_mint_amount(
                web3, bal_rewards[1], block, blockchain, rewarder, decimals=decimals
            )

            if len(aura_mint_amount) > 0:
                if aura_mint_amount[0] in all_rewards.keys():
                    all_rewards[aura_mint_amount[0]] += aura_mint_amount[1]
                else:
                    all_rewards[aura_mint_amount[0]] = aura_mint_amount[1]

        extra_rewards = get_extra_rewards(web3, rewarder_contract, wallet, block, blockchain, decimals=decimals)

        if len(extra_rewards) > 0:
            for extra_reward in extra_rewards:
                if extra_reward[0] in all_rewards.keys():
                    all_rewards[extra_reward[0]] += extra_reward[1]
                else:
                    all_rewards[extra_reward[0]] = extra_reward[1]

    return all_rewards


def get_locked(wallet, block, blockchain, web3=None, reward=False, decimals=True):
    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    aura_locker_contract = get_contract(AURA_LOCKER, blockchain, web3=web3, abi=ABI_AURA_LOCKER)

    aura_locker = aura_locker_contract.functions.balances(wallet).call(block_identifier=block)[0]

    result = [
        [EthereumTokenAddr.AURA, to_token_amount(EthereumTokenAddr.AURA, aura_locker, blockchain, web3, decimals)]
    ]

    if reward is True:
        rewards = []
        aura_locker_rewards = aura_locker_contract.functions.claimableRewards(wallet).call(block_identifier=block)
        if aura_locker_rewards:
            for token, balance in aura_locker_rewards:
                rewards.append([token, to_token_amount(token, balance, blockchain, web3, decimals)])

        result += rewards

    return result


def get_staked(wallet, block, blockchain, web3=None, reward=False, decimals=True):
    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    aurabal_rewarder_contract = get_contract(AURABAL_REWARDER, blockchain, web3=web3, abi=ABI_REWARDER)
    aurabal_address = const_call(aurabal_rewarder_contract.functions.stakingToken())
    aurabal_staked = aurabal_rewarder_contract.functions.balanceOf(wallet).call(block_identifier=block)

    result = [[aurabal_address, to_token_amount(aurabal_address, aurabal_staked, blockchain, web3, decimals)]]

    if reward is True:
        rewards = [get_rewards(web3, aurabal_rewarder_contract, wallet, block, blockchain, decimals=decimals)]

        # Extra Rewards
        extra_rewards = get_extra_rewards(web3, aurabal_rewarder_contract, wallet, block, blockchain, decimals=decimals)
        for n in range(0, len(extra_rewards)):
            rewards.append(extra_rewards[n])

        # AURA Rewards
        if rewards[0][1] > 0:
            rewards.append(
                get_aura_mint_amount(web3, rewards[0][1], block, blockchain, AURABAL_REWARDER, decimals=decimals)
            )

        result += rewards

    return result


def get_compounded(wallet, block, blockchain, web3=None, reward=False, decimals=True):
    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    stk_aurabal_contract = get_contract(stkauraBAL, blockchain, web3=web3, abi=ABI_STKAURABAL)
    aurabal_address = const_call(stk_aurabal_contract.functions.underlying())
    aurabal_staked = stk_aurabal_contract.functions.balanceOfUnderlying(wallet).call(block_identifier=block)

    result = [[aurabal_address, to_token_amount(aurabal_address, aurabal_staked, blockchain, web3, decimals)]]

    if reward is True:
        rewards = []
        # Extra Rewards
        extra_rewards = get_extra_rewards(web3, stk_aurabal_contract, wallet, block, blockchain, decimals=decimals)
        for n in range(0, len(extra_rewards)):
            rewards.append(extra_rewards[n])

        result += rewards

    return result


def underlying(
    wallet, lptoken_address, block, blockchain, web3=None, reward=False, return_balancer_underlying=False, decimals=True
):
    result = {}
    balances = {}

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    lptoken_address = Web3.to_checksum_address(lptoken_address)

    if blockchain == Chain.ETHEREUM:
        booster_address = BOOSTER
    else:
        booster_address = BOOSTER_LITE

    booster_contract = get_contract(booster_address, blockchain, web3=web3, abi=ABI_BOOSTER)

    rewarders = get_pool_rewarders(booster_contract, lptoken_address, blockchain, block)

    for rewarder in rewarders:
        rewarder_contract = get_contract(rewarder, blockchain, web3=web3, abi=ABI_REWARDER)
        lptoken_staked = Decimal(rewarder_contract.functions.balanceOf(wallet).call(block_identifier=block))
        lptoken_decimals = get_decimals(lptoken_address, blockchain, web3=web3)
        amount = lptoken_staked / Decimal(10**lptoken_decimals if decimals else 1)
        if not decimals:
            amount /= 10**lptoken_decimals

        if not return_balancer_underlying:
            unwrapped_tokens = balancer.unwrap(blockchain, lptoken_address, amount, block, decimals)
            for token_addr, token_balance in unwrapped_tokens.items():
                balances[token_addr] = balances.get(token_addr, 0) + token_balance
        else:
            balances[lptoken_address] = amount

    result["balances"] = balances

    if reward and rewarders != []:
        all_rewards = get_all_rewards(
            wallet, lptoken_address, block, blockchain, web3=web3, decimals=decimals, rewarders=rewarders
        )

        result["rewards"] = all_rewards

    return result


def pool_balances(blockchain: str, lp_address: str, block: int | str, decimals: bool = True) -> None:
    return balancer.pool_balances(blockchain, lp_address, block, decimals=decimals)


def update_db(output_file=DB_FILE, block="latest"):
    db_data = {}

    for blockchain in [Chain.GNOSIS, Chain.ETHEREUM, Chain.POLYGON, Chain.ARBITRUM, Chain.OPTIMISM]:
        db_data[blockchain] = {}

        web3 = get_node(blockchain)

        if blockchain == Chain.ETHEREUM:
            booster_address = BOOSTER
        else:
            booster_address = BOOSTER_LITE

        booster = get_contract(booster_address, blockchain, web3=web3, abi=ABI_BOOSTER)
        pools_length = booster.functions.poolLength().call(block_identifier=block)
        rewarder_pool_created_event = web3.keccak(text=REWARD_POOL_CREATED_EVENT_SIGNATURE).hex()

        # rewarder_factory_address = const_call(booster.functions.rewardFactory()) -> IMPORTANT: This only works if the rewarder factory never changes
        # This solution considers that in the future Aura could deploy a new rewarder factory
        for addr, block_start in REWARDER_FACTORIES[blockchain].items():
            rewarder_logs = get_logs_web3(
                blockchain=blockchain,
                address=addr,
                block_start=block_start,
                topics=[rewarder_pool_created_event],
            )

        for i in range(pools_length):
            pool_info = booster.functions.poolInfo(i).call(block_identifier=block)  # can't be const_call!

            for rewarder_log in rewarder_logs:
                # For some endpoints rewarder_log["data"] is a string and for others is a bytes object
                data = rewarder_log["data"].hex() if isinstance(rewarder_log["data"], bytes) else rewarder_log["data"]
                if data[26:66] == pool_info[3][2:].lower():
                    rewarder_creation_tx = web3.eth.get_transaction(rewarder_log["transactionHash"])

                    if pool_info[0] in db_data[blockchain].keys():
                        db_data[blockchain][pool_info[0]][rewarder_creation_tx["blockNumber"]] = {
                            "poolId": i,
                            "rewarder": pool_info[3],
                        }
                    else:
                        db_data[blockchain][pool_info[0]] = {
                            rewarder_creation_tx["blockNumber"]: {"poolId": i, "rewarder": pool_info[3]}
                        }

    with open(output_file, "w") as db_file:
        json.dump(db_data, db_file, indent=2)

    return db_data
