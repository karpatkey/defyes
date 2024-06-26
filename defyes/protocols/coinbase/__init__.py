from decimal import Decimal

from karpatkit.constants import Address, Chain

from defyes.functions import ensure_a_block_number
from defyes.protocols.coinbase.autogenerated import StakedToken
from defyes.types import Token, TokenAmount

StakedToken.default_addresses = {Chain.ETHEREUM: "0xBe9895146f7AF43049ca1c1AE358B0541Ea49704"}


def reduce_cbETH(
    amount: int | float, blockchain: str | Chain, block: int | str, decimals: bool = True
) -> tuple[str, int]:
    """Reduce cbETH to ETH.
    Currently the only available blockchain is Ethereum.
    Get the exchange rate from the StakedToken contract (cbETH) and reduce the amount of cbETH to ETH.

    Args:
        amount (float): Amount of osETH to reduce
        block (int, str): Block number or "latest"
        teu (bool, optional): If the amount is in teu. Defaults to False.
    """
    if blockchain != Chain.ETHEREUM:
        raise ValueError("Currently only Ethereum is supported")

    block = ensure_a_block_number(block, blockchain)
    token = Token(Address.ZERO, Chain.ETHEREUM, block)

    unwrap_rate = StakedToken(blockchain, block).exchange_rate

    amount_eth = Decimal(amount) * Decimal(unwrap_rate)

    eth_reduced = TokenAmount.from_teu(amount_eth, token).balance(decimals)

    if not decimals:
        int(eth_reduced)

    return Address.ZERO, eth_reduced
