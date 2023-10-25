from decimal import Decimal
from functools import cached_property
from typing import Iterator, NamedTuple

from web3 import Web3

from defyes.constants import Chain
from defyes.functions import ensure_a_block_number
from defyes.types import Addr, Token, TokenAmount

from .autogenerated import BaseVault


class BaseVault(BaseVault):
    @cached_property
    def management_withdraw_fee_factor(self) -> Decimal:
        return Decimal(self.get_withdraw_fee_ratio) / self.denominator

    @cached_property
    def share_token(self):
        return Token.get_instance(self.address, self.blockchain, self.block)

    @cached_property
    def asset_token(self):
        return Token.get_instance(self.asset, self.blockchain, self.block)


class StEthVolatilityVault(BaseVault):
    """
    stETH Volatility Vault

    This is a low-risk strategy that focuses on ETH accumulation. It invests in Lido and uses part of Lido's yield to
    set up strangles weekly. It accumulates more ETH whenever the price goes up and when it goes down.
    """

    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: Addr("0x463F9ED5e11764Eb9029762011a03643603aD879"),
        Chain.GOERLI: Addr("0x626bC69e52A543F8dea317Ff885C9060b8ebbbf5"),
    }


class EthphoriaVault(BaseVault):
    """
    ETHphoria Vault

    This is a low-risk strategy that focuses on ETH accumulation. The vault stakes ETH in Lido and uses all weekly yield
    to buy one-week ETH call options on a weekly basis. It accumulates more ETH whenever the price goes up. It is a way
    to go long on ETH without risking the principal.
    """

    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: Addr("0x5FE4B38520e856921978715C8579D2D7a4d2274F"),
    }


class UsdcFudVault(BaseVault):
    """
    USDC FUD Vault

    This is a low-risk strategy that focuses on hedging against market crashes. The vault invests USDC in Aave and uses
    all weekly yield to buy one-week ETH put options on a weekly basis. It accumulates more USDC whenever the price goes
    down.
    """

    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: Addr("0x287f941aB4B5AaDaD2F13F9363fcEC8Ee312a969"),
    }


vault_classes = (
    StEthVolatilityVault,
    EthphoriaVault,
    UsdcFudVault,
)


class VaultAssetShare(NamedTuple):
    vault: BaseVault
    asset_amount: TokenAmount
    share_amount: TokenAmount


def underlyings_holdings(
    wallet: Addr, block: int | str = "latest", blockchain: Chain = Chain.ETHEREUM
) -> Iterator[VaultAssetShare]:
    block_id = ensure_a_block_number(block, blockchain)
    for vault_class in vault_classes:
        vault = vault_class(blockchain, block_id)
        shares = vault.balance_of(wallet)
        assets = vault.preview_redeem(shares) + vault.idle_assets_of(wallet)  # includes management fee
        yield VaultAssetShare(
            vault,
            TokenAmount.from_teu(assets, vault.asset_token),
            TokenAmount.from_teu(shares, vault.share_token),
        )


def get_protocol_data(
    wallet: Addr, block: int | str = "latest", blockchain: Chain = Chain.ETHEREUM, decimals: bool = True
) -> dict:
    wallet = Web3.to_checksum_address(wallet)
    block_id = ensure_a_block_number(block, blockchain)

    positions = {
        vault.address: {
            "underlyings": [asset_amount.as_dict(decimals)],
            "holdings": [share_amount.as_dict(decimals)],
        }
        for vault, asset_amount, share_amount in underlyings_holdings(wallet, block_id, blockchain)
        if asset_amount != 0 or share_amount != 0
    }

    return {
        "blockchain": blockchain,
        "block_id": block_id,
        "protocol": "Pods",
        "version": 0,
        "wallet": wallet,
        "decimals": decimals,
        "positions": positions,
        "positions_key": "vault_address",
        "financial_metrics": {},
    }
