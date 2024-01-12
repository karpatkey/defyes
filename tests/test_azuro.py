from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import GnosisTokenAddr
from karpatkit.node import get_node

from defyes import Azuro

WALLET_N1 = "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f"
NFT_ID = 1099511627781

BLOCK = 27532353
NODE = get_node(Chain.GNOSIS)


def test_get_deposit():
    assert (
        Azuro.get_deposit(WALLET_N1, NFT_ID, Azuro.POOL_ADDR_V2, BLOCK, Chain.GNOSIS, NODE) == 500000000000000000000000
    )


def test_underlying():
    assert Azuro.underlying(WALLET_N1, NFT_ID, BLOCK, Chain.GNOSIS, NODE, rewards=True) == [
        [GnosisTokenAddr.WXDAI, Decimal("522206.977145829181047864")],
        [GnosisTokenAddr.WXDAI, Decimal("22206.977145829181047864")],
    ]


@pytest.mark.skip(reason="Takes too long, we have to improve get_logs_web3")
def test_underlying_all():
    assert Azuro.underlying_all(WALLET_N1, BLOCK, Chain.GNOSIS, NODE, rewards=True) == [
        [
            [GnosisTokenAddr.WXDAI, Decimal("2327299.184243886654322408")],
            [GnosisTokenAddr.WXDAI, Decimal("27299.184243886654322408")],
        ],
        [[GnosisTokenAddr.WXDAI, Decimal("0")], [GnosisTokenAddr.WXDAI, Decimal("0.028837093647137877")]],
        [
            [GnosisTokenAddr.WXDAI, Decimal("1434603.321418109328231961")],
            [GnosisTokenAddr.WXDAI, Decimal("4613.321418109328231961")],
        ],
        [
            [GnosisTokenAddr.WXDAI, Decimal("71451.436321150949751018")],
            [GnosisTokenAddr.WXDAI, Decimal("1611.490569207598008139")],
        ],
        [
            [GnosisTokenAddr.WXDAI, Decimal("2327299.184243886654322408")],
            [GnosisTokenAddr.WXDAI, Decimal("27299.184243886654322408")],
        ],
    ]
