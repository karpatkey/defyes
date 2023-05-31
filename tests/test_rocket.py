from decimal import Decimal

from defi_protocols import RocketPool
from defi_protocols.constants import ZERO_ADDRESS, ETHEREUM

ROCKET_ADDR = '0xae78736Cd615f374D3085123A210448E74Fc6393'
WALLET = '0xEADB3840596cabF312F2bC88A4Bb0b93A4E1FF5F'
BLOCKCHAIN = ETHEREUM

def test_underlying():
    block = 17293000
    underlying_unwrapped = RocketPool.underlying(WALLET, block, BLOCKCHAIN, unwrapped=True)
    assert underlying_unwrapped == [[ZERO_ADDRESS, Decimal('3382.999083555502681732')]]
    underlying_wrapped = RocketPool.underlying(WALLET, block, BLOCKCHAIN, unwrapped=False)
    assert underlying_wrapped == [[ROCKET_ADDR, Decimal('3158.323722446125043829')]]