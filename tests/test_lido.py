from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.constants import Address
from karpatkit.node import get_node

from defyes import Lido

WALLET_N1 = "0x3591D9351C736Daa7867fA6629D3A10880d78b83"


@pytest.mark.parametrize("steth", [True, False])
def test_underlying(steth):
    block = 17059685
    node = get_node(Chain.ETHEREUM)

    underlying = Lido.underlying(WALLET_N1, block, web3=node, steth=steth)
    assert underlying == [
        [EthereumTokenAddr.stETH if steth else Address.ZERO, Decimal("50.00010737587224903593918755")]
    ]


@pytest.mark.parametrize("steth", [True, False])
def test_unwrap(steth):
    block = 17059674
    node = get_node(Chain.ETHEREUM)

    asset = Lido.unwrap(100, block, web3=node, steth=steth)
    assert asset == [EthereumTokenAddr.stETH if steth else Address.ZERO, Decimal("111.912984654790019100")]
