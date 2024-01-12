from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import GnosisTokenAddr

from defyes import QiDao


def test_get_vaul_address():
    address = QiDao.get_vault_address(GnosisTokenAddr.WETH, Chain.GNOSIS)
    assert address == "0x5c49b268c9841AFF1Cc3B0a418ff5c3442eE3F3b"


def test_get_vault_data():
    block = 27814350
    data = QiDao.get_vault_data(0, GnosisTokenAddr.GNO, block, Chain.GNOSIS)
    assert data.pop("liquidation_price").is_nan()
    assert data == {
        "collateral_address": GnosisTokenAddr.GNO,
        "collateral_amount": Decimal("12.669153514705549101"),
        "collateral_token_usd_value": Decimal("115.44042"),
        "debt_address": GnosisTokenAddr.MAI,
        "debt_amount": Decimal("0"),
        "debt_token_usd_value": Decimal("0.99446664920316931668708736"),
        "debt_usd_value": Decimal("0"),
        "collateral_ratio": Decimal("Infinity"),
        "available_debt_amount": Decimal("3259.913205994382808393"),
        "liquidation_ratio": 130,
    }


def test_underlying():
    block = 27814350
    underlying = QiDao.underlying(0, GnosisTokenAddr.GNO, block, Chain.GNOSIS)
    assert underlying == [[GnosisTokenAddr.GNO, Decimal("12.669153514705549101")], [GnosisTokenAddr.MAI, Decimal("0")]]
