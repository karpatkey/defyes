from decimal import Decimal

from defyes import Azuro
from defyes.constants import WXDAI, XDAI
from defyes.functions import get_node

WALLET_N1 = "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f"
NFT_ID = 1099511627781

BLOCK = 27532353
NODE = get_node(XDAI, BLOCK)


def test_get_deposit():
    assert Azuro.get_deposit(WALLET_N1, NFT_ID, Azuro.POOL_ADDR_V2, BLOCK, XDAI, NODE) == 500000000000000000000000


def test_underlying():
    assert Azuro.underlying(WALLET_N1, NFT_ID, BLOCK, XDAI, NODE, rewards=True) == [
        [WXDAI, Decimal("522206.977145829181047864")],
        [WXDAI, Decimal("22206.977145829181047864")],
    ]


def test_underlying_all():
    assert Azuro.underlying_all(WALLET_N1, BLOCK, XDAI, NODE, rewards=True) == [
        [[WXDAI, Decimal("2327299.184243886654322408")], [WXDAI, Decimal("27299.184243886654322408")]],
        [[WXDAI, Decimal("0")], [WXDAI, Decimal("0.028837093647137877")]],
        [[WXDAI, Decimal("1434603.321418109328231961")], [WXDAI, Decimal("4613.321418109328231961")]],
        [[WXDAI, Decimal("71451.436321150949751018")], [WXDAI, Decimal("1611.490569207598008139")]],
        [[WXDAI, Decimal("2327299.184243886654322408")], [WXDAI, Decimal("27299.184243886654322408")]],
    ]
