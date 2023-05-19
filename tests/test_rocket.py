from decimal import Decimal

from defi_protocols import Rocket
from defi_protocols.constants import E_ADDRESS

TOKEN_ADDR = '0xae78736Cd615f374D3085123A210448E74Fc6393'
WALLET = '0x834b1E1E6026E4e93833423d6462525AA2dee86F'

def test_underlying():
    block = 17293000
    underlying = Rocket.underlying(WALLET, TOKEN_ADDR, block)
    assert underlying == [[E_ADDRESS, Decimal('991.795974817271166526')]]