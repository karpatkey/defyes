from decimal import Decimal

from defyes import RocketPool
from defyes.constants import ETHEREUM, ZERO_ADDRESS

ROCKET_ADDR = "0xae78736Cd615f374D3085123A210448E74Fc6393"
WALLET = "0xEADB3840596cabF312F2bC88A4Bb0b93A4E1FF5F"
BLOCKCHAIN = ETHEREUM


def test_underlying():
    block = 17293000
    underlying_unwrapped = RocketPool.underlying(WALLET, block, BLOCKCHAIN, unwrapped=True)
    assert underlying_unwrapped == [[ZERO_ADDRESS, Decimal("3382.999083555502681732137732")]]
    underlying_wrapped = RocketPool.underlying(WALLET, block, BLOCKCHAIN, unwrapped=False)
    assert underlying_wrapped == [[ROCKET_ADDR, Decimal("3158.323722446125043829")]]


def test_unwrap():
    block = 17293000
    amount_int = 12345677893892348743
    unwrapped_int_result = RocketPool.unwrap(amount_int, block, BLOCKCHAIN)
    assert unwrapped_int_result == [[ZERO_ADDRESS, Decimal("13.22391897451281051551684486")]]
    amount_float = amount_int + 0.1
    unwrapped_float_result = RocketPool.unwrap(amount_float, block, BLOCKCHAIN)
    assert unwrapped_float_result == [[ZERO_ADDRESS, Decimal("13.22391897451280961683245385")]]
    amount_decimal = Decimal(amount_float)
    unwrapped_decimal_result = RocketPool.unwrap(amount_decimal, block, BLOCKCHAIN)
    assert unwrapped_decimal_result == [[ZERO_ADDRESS, Decimal("13.22391897451280961683245385")]]
