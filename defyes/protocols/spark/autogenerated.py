"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import PoolAddressesProvider, LendingPool, PriceOracle, ProtocolDataProvider, VariableDebtToken, IncentivesController

# Optionally
class PoolAddressesProvider(PoolAddressesProvider):
    ...
"""

from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class PoolAddressesProvider:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "pool_addresses_provider.json"))

    @property
    def get_acl_admin(self) -> str:
        return self.contract.functions.getACLAdmin().call(block_identifier=self.block)

    @property
    def get_acl_manager(self) -> str:
        return self.contract.functions.getACLManager().call(block_identifier=self.block)

    def get_address(self, id: bytes) -> str:
        return self.contract.functions.getAddress(id).call(block_identifier=self.block)

    @property
    def get_market_id(self) -> str:
        return self.contract.functions.getMarketId().call(block_identifier=self.block)

    @property
    def get_pool(self) -> str:
        return const_call(self.contract.functions.getPool())

    @property
    def get_pool_configurator(self) -> str:
        return self.contract.functions.getPoolConfigurator().call(block_identifier=self.block)

    @property
    def get_pool_data_provider(self) -> str:
        return self.contract.functions.getPoolDataProvider().call(block_identifier=self.block)

    @property
    def get_price_oracle(self) -> str:
        return self.contract.functions.getPriceOracle().call(block_identifier=self.block)

    @property
    def get_price_oracle_sentinel(self) -> str:
        return self.contract.functions.getPriceOracleSentinel().call(block_identifier=self.block)

    @property
    def owner(self) -> str:
        return self.contract.functions.owner().call(block_identifier=self.block)


class LendingPool:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "lending_pool.json"))

    @property
    def addresses_provider(self) -> str:
        return self.contract.functions.ADDRESSES_PROVIDER().call(block_identifier=self.block)

    @property
    def bridge_protocol_fee(self) -> int:
        return self.contract.functions.BRIDGE_PROTOCOL_FEE().call(block_identifier=self.block)

    @property
    def flashloan_premium_total(self) -> int:
        return self.contract.functions.FLASHLOAN_PREMIUM_TOTAL().call(block_identifier=self.block)

    @property
    def flashloan_premium_to_protocol(self) -> int:
        return self.contract.functions.FLASHLOAN_PREMIUM_TO_PROTOCOL().call(block_identifier=self.block)

    @property
    def max_number_reserves(self) -> int:
        return self.contract.functions.MAX_NUMBER_RESERVES().call(block_identifier=self.block)

    @property
    def max_stable_rate_borrow_size_percent(self) -> int:
        return self.contract.functions.MAX_STABLE_RATE_BORROW_SIZE_PERCENT().call(block_identifier=self.block)

    @property
    def pool_revision(self) -> int:
        return self.contract.functions.POOL_REVISION().call(block_identifier=self.block)

    def get_configuration(self, asset: str) -> tuple:
        return self.contract.functions.getConfiguration(asset).call(block_identifier=self.block)

    def get_e_mode_category_data(self, id: int) -> tuple:
        return self.contract.functions.getEModeCategoryData(id).call(block_identifier=self.block)

    def get_reserve_address_by_id(self, id: int) -> str:
        return self.contract.functions.getReserveAddressById(id).call(block_identifier=self.block)

    def get_reserve_data(self, asset: str) -> tuple:
        return self.contract.functions.getReserveData(asset).call(block_identifier=self.block)

    def get_reserve_normalized_income(self, asset: str) -> int:
        return self.contract.functions.getReserveNormalizedIncome(asset).call(block_identifier=self.block)

    def get_reserve_normalized_variable_debt(self, asset: str) -> int:
        return self.contract.functions.getReserveNormalizedVariableDebt(asset).call(block_identifier=self.block)

    @property
    def get_reserves_list(self) -> list[str]:
        return self.contract.functions.getReservesList().call(block_identifier=self.block)

    def get_user_account_data(self, user: str) -> tuple[int, int, int, int, int, int]:
        """
        Output: totalCollateralBase, totalDebtBase, availableBorrowsBase,
        currentLiquidationThreshold, ltv, healthFactor
        """
        return self.contract.functions.getUserAccountData(user).call(block_identifier=self.block)

    def get_user_configuration(self, user: str) -> tuple:
        return self.contract.functions.getUserConfiguration(user).call(block_identifier=self.block)

    def get_user_e_mode(self, user: str) -> int:
        return self.contract.functions.getUserEMode(user).call(block_identifier=self.block)


class PriceOracle:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "price_oracle.json"))

    @property
    def addresses_provider(self) -> str:
        return self.contract.functions.ADDRESSES_PROVIDER().call(block_identifier=self.block)

    @property
    def base_currency(self) -> str:
        return self.contract.functions.BASE_CURRENCY().call(block_identifier=self.block)

    @property
    def base_currency_unit(self) -> int:
        return self.contract.functions.BASE_CURRENCY_UNIT().call(block_identifier=self.block)

    def get_asset_price(self, asset: str) -> int:
        return self.contract.functions.getAssetPrice(asset).call(block_identifier=self.block)

    def get_assets_prices(self, assets: list[str]) -> list[int]:
        return self.contract.functions.getAssetsPrices(assets).call(block_identifier=self.block)

    @property
    def get_fallback_oracle(self) -> str:
        return self.contract.functions.getFallbackOracle().call(block_identifier=self.block)

    def get_source_of_asset(self, asset: str) -> str:
        return self.contract.functions.getSourceOfAsset(asset).call(block_identifier=self.block)


class ProtocolDataProvider:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "protocol_data_provider.json"))

    @property
    def addresses_provider(self) -> str:
        return self.contract.functions.ADDRESSES_PROVIDER().call(block_identifier=self.block)

    def get_a_token_total_supply(self, asset: str) -> int:
        return self.contract.functions.getATokenTotalSupply(asset).call(block_identifier=self.block)

    @property
    def get_all_a_tokens(self) -> list[tuple]:
        return self.contract.functions.getAllATokens().call(block_identifier=self.block)

    @property
    def get_all_reserves_tokens(self) -> list[tuple]:
        return self.contract.functions.getAllReservesTokens().call(block_identifier=self.block)

    def get_debt_ceiling(self, asset: str) -> int:
        return self.contract.functions.getDebtCeiling(asset).call(block_identifier=self.block)

    @property
    def get_debt_ceiling_decimals(self) -> int:
        return self.contract.functions.getDebtCeilingDecimals().call(block_identifier=self.block)

    def get_flash_loan_enabled(self, asset: str) -> bool:
        return self.contract.functions.getFlashLoanEnabled(asset).call(block_identifier=self.block)

    def get_interest_rate_strategy_address(self, asset: str) -> str:
        """
        Output: irStrategyAddress
        """
        return self.contract.functions.getInterestRateStrategyAddress(asset).call(block_identifier=self.block)

    def get_liquidation_protocol_fee(self, asset: str) -> int:
        return self.contract.functions.getLiquidationProtocolFee(asset).call(block_identifier=self.block)

    def get_paused(self, asset: str) -> bool:
        """
        Output: isPaused
        """
        return self.contract.functions.getPaused(asset).call(block_identifier=self.block)

    def get_reserve_caps(self, asset: str) -> tuple[int, int]:
        """
        Output: borrowCap, supplyCap
        """
        return self.contract.functions.getReserveCaps(asset).call(block_identifier=self.block)

    def get_reserve_configuration_data(
        self, asset: str
    ) -> tuple[int, int, int, int, int, bool, bool, bool, bool, bool]:
        """
        Output: decimals, ltv, liquidationThreshold, liquidationBonus,
        reserveFactor, usageAsCollateralEnabled, borrowingEnabled,
        stableBorrowRateEnabled, isActive, isFrozen
        """
        return self.contract.functions.getReserveConfigurationData(asset).call(block_identifier=self.block)

    def get_reserve_data(self, asset: str) -> tuple[int, int, int, int, int, int, int, int, int, int, int, int]:
        """
        Output: unbacked, accruedToTreasuryScaled, totalAToken,
        totalStableDebt, totalVariableDebt, liquidityRate, variableBorrowRate,
        stableBorrowRate, averageStableBorrowRate, liquidityIndex,
        variableBorrowIndex, lastUpdateTimestamp
        """
        return self.contract.functions.getReserveData(asset).call(block_identifier=self.block)

    def get_reserve_e_mode_category(self, asset: str) -> int:
        return self.contract.functions.getReserveEModeCategory(asset).call(block_identifier=self.block)

    def get_reserve_tokens_addresses(self, asset: str) -> tuple[str, str, str]:
        """
        Output: aTokenAddress, stableDebtTokenAddress,
        variableDebtTokenAddress
        """
        return self.contract.functions.getReserveTokensAddresses(asset).call(block_identifier=self.block)

    def get_siloed_borrowing(self, asset: str) -> bool:
        return self.contract.functions.getSiloedBorrowing(asset).call(block_identifier=self.block)

    def get_total_debt(self, asset: str) -> int:
        return self.contract.functions.getTotalDebt(asset).call(block_identifier=self.block)

    def get_unbacked_mint_cap(self, asset: str) -> int:
        return self.contract.functions.getUnbackedMintCap(asset).call(block_identifier=self.block)

    def get_user_reserve_data(self, asset: str, user: str) -> tuple[int, int, int, int, int, int, int, int, bool]:
        """
        Output: currentATokenBalance, currentStableDebt, currentVariableDebt,
        principalStableDebt, scaledVariableDebt, stableBorrowRate,
        liquidityRate, stableRateLastUpdated, usageAsCollateralEnabled
        """
        return self.contract.functions.getUserReserveData(asset, user).call(block_identifier=self.block)


class VariableDebtToken:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "variable_debt_token.json"))

    @property
    def debt_token_revision(self) -> int:
        return self.contract.functions.DEBT_TOKEN_REVISION().call(block_identifier=self.block)

    @property
    def delegation_with_sig_typehash(self) -> bytes:
        return self.contract.functions.DELEGATION_WITH_SIG_TYPEHASH().call(block_identifier=self.block)

    @property
    def domain_separator(self) -> bytes:
        return self.contract.functions.DOMAIN_SEPARATOR().call(block_identifier=self.block)

    @property
    def eip712_revision(self) -> bytes:
        return self.contract.functions.EIP712_REVISION().call(block_identifier=self.block)

    @property
    def pool(self) -> str:
        return self.contract.functions.POOL().call(block_identifier=self.block)

    @property
    def underlying_asset_address(self) -> str:
        return const_call(self.contract.functions.UNDERLYING_ASSET_ADDRESS())

    def allowance(self, arg0: str, arg1: str) -> int:
        return self.contract.functions.allowance(arg0, arg1).call(block_identifier=self.block)

    def balance_of(self, user: str) -> int:
        return self.contract.functions.balanceOf(user).call(block_identifier=self.block)

    def borrow_allowance(self, from_user: str, to_user: str) -> int:
        return self.contract.functions.borrowAllowance(from_user, to_user).call(block_identifier=self.block)

    @property
    def decimals(self) -> int:
        return self.contract.functions.decimals().call(block_identifier=self.block)

    @property
    def get_incentives_controller(self) -> str:
        return const_call(self.contract.functions.getIncentivesController())

    def get_previous_index(self, user: str) -> int:
        return self.contract.functions.getPreviousIndex(user).call(block_identifier=self.block)

    def get_scaled_user_balance_and_supply(self, user: str) -> tuple[int, int]:
        return self.contract.functions.getScaledUserBalanceAndSupply(user).call(block_identifier=self.block)

    @property
    def name(self) -> str:
        return self.contract.functions.name().call(block_identifier=self.block)

    def nonces(self, owner: str) -> int:
        return self.contract.functions.nonces(owner).call(block_identifier=self.block)

    def scaled_balance_of(self, user: str) -> int:
        return self.contract.functions.scaledBalanceOf(user).call(block_identifier=self.block)

    @property
    def scaled_total_supply(self) -> int:
        return self.contract.functions.scaledTotalSupply().call(block_identifier=self.block)

    @property
    def symbol(self) -> str:
        return self.contract.functions.symbol().call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)


class IncentivesController:
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
        self.contract = node.eth.contract(address=self.address, abi=load_abi(__file__, "incentives_controller.json"))

    @property
    def emission_manager(self) -> str:
        return self.contract.functions.EMISSION_MANAGER().call(block_identifier=self.block)

    @property
    def revision(self) -> int:
        return self.contract.functions.REVISION().call(block_identifier=self.block)

    def get_all_user_rewards(self, assets: list[str], user: str) -> tuple[list[str], list[int]]:
        """
        Output: rewardsList, unclaimedAmounts
        """
        return self.contract.functions.getAllUserRewards(assets, user).call(block_identifier=self.block)

    def get_asset_decimals(self, asset: str) -> int:
        return self.contract.functions.getAssetDecimals(asset).call(block_identifier=self.block)

    def get_asset_index(self, asset: str, reward: str) -> tuple[int, int]:
        return self.contract.functions.getAssetIndex(asset, reward).call(block_identifier=self.block)

    def get_claimer(self, user: str) -> str:
        return self.contract.functions.getClaimer(user).call(block_identifier=self.block)

    def get_distribution_end(self, asset: str, reward: str) -> int:
        return self.contract.functions.getDistributionEnd(asset, reward).call(block_identifier=self.block)

    @property
    def get_emission_manager(self) -> str:
        return self.contract.functions.getEmissionManager().call(block_identifier=self.block)

    def get_reward_oracle(self, reward: str) -> str:
        return self.contract.functions.getRewardOracle(reward).call(block_identifier=self.block)

    def get_rewards_by_asset(self, asset: str) -> list[str]:
        return self.contract.functions.getRewardsByAsset(asset).call(block_identifier=self.block)

    def get_rewards_data(self, asset: str, reward: str) -> tuple[int, int, int, int]:
        return self.contract.functions.getRewardsData(asset, reward).call(block_identifier=self.block)

    @property
    def get_rewards_list(self) -> list[str]:
        return self.contract.functions.getRewardsList().call(block_identifier=self.block)

    def get_transfer_strategy(self, reward: str) -> str:
        return self.contract.functions.getTransferStrategy(reward).call(block_identifier=self.block)

    def get_user_accrued_rewards(self, user: str, reward: str) -> int:
        return self.contract.functions.getUserAccruedRewards(user, reward).call(block_identifier=self.block)

    def get_user_asset_index(self, user: str, asset: str, reward: str) -> int:
        return self.contract.functions.getUserAssetIndex(user, asset, reward).call(block_identifier=self.block)

    def get_user_rewards(self, assets: list[str], user: str, reward: str) -> int:
        return self.contract.functions.getUserRewards(assets, user, reward).call(block_identifier=self.block)
