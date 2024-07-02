from decimal import Decimal

from defabipedia import Chain

from defyes.protocols import stader

WALLET = "0x4F2083f5fBede34C2714aFfb3105539775f7FE64"
ETHx = "0xa35b1b31ce002fbf2058d22f30f95d405200a15b"


def test_get_protocol_data_for():
    block = 19264497
    p = stader.get_protocol_data_for(Chain.ETHEREUM, WALLET, ETHx, block)
    assert p == {
        "holdings": ["995.830893684182054684*ETHx"],
        "underlyings": ["1_017.757772400597608194*ETH"],
        "unclaimed_rewards": [],
        "financial_metrics": {},
    }


def test_unwrap_polygon():
    result = stader.unwrap(12567.567, 56726863, False, "polygon")
    expected = ["0x0000000000000000000000000000000000001010", Decimal("13957.39501740044196177572694")]
    assert result == expected


def test_unwrap_ethereum():
    result = stader.unwrap(12567.567, 19825299, False, "ethereum")
    expected = ["0x0000000000000000000000000000000000000000", Decimal("12932.423602700606662488222")]
    assert result == expected
