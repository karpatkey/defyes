from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import GnosisTokenAddr
from karpatkit.node import get_node

from defyes import RealT

TEST_BLOCK = 27450341
TEST_WALLET = "0x10e4597ff93cbee194f4879f8f1d54a370db6969"
WEB3 = get_node(blockchain=Chain.GNOSIS)


@pytest.mark.parametrize("decimals", [False, True])
def test_underlying(decimals):
    x = RealT.underlying(TEST_WALLET, TEST_BLOCK, Chain.GNOSIS, WEB3, decimals=decimals)
    b = Decimal(702419123657008433506235) / Decimal(10**18 if decimals else 1)
    assert x == [[GnosisTokenAddr.WXDAI, b]]
