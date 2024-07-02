from contextlib import suppress
from decimal import Decimal
from functools import cached_property

from defabipedia import Chain
from karpatkit.helpers import suppress_error_codes
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.functions import get_decimals, get_logs_web3, to_token_amount

from . import autogenerated

START_BLOCK = {
    "ethereumv1": 14457664,
    Chain.ETHEREUM: 15399251,
    Chain.POLYGON: 40687417,
    Chain.ARBITRUM: 72942741,
    Chain.GNOSIS: 27088528,
}


class Vault(autogenerated.Vault):
    ADDR: str = "0xBA12222222228d8Ba445958a75a0704d566BF2C8"
    default_addresses: dict[str, str] = {
        Chain.ETHEREUM: ADDR,
        Chain.POLYGON: ADDR,
        Chain.GNOSIS: ADDR,
        Chain.ARBITRUM: ADDR,
    }

    def get_pool_data(self, pool_id: int) -> list:
        tokens = []
        pool_data = self.get_pool_tokens(pool_id)
        for token, balance in zip(pool_data[0], pool_data[1]):
            tokens.append((token, balance))

        return tokens


class PoolToken(autogenerated.PoolToken):
    def preview_redeem(self, shares: int) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return super().preview_redeem(shares)

    @cached_property
    def pool_id(self) -> str | None:
        with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
            return super().get_pool_id


class LiquidityPool(autogenerated.LiquidityPool):
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
    def main_token(self) -> int | None:
        with suppress(ContractLogicError), suppress_error_codes():
            return self.get_main_token

    @cached_property
    def wrapped_token(self) -> int | None:
        with suppress(ContractLogicError), suppress_error_codes():
            return self.get_wrapped_token

    @cached_property
    def wrapped_token_rate(self) -> int | None:
        with suppress(ContractLogicError), suppress_error_codes():
            return self.get_wrapped_token_rate

    def balance_of(self, wallet: str) -> int:
        wallet = Web3.to_checksum_address(wallet)
        return super().balance_of(wallet)

    def exit_balance(self, lp_amount: Decimal, token_balance: Decimal) -> Decimal:
        return Decimal(lp_amount) * Decimal(10**self.decimals) / Decimal(self.supply) * Decimal(token_balance)

    def calc_amount(
        self, token: PoolToken, lp_amount: Decimal, token_amount: Decimal, decimals: bool = True
    ) -> Decimal:
        if token.address == self.wrapped_token:
            main_token = self.main_token
            token_decimals = get_decimals(main_token, self.blockchain, web3=self.contract.w3) if decimals else 0
            if self.wrapped_token_rate:
                balance = self.exit_balance(lp_amount, token_amount) * self.wrapped_token_rate / Decimal(10**18)
            else:
                # FIXME: preview_redeem receives an int and the result of exit_balance may not be an integer
                balance = Decimal(token.preview_redeem(int(self.exit_balance(lp_amount, token_amount))))
        else:
            main_token = token.address
            token_decimals = token.decimals
            balance = self.exit_balance(lp_amount, token_amount)

        if decimals:
            balance = balance / Decimal(10**token_decimals)

        return main_token, balance

    def swap_fee_percentage_for(self, block: int | str) -> int:
        return self.contract.functions.getSwapFeePercentage().call(block_identifier=block)

    def swap_fees(self, vault_address: str, block_start: int, decimals: bool = True) -> list[dict]:
        node = self.contract.w3
        pool_id = "0x" + self.poolid.hex()
        swap_event = node.keccak(text="Swap(bytes32,address,address,uint256,uint256)").hex()

        if block_start < START_BLOCK[self.blockchain]:
            block_start = START_BLOCK[self.blockchain]

        swap_logs = get_logs_web3(
            blockchain=self.blockchain,
            address=vault_address,
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
