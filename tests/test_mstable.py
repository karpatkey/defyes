from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr

from defyes import mStable

WALLET = "0x83dE1603DF0249c0155e30c636598FEE5E11DBdc"
TOKEN_ADDR = "0x455fb969dc06c4aa77e7db3f0686cc05164436d2"


def test_underlying():
    block = 16473571
    underlying = mStable.underlying(TOKEN_ADDR, WALLET, block, blockchain=Chain.ETHEREUM)
    assert underlying == [[EthereumTokenAddr.USDC, Decimal("23744.121638")]]
