from decimal import Decimal
import pytest
from defi_protocols import Ankr
from defi_protocols.constants import E_ADDRESS, ETHEREUM

RETH_ADDRESS = '0xae78736Cd615f374D3085123A210448E74Fc6393'
TOKEN_ADDR = '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb'
WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
BLOCKCHAIN = ETHEREUM


def test_underlying():
    block = 17293000
    underlying = Ankr.underlying(WALLET, TOKEN_ADDR, block, BLOCKCHAIN)
    assert underlying == [[E_ADDRESS, Decimal('578.291718333123492848')]]


def test_underlying_deriv():
    block = 17293000
    underlying = Ankr.underlying(WALLET, TOKEN_ADDR, block, BLOCKCHAIN, deriv=True)
    assert underlying == [[TOKEN_ADDR, Decimal('518.999055369601472876')]]


def test_underlying_not_ankr_address():
    block = 17293000
    with pytest.raises(ValueError):
        Ankr.underlying(WALLET, RETH_ADDRESS, block, BLOCKCHAIN)
