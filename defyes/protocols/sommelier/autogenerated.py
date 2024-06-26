"""
Autogenerated module. Don't change it manualy. Instead, import its classes into __init__.py or even derive them adding
extra methds.

# Inside __init__.py

from .autogenerated import CellarBalancerMultiAsset

# Optionally
class CellarBalancerMultiAsset(CellarBalancerMultiAsset):
    ...
"""

from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.generator import load_abi


class CellarBalancerMultiAsset:
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
        self.contract = node.eth.contract(
            address=self.address, abi=load_abi(__file__, "cellar_balancer_multi_asset.json")
        )

    @property
    def domain_separator(self) -> bytes:
        return self.contract.functions.DOMAIN_SEPARATOR().call(block_identifier=self.block)

    def allowance(self, arg0: str, arg1: str) -> int:
        return self.contract.functions.allowance(arg0, arg1).call(block_identifier=self.block)

    def alternative_asset_data(self, arg0: str) -> tuple[bool, int, int]:
        """
        Output: isSupported, holdingPosition, depositFee
        """
        return self.contract.functions.alternativeAssetData(arg0).call(block_identifier=self.block)

    @property
    def asset(self) -> str:
        return const_call(self.contract.functions.asset())

    def balance_of(self, arg0: str) -> int:
        return self.contract.functions.balanceOf(arg0).call(block_identifier=self.block)

    @property
    def block_external_receiver(self) -> bool:
        return self.contract.functions.blockExternalReceiver().call(block_identifier=self.block)

    def convert_to_assets(self, shares: int) -> int:
        """
        Output: assets
        """
        return self.contract.functions.convertToAssets(shares).call(block_identifier=self.block)

    def convert_to_shares(self, assets: int) -> int:
        """
        Output: shares
        """
        return self.contract.functions.convertToShares(assets).call(block_identifier=self.block)

    @property
    def decimals(self) -> int:
        return self.contract.functions.decimals().call(block_identifier=self.block)

    @property
    def fee_data(self) -> tuple[int, int, int, str]:
        """
        Output: strategistPlatformCut, platformFee, lastAccrual,
        strategistPayoutAddress
        """
        return self.contract.functions.feeData().call(block_identifier=self.block)

    @property
    def get_credit_positions(self) -> list[int]:
        return self.contract.functions.getCreditPositions().call(block_identifier=self.block)

    @property
    def get_debt_positions(self) -> list[int]:
        return self.contract.functions.getDebtPositions().call(block_identifier=self.block)

    @property
    def holding_position(self) -> int:
        return self.contract.functions.holdingPosition().call(block_identifier=self.block)

    @property
    def ignore_pause(self) -> bool:
        return self.contract.functions.ignorePause().call(block_identifier=self.block)

    @property
    def is_paused(self) -> bool:
        return self.contract.functions.isPaused().call(block_identifier=self.block)

    def is_position_used(self, arg0: int) -> bool:
        return self.contract.functions.isPositionUsed(arg0).call(block_identifier=self.block)

    @property
    def is_shutdown(self) -> bool:
        return self.contract.functions.isShutdown().call(block_identifier=self.block)

    @property
    def locked(self) -> bool:
        return self.contract.functions.locked().call(block_identifier=self.block)

    def max_deposit(self, arg0: str) -> int:
        return self.contract.functions.maxDeposit(arg0).call(block_identifier=self.block)

    def max_mint(self, arg0: str) -> int:
        return self.contract.functions.maxMint(arg0).call(block_identifier=self.block)

    def max_redeem(self, owner: str) -> int:
        return self.contract.functions.maxRedeem(owner).call(block_identifier=self.block)

    def max_withdraw(self, owner: str) -> int:
        return self.contract.functions.maxWithdraw(owner).call(block_identifier=self.block)

    @property
    def name(self) -> str:
        return self.contract.functions.name().call(block_identifier=self.block)

    def nonces(self, arg0: str) -> int:
        return self.contract.functions.nonces(arg0).call(block_identifier=self.block)

    @property
    def owner(self) -> str:
        return self.contract.functions.owner().call(block_identifier=self.block)

    def preview_deposit(self, assets: int) -> int:
        """
        Output: shares
        """
        return self.contract.functions.previewDeposit(assets).call(block_identifier=self.block)

    def preview_mint(self, shares: int) -> int:
        """
        Output: assets
        """
        return self.contract.functions.previewMint(shares).call(block_identifier=self.block)

    def preview_multi_asset_deposit(self, deposit_asset: str, assets: int) -> int:
        """
        Output: shares
        """
        return self.contract.functions.previewMultiAssetDeposit(deposit_asset, assets).call(block_identifier=self.block)

    def preview_redeem(self, shares: int) -> int:
        """
        Output: assets
        """
        return self.contract.functions.previewRedeem(shares).call(block_identifier=self.block)

    def preview_withdraw(self, assets: int) -> int:
        """
        Output: shares
        """
        return self.contract.functions.previewWithdraw(assets).call(block_identifier=self.block)

    @property
    def price_router(self) -> str:
        return self.contract.functions.priceRouter().call(block_identifier=self.block)

    @property
    def registry(self) -> str:
        return self.contract.functions.registry().call(block_identifier=self.block)

    @property
    def share_price_oracle(self) -> str:
        return self.contract.functions.sharePriceOracle().call(block_identifier=self.block)

    @property
    def share_supply_cap(self) -> int:
        return self.contract.functions.shareSupplyCap().call(block_identifier=self.block)

    @property
    def symbol(self) -> str:
        return self.contract.functions.symbol().call(block_identifier=self.block)

    @property
    def total_assets(self) -> int:
        """
        Output: assets
        """
        return self.contract.functions.totalAssets().call(block_identifier=self.block)

    @property
    def total_assets_withdrawable(self) -> int:
        """
        Output: assets
        """
        return self.contract.functions.totalAssetsWithdrawable().call(block_identifier=self.block)

    @property
    def total_supply(self) -> int:
        return self.contract.functions.totalSupply().call(block_identifier=self.block)
