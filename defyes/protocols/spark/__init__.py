"""
Spark protocol (by default in Ethereum mainnet)

Mainnet Addresses https://docs.sparkprotocol.io/developers/deployed-contracts/mainnet-addresses
"""

from decimal import Decimal
from typing import Iterator, NamedTuple

from defyes.constants import Chain
from defyes.types import Addr, Token, TokenAmount

from .autogenerated import ProtocolDataProvider


class ProtocolDataProvider(ProtocolDataProvider):
    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: Addr("0xFc21d6d146E6086B8359705C8b28512a983db0cb"),
    }

    @property
    def assets_with_reserve_tokens(self):
        for asset_name, asset_addr in self.get_all_reserves_tokens:
            asset = Token(asset_addr, asset_name)
            tokens = self.get_reserve_tokens_addresses(asset_addr)
            yield asset, ReserveTokensAddresses(*tokens)

    @property
    def web3(self):
        return self.contract.w3

    @property
    def last_block_id(self):
        return self.web3.eth.block_number

    @property
    def block_id(self):
        return self.block if isinstance(self.block, int) else self.last_block_id

    def underlying_all(self, wallet: Addr):
        wallet = Addr(wallet)
        return {
            "blockchain": self.blockchain,
            "block_id": self.block_id,
            "protocol": "Spark",
            "version": 0,
            "wallet": wallet,
            "positions": dict(self.positions(wallet)),
        }

    def positions(self, wallet: Addr) -> Iterator[tuple[Addr, dict]]:
        web3 = self.web3
        for asset, tokens in self.assets_with_reserve_tokens:
            ur = UserReserveData(*self.get_user_reserve_data(asset, wallet))

            def holdings():
                for amount, (kind, addr) in zip(ur[:3], tokens._asdict().items()):
                    if amount != 0:
                        yield f"{kind}_{asset.label}", TokenAmount(amount, addr, web3)
                    # ,{
                    #     "address": addr,
                    #     "balance": TokenAmount(amount, addr, web3),
                    # }

            holdings = dict(holdings())
            if holdings:
                position = {
                    "holdings": holdings,
                    "underlying": TokenAmount(ur.sp - ur.stable_debt - ur.variable_debt, str(asset), web3),
                }
                yield asset, position


class ReserveTokensAddresses(NamedTuple):
    sp: Addr
    stable_debt: Addr
    variable_debt: Addr


class UserReserveData(NamedTuple):
    sp: int
    stable_debt: int
    variable_debt: int
    principal_stable_debt: int
    scaled_variable_debt: int
    stable_borrow_rate: int
    reserve_liquidity_rate: int
    timestamp: int
    is_collateral: bool


def underlying_all(wallet: Addr, block: int | str, chain: Chain, decimal: bool = True) -> dict:
    ret = ProtocolDataProvider(chain, block).underlying_all(wallet)

    def to_value(token_amount):
        return Decimal(str(token_amount)) if decimal else int(token_amount)

    def to_dict(token_amount):
        return {"balance": to_value(token_amount), "address": token_amount.addr}

    positions = ret["positions"]

    ret["positions"] = {
        str(asset): {
            "holdings": [to_dict(token_amount) for token_amount in position["holdings"].values()],
            "underlying": to_value(position["underlying"]),
        }
        for asset, position in positions.items()
    }
    return ret
