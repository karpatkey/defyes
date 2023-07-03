from decimal import Decimal

import pytest

from defyes import Unit
from defyes.constants import ETHEREUM
from defyes.functions import get_node

USDP = "0x1456688345527bE1f37E9e627DA0837D6f08C925"
FTM_ETH = "0x4E15361FD6b4BB609Fa63C81A2be19d873717870"
WOOFY_ETH = "0xD0660cD418a64a1d44E9214ad8e459324D8157f1"
xSUSHI_ETH = "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272"
X3CRV_Gauge_Unit_ETH = "0x4bfB2FA13097E5312B19585042FdbF3562dC8676"
yvYFI_ETH = "0xE14d13d8B3b85aF791b2AADD661cDBd5E6097Db1"
EURS_ETH = "0xdB25f211AB05b1c97D595516F45794528a807ad8"
wuSSLPWETHUSDT_ETH = "0xcE5147182624fD121d0CE974847A8DbFCa9358B7"
USG_ETH = "0x0770E27F92F0D0e716dc531037B8b87FEFEbE561"

TEST_BLOCK = 17225800
TEST_WALLET = "0x8442e4FCbbA519B4f4C1EA1FcE57a5379C55906C"
COLLATERAL_ADDRESS = FTM_ETH
WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)


@pytest.mark.parametrize("decimals", [True, False])
def test_get_cdp_viewer_data(decimals):
    x = Unit.get_cdp_viewer_data(TEST_WALLET, COLLATERAL_ADDRESS, TEST_BLOCK, ETHEREUM, WEB3, decimals=decimals)
    y = Decimal(10**18 if decimals else 1)
    assert x == {
        "icr": 69,
        "liquidation_ratio": 70,
        "collateral_address": FTM_ETH,
        "collateral_amount": Decimal("1000000000000000000") / y,
        "debt_amount": Decimal("1620018748269707798") / y,
        "liquidation_price": Decimal("2.314312497528153997142857143"),
        "collateral_usd_value": Decimal("0.3637421370000000000000000000"),
        "utilization_ratio": Decimal("445.3756063652608380645215157"),
    }


@pytest.mark.parametrize("decimals", [True, False])
def test_get_cdp_data(decimals):
    x = Unit.get_cdp_data(TEST_WALLET, COLLATERAL_ADDRESS, TEST_BLOCK, ETHEREUM, WEB3, decimals=decimals)
    y = Decimal(10**18 if decimals else 1)
    assert x == {
        "icr": 69,
        "liquidation_ratio": 70,
        "stability_fee": Decimal("0.9"),
        "liquidation_fee": 5,
        "issuance_fee": Decimal("0.3"),
        "collateral_address": FTM_ETH,
        "collateral_amount": Decimal("1000000000000000000") / y,
        "debt_address": USDP,
        "debt_amount": Decimal("1620018748269707798") / y,
        "liquidation_price": Decimal("2.314312497528153997142857143"),
        "collateral_usd_value": Decimal("0.3637421370000000000000000000"),
        "utilization_ratio": Decimal("445.3756063652608380645215157"),
        "utilization": Decimal("645.4718932829867218326398778"),
        "debt_limit": Decimal("0"),
        "borrowable_debt": Decimal("-1620969383653572380") / y,
    }


@pytest.mark.parametrize("decimals", [True, False])
def test_underlying(decimals):
    x = Unit.underlying(TEST_WALLET, TEST_BLOCK, ETHEREUM, WEB3, decimals=decimals)
    y18 = Decimal(10**18 if decimals else 1)
    y12 = Decimal(10**12 if decimals else 1)
    y2 = Decimal(10**2 if decimals else 1)
    assert x == [
        [[FTM_ETH, Decimal("1000000000000000000") / y18], [USDP, Decimal("-1620018748269707798") / y18]],
        [[WOOFY_ETH, Decimal("559232649388782") / y12], [USDP, Decimal("-8724323954416268170") / y18]],
        [[xSUSHI_ETH, Decimal("300000000000000000") / y18], [USDP, Decimal("-1304849446951977717") / y18]],
        [[X3CRV_Gauge_Unit_ETH, Decimal("2400000000000000000") / y18], [USDP, Decimal("-1660386168669741637") / y18]],
        [[yvYFI_ETH, Decimal("642818733893975") / y18], [USDP, Decimal("-3889516423093472424") / y18]],
        [[EURS_ETH, Decimal("400") / y2], [USDP, Decimal("-2064283359842719431") / y18]],
        [[wuSSLPWETHUSDT_ETH, Decimal("760053991711") / y18], [USDP, Decimal("-19645142679366516132") / y18]],
        [[USG_ETH, Decimal("1000000000000000000") / y18], [USDP, Decimal("-1000000000000000000") / y18]],
    ]
