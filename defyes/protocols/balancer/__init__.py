from contextlib import suppress
from datetime import datetime, timedelta
from decimal import Decimal
from functools import cached_property

from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.constants import ZERO_ADDRESS, ETHTokenAddr
from defyes.functions import block_to_date, date_to_block, get_logs_web3, last_block, to_token_amount, get_symbol
from defyes.helpers import suppress_error_codes
from defyes.node import get_node
from defyes.prices.prices import get_price

from .autogenerated import (
    Gauge,
    GaugeFactory,
    GaugeRewardHelper,
    LiquidityPool,
    PoolToken,
    Vault,
    Vebal,
    VebalFeeDistributor,
)

# First block in every blockchain
START_BLOCK = {
    "ethereum": 14457664,
    "polygon": 40687417,
    "arbitrum": 72942741,
    "xdai": 27088528,
}


class Vault(Vault):
    ADDR: str = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
    default_addresses: dict[str, str] = {"ethereum": ADDR, "polygon": ADDR, "xdai": ADDR, "arbitrum": ADDR}

    def get_pool_data(self, pool_id: int) -> list:
        tokens = []
        pool_data = self.get_pool_tokens(pool_id)
        for token, balance in zip(pool_data[0], pool_data[1]):
            tokens.append((token, balance))

        return tokens


