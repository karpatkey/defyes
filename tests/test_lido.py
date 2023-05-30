import pytest
from decimal import Decimal

from defi_protocols import Lido
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node


WALLET_N1 = '0x3591D9351C736Daa7867fA6629D3A10880d78b83'


@pytest.mark.parametrize('steth', [True, False])
def test_underlying(steth):
    block = 17059685
    node = get_node(ETHEREUM, block)

    underlying = Lido.underlying(WALLET_N1, block, web3=node, steth=steth)
    assert underlying == [[ETHTokenAddr.stETH if steth else ZERO_ADDRESS, Decimal('50.00010737587224903593918755')]]


@pytest.mark.parametrize('steth', [True, False])
def test_unwrap(steth):
    block = 17059674
    node = get_node(ETHEREUM, block)

    asset = Lido.unwrap(100, block, web3=node, steth=steth)
    assert asset == [ETHTokenAddr.stETH if steth else ZERO_ADDRESS, Decimal('111.912984654790019100')]
