from decimal import Decimal

from defi_protocols import Reflexer
from defi_protocols.constants import ETHTokenAddr


LPTOKEN_ADDR = '0xd6f3768e62ef92a9798e5a8cedd2b78907cecef9'
WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'


def test_underlying():
    block = 16000000
    underlying = Reflexer.underlying(WALLET, LPTOKEN_ADDR, block)
    assert underlying == [[ETHTokenAddr.FLX, Decimal('48390.17697598300981895886497')],
                          [ETHTokenAddr.WETH, Decimal('556.9148074791862641107712679')]]


def test_lptoken_underlying():
    block = 16000000
    underlying = Reflexer.balance_of_lptoken_underlying(WALLET, LPTOKEN_ADDR, block)
    assert underlying == [[ETHTokenAddr.FLX, Decimal('0')],
                          [ETHTokenAddr.WETH, Decimal('0.0000')]]


def test_pool_balances():
    block = 16000000
    underlying = Reflexer.pool_balance(LPTOKEN_ADDR, block)
    assert underlying == [[ETHTokenAddr.FLX, Decimal('124449.671679348329429663')],
                          [ETHTokenAddr.WETH, Decimal('1432.271367359351906863')]]