class PoolToken(PoolToken):
    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        super().__init__(blockchain, block, address)
        self.is_wsteth = False

    @property
    def rate(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return self.get_rate

    @property
    def underlying(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return super().underlying

    @property
    def underlying_asset_address(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return super().underlying_asset_address

    @property
    def steth(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return self.st_eth

    def get_token_addr_steth(self, scaling_factor) -> str:
        main_token = self.underlying
        if scaling_factor:
            main_token = self.underlying_asset_address
            if main_token is None:
                main_token = self.address
                stETH = self.steth
                if stETH is not None:
                    if scaling_factor != 10**18:
                        main_token = stETH
                    else:
                        main_token = self.address
                else:
                    main_token = self.address

        return main_token

    def get_token_addr_wsteth(self) -> str:
        self.is_wsteth = False
        main_token = self.underlying
        if main_token is None:
            main_token = self.underlying_asset_address
            if main_token is None:
                main_token = self.address
                main_token_symbol = get_symbol(main_token, self.blockchain, web3=self.contract.w3).lower()
                self.is_wsteth = (main_token_symbol == "wsteth")

        return main_token

    def calc_amount(self, token_amount: int, decimals: bool = True, scaling_factor: int = None) -> Decimal:
        token_amount = Decimal(token_amount)
        if scaling_factor and not self.is_wsteth:
            # uncomment to have stETH being returned instead of wstETH
            # if scaling_factor:
            token_amount = token_amount * Decimal(scaling_factor) / Decimal(10 ** (2 * 18 - self.decimals))
        if decimals:
            token_amount = token_amount / Decimal(10**self.decimals)
        return token_amount


class LiquidityPool(LiquidityPool):
    @cached_property
    def poolid(self):
        try:
            return self.get_pool_id
        except ContractLogicError:
            return self.pool_id

    @cached_property
    def bpt_index(self) -> int | None:
        with suppress(ContractLogicError), suppress_error_codes():
            return self.get_bpt_index

    @cached_property
    def supply(self) -> int:
        """
        Return the first valid attribure: get_actual_supply or get_virtual_supply, otherwise total_supply.
        """
        for attr in ("get_actual_supply", "get_virtual_supply"):
            with suppress(ContractLogicError), suppress_error_codes():
                return getattr(self, attr)
        return self.total_supply

    @cached_property
    def scaling_factors(self) -> int | None:
        with suppress(ContractLogicError):
            return self.get_scaling_factors

    def balance_of(self, wallet: str) -> int:
        wallet = Web3.to_checksum_address(wallet)
        return super().balance_of(wallet)

    def swap_fee_percentage_for(self, block: int | str) -> int:
        return self.contract.functions.getSwapFeePercentage().call(block_identifier=block)

    def swap_fees(self, vault_address: str, block_start: int, decimals: bool = True) -> list[dict]:
        node = self.contract.w3
        pool_id = "0x" + self.poolid.hex()
        swap_event = node.keccak(text="Swap(bytes32,address,address,uint256,uint256)").hex()

        if block_start < START_BLOCK[self.blockchain]:
            block_start = START_BLOCK[self.blockchain]

        swap_logs = get_logs_web3(
            address=vault_address,
            blockchain=self.blockchain,
            block_start=block_start,
            block_end=self.block,
            topics=[swap_event, pool_id],
            web3=node,
        )

        swaps = []
        for swap_log in swap_logs:
            token_in = Web3.to_checksum_address(f"0x{swap_log['topics'][2].hex()[-40:]}")
            swap_fee = Decimal(self.swap_fee_percentage_for(swap_log["blockNumber"]))
            swap_fee /= Decimal(10**self.decimals)
            swap_fee *= int(swap_log["data"].hex()[2:66], 16)

            swap_data = {
                "block": swap_log["blockNumber"],
                "token_in": token_in,
                "amount_in": to_token_amount(token_in, swap_fee, self.blockchain, node, decimals),
            }

            swaps.append(swap_data)

        return swaps

    def calc_balance(self, wallet: str, decimals: bool = True) -> Decimal:
        token_amount = Decimal(self.balance_of(wallet))
        if decimals:
            token_amount = token_amount / Decimal(10**self.decimals)
        return token_amount


def get_gauge_addresses(blockchain: str, block: int | str, lp_address: str) -> list:
    ADDRS: dict[str, str] = {
        "ethereum": [(15399251, "0xf1665E19bc105BE4EDD3739F88315cC699cc5b65"),
                     (14457664, "0x4E7bBd911cf1EFa442BC1b2e9Ea01ffE785412EC")],
        "polygon": [(40687417, "0x22625eEDd92c81a219A83e1dc48f88d54786B017"),
                    (27098624, "0x3b8cA519122CdD8efb272b0D3085453404B25bD0")],
        "arbitrum": [(72942741, "0x6817149cb753BF529565B4D023d7507eD2ff4Bc0"),
                     (9756975, "0xb08E16cFc07C684dAA2f93C70323BAdb2A6CBFd2")],
        "xdai": [(27088528, "0x83E443EF4f9963C77bd860f94500075556668cb8"),
                 (26615210, "0x809B79b53F18E9bc08A961ED4678B901aC93213a")],
        "optimism": [(641824, "0x83E443EF4f9963C77bd860f94500075556668cb8"),
                     (60740, "0x2E96068b3D5B5BAE3D7515da4A1D2E52d08A2647")]
    }

    if block == "latest":
        block = last_block(blockchain)

    gauge_addresses = []
    for n, (blk, addr) in enumerate(ADDRS[blockchain], start=1):
        gauge_address = ZERO_ADDRESS
        if block > blk:
            gauge_factory = GaugeFactory(blockchain, block, addr)
            if n == len(ADDRS[blockchain]):
                with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
                    gauge_address = gauge_factory.get_pool_gauge(lp_address)
                if gauge_address != ZERO_ADDRESS:
                    gauge_addresses.append(gauge_address)
            else:
                gauge_created_event = Web3.keccak(text="GaugeCreated(address)").hex()
                logs = get_logs_web3(
                    address=gauge_factory.address,
                    blockchain=blockchain,
                    block_start=blk,
                    block_end=block,
                    topics=[gauge_created_event],
                    web3=gauge_factory.contract.w3,
                )
                for log in logs:
                    tx = gauge_factory.contract.w3.eth.get_transaction(log["transactionHash"])
                    if lp_address[2 : len(lp_address)].lower() in tx["input"]:
                        gauge_address = Web3.to_checksum_address(f"0x{log['topics'][1].hex()[-40:]}")
                        break
                if gauge_address == ZERO_ADDRESS:
                    continue
                else:
                    gauge_addresses.append(gauge_address)

    return gauge_addresses


class Gauge(Gauge):
    BAL_ADDRS: dict = {
        "ethereum": "0xba100000625a3754423978a60c9317c58a424e3D",
        "polygon": "0x9a71012B13CA4d3D0Cdc72A177DF3ef03b0E76A3",
        "arbitrum": "0x040d1EdC9569d4Bab2D15287Dc5A4F10F56a56B8",
        "xdai": "0x7eF541E2a22058048904fE5744f9c7E4C57AF717",
    }

    @property
    def decimals(self):
        return 18 if self.address == ZERO_ADDRESS else super().decimals

    def balance_of(self, wallet: str) -> Decimal:
        wallet = Web3.to_checksum_address(wallet)
        if self.address == ZERO_ADDRESS:
            return Decimal(self.contract.w3.eth.get_balance(wallet, self.block))
        else:
            with suppress(ContractLogicError):
                return super().balance_of(wallet)
        return Decimal(0)

    @property
    def reward_count(self):
        count = 0
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            count = super().reward_count
        return count

    def get_rewards(self, wallet: str, decimals: bool = True) -> dict:
        rewards = {}
        if self.address != ZERO_ADDRESS:
            wallet = Web3.to_checksum_address(wallet)

            # BAL rewards
            bal_decimals = Decimal(10**18) if decimals else 1
            with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
                rewards = {self.BAL_ADDRS[self.blockchain]: self.claimable_tokens(wallet) / bal_decimals}
            if not rewards:
                with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
                    rewards = {self.BAL_ADDRS[self.blockchain]: self.claimable_reward(wallet, self.BAL_ADDRS[self.blockchain]) / bal_decimals}

            tokens = [self.reward_tokens(n) for n in range(self.reward_count)]
            for token_address in tokens:
                if self.blockchain == "ethereum":
                    token_reward = self.claimable_reward(wallet, token_address)
                else:
                    token_reward = GaugeRewardHelper(self.blockchain, self.block).get_rewards(
                        self.address, wallet, token_address
                    )

                rewards[token_address] = to_token_amount(
                    token_address, token_reward, self.blockchain, self.contract.w3, decimals
                )

        return rewards

    def calc_balance(self, wallet: str, decimals: bool = True) -> Decimal:
        token_amount = Decimal(self.balance_of(wallet))
        if decimals:
            token_amount = token_amount / Decimal(10**self.decimals)
        return token_amount


class GaugeRewardHelper(GaugeRewardHelper):
    default_addresses: dict[str, str] = {
        "xdai": "0xf7D5DcE55E6D47852F054697BAB6A1B48A00ddbd",
        "polygon": "0xaEb406b0E430BF5Ea2Dc0B9Fe62E4E53f74B3a33",
        "arbitrum": "0xA0DAbEBAAd1b243BBb243f933013d560819eB66f",
    }

    def get_rewards(self, gauge_address: str, wallet: str, token_address: str) -> Decimal:
        gauge_address = Web3.to_checksum_address(gauge_address)
        wallet = Web3.to_checksum_address(wallet)
        token_address = Web3.to_checksum_address(token_address)
        return self.get_pending_rewards(gauge_address, wallet, token_address)


class Vebal(Vebal):
    default_addresses: dict[str, str] = {"ethereum": "0xC128a9954e6c874eA3d62ce62B468bA073093F25"}

    def balance_of(self, wallet: str, token_address: str) -> Decimal:
        wallet = Web3.to_checksum_address(wallet)
        if token_address == self.token:
            with suppress(ContractLogicError):
                return Decimal(self.locked(wallet)[0])
        return Decimal(0)

    def calc_balance(self, wallet: str, token_address: str, decimals: bool = True) -> Decimal:
        token_amount = Decimal(self.balance_of(wallet, token_address))
        if decimals:
            token_amount = token_amount / Decimal(10**18)
        return token_amount


def get_vebal_rewards(wallet: str, blockchain: str, block: str | int, decimals: bool = True) -> dict:
    ADDRS: list = [(15149500, "0xD3cf852898b21fc233251427c2DC93d3d604F3BB"),
                   (14623899, "0x26743984e3357eFC59f2fd6C1aFDC310335a61c9")]

    REWARD_TOKENS: list = [(16981440, [ETHTokenAddr.BAL, ETHTokenAddr.BB_A_USD_OLD, ETHTokenAddr.BB_A_USD, ETHTokenAddr.BB_A_USD_V3]),
                           (14623899, [ETHTokenAddr.BAL, ETHTokenAddr.BB_A_USD_OLD, ETHTokenAddr.BB_A_USD])]

    rewards = {ETHTokenAddr.BAL: 0, ETHTokenAddr.BB_A_USD_OLD: 0, ETHTokenAddr.BB_A_USD: 0, ETHTokenAddr.BB_A_USD_V3: 0}

    if isinstance(block, str) and block == "latest":
        block = last_block(blockchain)

    if block >= ADDRS[-1][0]:
        for blk, addr in ADDRS:
            if block >= blk:
                for reward_block, reward_list in REWARD_TOKENS:
                    if block >= reward_block:
                        reward_tokens = reward_list
                        break

                balances = VebalFeeDistributor(blockchain, block, addr).claim_tokens(wallet, reward_list)
                for reward_token, balance in zip(reward_list, balances):
                    balance = balance / Decimal(10**18) if decimals else Decimal(balance)
                    rewards[reward_token] = rewards.get(reward_token, 0) + balance

    return rewards

def unwrap(blockchain: str, lp_address: str, amount: Decimal, block: int | str, decimals: bool = True) -> None:
    lp = LiquidityPool(blockchain, block, lp_address)
    pool_tokens = Vault(blockchain, block).get_pool_data(lp.poolid)
    pool_balance_fraction = Decimal(amount) * Decimal(10**lp.decimals) / Decimal(lp.supply)
    balances = {}
    for n, (token_addr, balance) in enumerate(pool_tokens):
        if n == lp.bpt_index:
            continue

        token = PoolToken(blockchain, block, token_addr)
        if token.rate is not None:
            for token_addr, token_balance in unwrap(
                blockchain, token.address, token.calc_amount(balance, decimals), block
            ).items():
                balances[token_addr] = balances.get(token_addr, 0) + token_balance * pool_balance_fraction
        else:
            scaling_factor = None if lp.scaling_factors is None else lp.scaling_factors[n]
            token_addr = token.get_token_addr_wsteth()
            token_balance = token.calc_amount(balance, decimals, scaling_factor)

            balances[token_addr] = balances.get(token_addr, 0) + token_balance * pool_balance_fraction
    return balances


def pool_balances(blockchain: str, lp_address: str, block: int | str, decimals: bool = True) -> None:
    lp = LiquidityPool(blockchain, block, lp_address)
    pool_tokens = Vault(blockchain, block).get_pool_data(lp.poolid)
    balances = {}
    for n, (token_addr, balance) in enumerate(pool_tokens):
        if n == lp.bpt_index:
            continue

        token = PoolToken(blockchain, block, token_addr)
        if token.rate is not None:
            for token_addr, token_balance in unwrap(
                blockchain, token.address, token.calc_amount(balance, decimals), block
            ).items():
                balances[token_addr] = balances.get(token_addr, 0) + token_balance
        else:
            scaling_factor = None if lp.scaling_factors is None else lp.scaling_factors[n]
            token_addr = token.get_token_addr_wsteth()
            token_balance = token.calc_amount(balance, decimals, scaling_factor)

            balances[token_addr] = balances.get(token_addr, 0) + token_balance
    return balances


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    lp_addrs: str | list,
    block: int | str = "latest",
    reward: bool = False,
    decimals: bool = True,
    aura_staked: Decimal = None,
) -> None:
    if isinstance(lp_addrs, str):
        lp_addrs = [lp_addrs]

    positions = {}
    for lp_address in lp_addrs:
        lp_address = Web3.to_checksum_address(lp_address)
        positions[lp_address] = {"liquidity": {}, "staked": {}, "locked": {}, "financial_metrics": {}}
        gauge_addresses = get_gauge_addresses(blockchain, block, lp_address)
        lp = LiquidityPool(blockchain, block, lp_address)

        lp_balance = lp.balance_of(wallet)
        pool_balance_fraction = lp_balance / Decimal(lp.supply)
        if lp_balance:
            positions[lp_address]["liquidity"] = {
                "holdings": [{"address": lp_address, "balance": lp.calc_balance(wallet, decimals)}]
            }

        pool_staked_fraction = 0
        total_staked_balance = 0
        for addr in gauge_addresses:
            gauge = Gauge(blockchain, block, addr)
            lp_balance_staked = gauge.balance_of(wallet)
            pool_staked_fraction += lp_balance_staked / Decimal(lp.supply)
            total_staked_balance += lp_balance_staked / Decimal(10**gauge.decimals if decimals else 1)

        if total_staked_balance:
            positions[lp_address]["staked"] = {
                "holdings": [{"address": lp_address, "balance": total_staked_balance}]
            }

        if blockchain == "ethereum":
            vebal = Vebal(blockchain, block)
            lp_balance_locked = vebal.balance_of(wallet, lp.address)
            pool_locked_fraction = lp_balance_locked / Decimal(lp.supply)
            if lp_balance_locked:
                positions[lp_address]["locked"] = {
                    "holdings": [{"address": lp_address, "balance": vebal.calc_balance(wallet, lp_address, decimals)}]
                }
        else:
            pool_locked_fraction = Decimal(0)

        balances = pool_balances(blockchain, lp_address, block, decimals)
        for addr, amount in balances.items():
            balance = amount * pool_balance_fraction
            if balance:
                positions[lp_address]["liquidity"]["underlyings"] = positions[lp_address]["liquidity"].get(
                    "underlyings", []
                )
                positions[lp_address]["liquidity"]["underlyings"].append({"address": addr, "balance": balance})

            if aura_staked is None:
                balance_staked = amount * pool_staked_fraction
            else:
                aura_pool_fraction = aura_staked / Decimal(lp.supply)
                balance_staked = amount * aura_pool_fraction
            if balance_staked:
                positions[lp_address]["staked"]["underlyings"] = positions[lp_address]["staked"].get("underlyings", [])
                positions[lp_address]["staked"]["underlyings"].append({"address": addr, "balance": balance_staked})

            balance_locked = amount * pool_locked_fraction
            if balance_locked:
                positions[lp_address]["locked"]["underlyings"] = positions[lp_address]["locked"].get("underlyings", [])
                positions[lp_address]["locked"]["underlyings"].append({"address": addr, "balance": balance_locked})

        if reward:
            total_rewards = {}
            for addr in gauge_addresses:
                gauge = Gauge(blockchain, block, addr)
                rewards = gauge.get_rewards(wallet)
                for addr, reward_balance in rewards.items():
                    total_rewards[addr] = total_rewards.get(addr, 0) + reward_balance
            for addr, reward_balance in total_rewards.items():
                if reward_balance:
                    positions[lp_address]["staked"]["unclaimed_rewards"] = positions[lp_address]["staked"].get(
                        "unclaimed_rewards", []
                    )
                    positions[lp_address]["staked"]["unclaimed_rewards"].append({"address": addr, "balance": reward_balance})

            if blockchain == "ethereum":
                vebal_rewards = get_vebal_rewards(wallet, blockchain, block, decimals)
                for addr, reward_balance in vebal_rewards.items():
                    if reward_balance:
                        positions[lp_address]["locked"]["unclaimed_rewards"] = positions[lp_address]["locked"].get(
                            "unclaimed_rewards", []
                        )
                        positions[lp_address]["locked"]["unclaimed_rewards"].append(
                            {"address": addr, "balance": reward_balance}
                        )

    return {
        "protocol": "Balancer",
        "blockchain": blockchain,
        "block": block,
        "positions": positions,
        "positions_key": "liquidity_pool_address",
        "version": 0,
    }


def get_swap_fees_apr(
    lptoken_address: str, blockchain: str, block: int | str = "latest", days: int = 1, apy: bool = False
) -> Decimal:
    block_start = date_to_block(
        datetime.strftime(
            datetime.strptime(block_to_date(block, blockchain), "%Y-%m-%d %H:%M:%S") - timedelta(days=days),
            "%Y-%m-%d %H:%M:%S",
        ),
        blockchain,
    )

    node = get_node(blockchain, block)
    vault_address = Vault(blockchain, block).address
    lp = LiquidityPool(blockchain, block, lptoken_address)
    swaps = lp.swap_fees(vault_address, block_start)

    # create a dictionary to store the total amountIn for each tokenIn
    totals = {}
    for swap in swaps:
        totals[swap["token_in"]] = totals.get(swap["token_in"], 0) + swap["amount_in"]

    fee = 0
    for token, amount in totals.items():
        fee += amount * Decimal(get_price(token, block, blockchain, node)[0])

    pool_balance = pool_balances(blockchain, lptoken_address, block)
    tvl = 0
    for token, balance in pool_balance.items():
        tvl += balance * Decimal(get_price(token, block, blockchain, node)[0])

    rate = Decimal(fee / tvl)
    apr = (((1 + rate) ** Decimal(365 / days) - 1) * 100) / 2
    seconds_per_year = 365 * 24 * 60 * 60
    if apy:
        return (1 + (apr / seconds_per_year)) ** seconds_per_year - 1
    else:
        return apr
