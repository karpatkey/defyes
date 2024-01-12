from decimal import Decimal

import pytest
from defabipedia import Chain

from defyes import pretty
from defyes.protocols import spark
from defyes.types import Addr, Token, TokenAmount

wallet = Addr(0x849D52316331967B6FF1198E5E32A0EB168D039D)
block_id = 17_772_457

DAI = Token.get_instance(0x6B175474E89094C44DA98B954EEDEAC495271D0F, Chain.ETHEREUM)
GNO = Token.get_instance(0x6810E776880C02933D47DB1B9FC05908E5386B96, Chain.ETHEREUM)
variableDebtDAI = Token.get_instance("0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914", Chain.ETHEREUM)
spGNO = Token.get_instance("0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F", Chain.ETHEREUM)

expected_position = {
    "holdings": [
        TokenAmount.from_teu(1_000_035_715961244421526907, variableDebtDAI),
        TokenAmount.from_teu(88_000_000000000000000000, spGNO),
    ],
    "underlyings": [
        TokenAmount.from_teu(-1_000_035_715961244421526907, DAI),
        TokenAmount.from_teu(88_000_000000000000000000, GNO),
    ],
}

expected_position_retro = {
    "holdings": [
        {"address": "0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914", "balance": 1_000_035_715961244421526907},
        {"address": "0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F", "balance": 88_000_000000000000000000},
    ],
    "underlyings": [
        {"address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "balance": -1_000_035_715961244421526907},
        {"address": "0x6810e776880C02933D47DB1b9fc05908e5386b96", "balance": 88_000_000000000000000000},
    ],
}

expected_position_retro_decimal = {
    "holdings": [
        {
            "address": "0xf705d2B7e92B3F38e6ae7afaDAA2fEE110fE5914",
            "balance": Decimal("1_000_035.715961244421526907"),
        },
        {"address": "0x7b481aCC9fDADDc9af2cBEA1Ff2342CB1733E50F", "balance": Decimal("88_000.0")},
    ],
    "underlyings": [
        {"address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "balance": Decimal("-1_000_035.715961244421526907")},
        {"address": "0x6810e776880C02933D47DB1b9fc05908e5386b96", "balance": Decimal("88_000.0")},
    ],
}


def expected_protocol_data(expected_position):
    return {
        "block_id": block_id,
        "blockchain": "ethereum",
        "positions": {"single_position": expected_position},
        "positions_key": None,
        "protocol": "Spark",
        "version": 0,
        "wallet": wallet,
        "financial_metrics": {
            "collateral_ratio": Decimal("1016.357510595627631280679422"),
            "liquidation_ratio": Decimal("400"),
        },
    }


expected_financial_metrics = {
    "collateral_ratio": Decimal("1016.357510595627631280679422"),
    "liquidation_ratio": Decimal("400"),
    "native_token_price_usd": Decimal("1857.8255"),
    "collaterals": [
        {
            "token_address": "0x6810e776880C02933D47DB1b9fc05908e5386b96",
            "token_amount": Decimal("88000.0"),
            "token_price_usd": Decimal("115.48774675"),
        }
    ],
    "debts": [
        {
            "token_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "token_amount": Decimal("1000035.715961244421526907"),
            "token_price_usd": Decimal("0.9999"),
        }
    ],
}


expected_financial_metrics_teu = {
    "collateral_ratio": Decimal("1016.357510595627631280679422"),
    "liquidation_ratio": Decimal("400"),
    "native_token_price_usd": Decimal("1857.8255"),
    "collaterals": [
        {
            "token_address": "0x6810e776880C02933D47DB1b9fc05908e5386b96",
            "token_amount": 88_000_000000000000000000,
            "token_price_usd": Decimal("115.48774675"),
        }
    ],
    "debts": [
        {
            "token_address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "token_amount": 1_000_035_715961244421526907,
            "token_price_usd": Decimal("0.9999"),
        }
    ],
}


@pytest.fixture
def pdp():
    return spark.ProtocolDataProvider(Chain.ETHEREUM, block_id)


decimal = pytest.mark.parametrize("decimal", [False, True], ids=["int", "decimal"])


@decimal
def test_get_protocol_data(decimal):
    ret = spark.get_protocol_data(wallet, block_id, Chain.ETHEREUM, decimals=decimal)
    print()
    pretty.print(ret)
    pretty.jprint(ret)
    expected = expected_protocol_data(expected_position_retro_decimal if decimal else expected_position_retro)
    expected["decimals"] = decimal
    assert ret == expected


def test_underlyings(pdp):
    ret = list(pdp.underlyings(wallet))
    print()
    pretty.print(ret)
    assert ret == expected_position["underlyings"]


def test_holdings(pdp):
    ret = list(pdp.holdings(wallet))
    print()
    pretty.print(ret)
    assert ret == expected_position["holdings"]


@decimal
def test_get_full_financial_metrics(decimal):
    ret = spark.get_full_financial_metrics(wallet, block_id, Chain.ETHEREUM, decimals=decimal)
    print()
    pretty.print(ret)
    pretty.jprint(ret)
    assert ret == expected_financial_metrics if decimal else expected_financial_metrics_teu
