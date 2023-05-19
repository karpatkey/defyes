from decimal import Decimal

from defi_protocols import Ankr
from defi_protocols.constants import E_ADDRESS

TOKEN_ADDR = '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb'
WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

def test_underlying():
    block = 17293000
    underlying = Ankr.underlying(WALLET, TOKEN_ADDR, block)
    assert underlying == [[E_ADDRESS, Decimal('578.291718333123492848')]]