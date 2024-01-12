from decimal import Decimal

from defabipedia import Chain
from karpatkit.constants import Address

from defyes import Ankr

ANKR_ADDR = "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb"
WALLET = "0x5A6e41C8Ca7830D9ce5b3C8108fD163c7CC8D5E5"
BLOCKCHAIN = Chain.ETHEREUM


def test_underlying():
    block = 17293000
    underlying_unwrapped = Ankr.underlying(WALLET, block, BLOCKCHAIN, unwrapped=True)
    assert underlying_unwrapped == [[Address.ZERO, Decimal("269.0634980558404304508072537")]]
    underlying_wrapped = Ankr.underlying(WALLET, block, BLOCKCHAIN, unwrapped=False)
    assert underlying_wrapped == [[ANKR_ADDR, Decimal("241.476225403906583644")]]


def test_unwrap():
    block = 17293000
    amount_int = 12345677893892348743
    unwrapped_int_result = Ankr.unwrap(amount_int, block, BLOCKCHAIN)
    assert unwrapped_int_result == [[Address.ZERO, Decimal("13.75610072770168784459304943")]]
    amount_float = amount_int + 0.1
    unwrapped_float_result = Ankr.unwrap(amount_float, block, BLOCKCHAIN)
    assert unwrapped_float_result == [[Address.ZERO, Decimal("13.75610072770168690974211539")]]
    amount_decimal = Decimal(amount_float)
    unwrapped_decimal_result = Ankr.unwrap(amount_decimal, block, BLOCKCHAIN)
    assert unwrapped_decimal_result == [[Address.ZERO, Decimal("13.75610072770168690974211539")]]
    # Block where ankrETH had a different proxy implementation (ARETH_16)
    block = 16476339
    amount_int = 12345677893892348743
    unwrapped_int_result = Ankr.unwrap(amount_int, block, BLOCKCHAIN)
    assert unwrapped_int_result == [[Address.ZERO, Decimal("13.55106811673978062983888839")]]
