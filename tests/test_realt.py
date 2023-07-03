from decimal import Decimal

import pytest

from defyes import RealT
from defyes.constants import XDAI
from defyes.functions import get_node

TEST_BLOCK = 27450341
TEST_WALLET = "0x10e4597ff93cbee194f4879f8f1d54a370db6969"
WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)
WXDAI = "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"


@pytest.mark.parametrize("decimals", [False, True])
def test_underlying(decimals):
    x = RealT.underlying(TEST_WALLET, TEST_BLOCK, XDAI, WEB3, decimals=decimals)
    b = Decimal(702419123657008433506235) / Decimal(10**18 if decimals else 1)
    assert x == [[WXDAI, b]]
