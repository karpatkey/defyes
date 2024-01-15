"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import Gauge, GaugeFactory, GaugeRewardHelper, LiquidityPool, PoolToken, Vault, Vebal, VebalFeeDistributor

# Optionally
class Gauge(Gauge):
    ...
"""
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class Gauge:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "gauge.json"))

    def claimable_tokens(self, addr: str) -> int:
        return self.contract.functions.claimable_tokens(addr).call(block_identifier=self.block)

    def claimed_reward(self, _addr: str, _token: str) -> int:
        return self.contract.functions.claimed_reward(_addr, _token).call(block_identifier=self.block)

    def claimable_reward(self, _user: str, _reward_token: str) -> int:
        return self.contract.functions.claimable_reward(_user, _reward_token).call(block_identifier=self.block)

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    def allowance(self, owner: str, spender: str) -> int:
        return self.contract.functions.allowance(owner, spender).call(block_identifier=self.block)

    @property
    def integrate_checkpoint(self) -> int:
        return self.contract.functions.integrate_checkpoint().call(block_identifier=self.block)

    @property
    def bal_token(self) -> str:
        return self.contract.functions.bal_token().call(block_identifier=self.block)

    @property
    def bal_pseudo_minter(self) -> str:
        return self.contract.functions.bal_pseudo_minter().call(block_identifier=self.block)

    @property
    def voting_escrow_delegation_proxy(self) -> str:
        return self.contract.functions.voting_escrow_delegation_proxy().call(block_identifier=self.block)

    @property
    def authorizer_adaptor(self) -> str:
        return self.contract.functions.authorizer_adaptor().call(block_identifier=self.block)

    @property
    def domain_separator(self) -> bytes:
        return self.contract.functions.DOMAIN_SEPARATOR().call(block_identifier=self.block)

    def nonces(self, arg0: str) -> int:
        return self.contract.functions.nonces(arg0).call(block_identifier=self.block)

    @property
    def name(self) -> str:
        return self.contract.functions.name().call(block_identifier=self.block)

    @property
    def symbol(self) -> str:
        return self.contract.functions.symbol().call(block_identifier=self.block)

    def balance_of(self, arg0: str) -> int:
        return self.contract.functions.balanceOf(arg0).call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)

    @property
    def lp_token(self) -> str:
        return self.contract.functions.lp_token().call(block_identifier=self.block)

    @property
    def version(self) -> str:
        return self.contract.functions.version().call(block_identifier=self.block)

    @property
    def factory(self) -> str:
        return self.contract.functions.factory().call(block_identifier=self.block)

    def working_balances(self, arg0: str) -> int:
        return self.contract.functions.working_balances(arg0).call(block_identifier=self.block)

    @property
    def working_supply(self) -> int:
        return self.contract.functions.working_supply().call(block_identifier=self.block)

    @property
    def period(self) -> int:
        return self.contract.functions.period().call(block_identifier=self.block)

    def period_timestamp(self, arg0: int) -> int:
        return self.contract.functions.period_timestamp(arg0).call(block_identifier=self.block)

    def integrate_checkpoint_of(self, arg0: str) -> int:
        return self.contract.functions.integrate_checkpoint_of(arg0).call(block_identifier=self.block)

    def integrate_fraction(self, arg0: str) -> int:
        return self.contract.functions.integrate_fraction(arg0).call(block_identifier=self.block)

    def integrate_inv_supply(self, arg0: int) -> int:
        return self.contract.functions.integrate_inv_supply(arg0).call(block_identifier=self.block)

    def integrate_inv_supply_of(self, arg0: str) -> int:
        return self.contract.functions.integrate_inv_supply_of(arg0).call(block_identifier=self.block)

    @property
    def reward_count(self) -> int:
        return self.contract.functions.reward_count().call(block_identifier=self.block)

    def reward_tokens(self, arg0: int) -> str:
        return self.contract.functions.reward_tokens(arg0).call(block_identifier=self.block)

    def reward_data(self, arg0: str) -> tuple:
        return self.contract.functions.reward_data(arg0).call(block_identifier=self.block)

    def rewards_receiver(self, arg0: str) -> str:
        return self.contract.functions.rewards_receiver(arg0).call(block_identifier=self.block)

    def reward_integral_for(self, arg0: str, arg1: str) -> int:
        return self.contract.functions.reward_integral_for(arg0, arg1).call(block_identifier=self.block)

    @property
    def is_killed(self) -> bool:
        return self.contract.functions.is_killed().call(block_identifier=self.block)

    def inflation_rate(self, arg0: int) -> int:
        return self.contract.functions.inflation_rate(arg0).call(block_identifier=self.block)


class GaugeFactory:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "gauge_factory.json"))

    def get_pool_gauge(self, pool: str) -> str:
        return const_call(self.contract.functions.getPoolGauge(pool))


class GaugeRewardHelper:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "gauge_reward_helper.json"))


class LiquidityPool:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "liquidity_pool.json"))

    @property
    def get_pool_id(self) -> bytes:
        return const_call(self.contract.functions.getPoolId())

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    @property
    def get_actual_supply(self) -> int:
        return self.contract.functions.getActualSupply().call(block_identifier=self.block)

    @property
    def get_virtual_supply(self) -> int:
        return self.contract.functions.getVirtualSupply().call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)

    @property
    def get_bpt_index(self) -> int:
        return const_call(self.contract.functions.getBptIndex())

    def balance_of(self, account: str) -> int:
        return self.contract.functions.balanceOf(account).call(block_identifier=self.block)

    @property
    def get_swap_fee_percentage(self) -> int:
        return self.contract.functions.getSwapFeePercentage().call(block_identifier=self.block)

    @property
    def get_rate(self) -> int:
        return self.contract.functions.getRate().call(block_identifier=self.block)

    @property
    def get_scaling_factors(self) -> list[int]:
        return self.contract.functions.getScalingFactors().call(block_identifier=self.block)

    @property
    def pool_id(self) -> bytes:
        return const_call(self.contract.functions.POOL_ID())

    @property
    def in_recovery_mode(self) -> bool:
        return self.contract.functions.inRecoveryMode().call(block_identifier=self.block)

    @property
    def version(self) -> str:
        return self.contract.functions.version().call(block_identifier=self.block)

    @property
    def get_main_token(self) -> str:
        return self.contract.functions.getMainToken().call(block_identifier=self.block)

    @property
    def get_wrapped_token(self) -> str:
        return self.contract.functions.getWrappedToken().call(block_identifier=self.block)

    @property
    def get_wrapped_token_rate(self) -> int:
        return self.contract.functions.getWrappedTokenRate().call(block_identifier=self.block)

    @property
    def get_main_index(self) -> int:
        return self.contract.functions.getMainIndex().call(block_identifier=self.block)

    @property
    def get_wrapped_index(self) -> int:
        return self.contract.functions.getWrappedIndex().call(block_identifier=self.block)


class PoolToken:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "pool_token.json"))

    @property
    def decimals(self) -> int:
        return const_call(self.contract.functions.decimals())

    @property
    def get_rate(self) -> int:
        return self.contract.functions.getRate().call(block_identifier=self.block)

    @property
    def get_main_token(self) -> str:
        return self.contract.functions.getMainToken().call(block_identifier=self.block)

    @property
    def underlying_asset_address(self) -> str:
        return self.contract.functions.UNDERLYING_ASSET_ADDRESS().call(block_identifier=self.block)

    @property
    def rate(self) -> int:
        return self.contract.functions.rate().call(block_identifier=self.block)

    @property
    def st_eth(self) -> str:
        return self.contract.functions.stETH().call(block_identifier=self.block)

    @property
    def underlying(self) -> str:
        return self.contract.functions.UNDERLYING().call(block_identifier=self.block)

    @property
    def get_pool_id(self) -> bytes:
        return self.contract.functions.getPoolId().call(block_identifier=self.block)

    def preview_redeem(self, shares: int) -> int:
        return self.contract.functions.previewRedeem(shares).call(block_identifier=self.block)


class Vault:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "vault.json"))

    @property
    def weth(self) -> str:
        return self.contract.functions.WETH().call(block_identifier=self.block)

    def batch_swap(
        self, kind: int, swaps: list[tuple], assets: list[str], funds: tuple, limits: list[int], deadline: int
    ) -> list[int]:
        return self.contract.functions.batchSwap(kind, swaps, assets, funds, limits, deadline).call(
            block_identifier=self.block
        )

    def get_action_id(self, selector: bytes) -> bytes:
        return self.contract.functions.getActionId(selector).call(block_identifier=self.block)

    @property
    def get_authorizer(self) -> str:
        return self.contract.functions.getAuthorizer().call(block_identifier=self.block)

    @property
    def get_domain_separator(self) -> bytes:
        return self.contract.functions.getDomainSeparator().call(block_identifier=self.block)

    def get_internal_balance(self, user: str, tokens: list[str]) -> list[int]:
        return self.contract.functions.getInternalBalance(user, tokens).call(block_identifier=self.block)

    def get_next_nonce(self, user: str) -> int:
        return self.contract.functions.getNextNonce(user).call(block_identifier=self.block)

    @property
    def get_paused_state(self) -> tuple[bool, int, int]:
        """
        Output: paused, pauseWindowEndTime, bufferPeriodEndTime
        """
        return self.contract.functions.getPausedState().call(block_identifier=self.block)

    def get_pool(self, pool_id: bytes) -> tuple[str, int]:
        """
        Output: ,
        """
        return self.contract.functions.getPool(pool_id).call(block_identifier=self.block)

    def get_pool_token_info(self, pool_id: bytes, token: str) -> tuple[int, int, int, str]:
        """
        Output: cash, managed, lastChangeBlock, assetManager
        """
        return self.contract.functions.getPoolTokenInfo(pool_id, token).call(block_identifier=self.block)

    def get_pool_tokens(self, pool_id: bytes) -> tuple[list[str], list[int], int]:
        """
        Output: tokens, balances, lastChangeBlock
        """
        return self.contract.functions.getPoolTokens(pool_id).call(block_identifier=self.block)

    @property
    def get_protocol_fees_collector(self) -> str:
        return self.contract.functions.getProtocolFeesCollector().call(block_identifier=self.block)

    def has_approved_relayer(self, user: str, relayer: str) -> bool:
        return self.contract.functions.hasApprovedRelayer(user, relayer).call(block_identifier=self.block)

    def join_pool(self, pool_id: bytes, sender: str, recipient: str, request: tuple):
        return self.contract.functions.joinPool(pool_id, sender, recipient, request).call(block_identifier=self.block)

    def manage_user_balance(self, ops: list[tuple]):
        return self.contract.functions.manageUserBalance(ops).call(block_identifier=self.block)

    def swap(self, single_swap: tuple, funds: tuple, limit: int, deadline: int) -> int:
        return self.contract.functions.swap(single_swap, funds, limit, deadline).call(block_identifier=self.block)


class Vebal:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "vebal.json"))

    @property
    def token(self) -> str:
        return const_call(self.contract.functions.token())

    def locked(self, arg0: str) -> tuple:
        return self.contract.functions.locked(arg0).call(block_identifier=self.block)


class VebalFeeDistributor:
    default_addresses: dict[str, str]

    def __init__(self, blockchain: str, block: int, address: str | None = None) -> None:
        self.block = block
        self.blockchain = blockchain
        if address:
            self.address = Web3.to_checksum_address(address)
        else:
            try:
                self.address = self.default_addresses[blockchain]
            except AttributeError as e:
                raise ValueError("No default_addresses defined when trying to guess the address.") from e
            except KeyError as e:
                raise ValueError(
                    f"{blockchain!r} not defined in default_addresses when trying to guess the address."
                ) from e
        node = get_node(blockchain)
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "vebal_fee_distributor.json"))

    def claim_tokens(self, user: str, tokens: list[str]) -> list[int]:
        return self.contract.functions.claimTokens(user, tokens).call(block_identifier=self.block)
