from decimal import Decimal

import pytest

from defyes.constants import Chain
from defyes.lazytime import Time
from defyes.protocols import pods
from defyes.protocols.pods import ChainedPrice
from defyes.types import Addr, Token

wallet = Addr(0x58E6C7AB55AA9012EACCA16D1ED4C15795669E1C)
block_id = 17_772_457  # 2023-07-25 20:21:59 UTC+0000

ethphoria_shares = 49_940_538_321_937_547_614
ethphoria_assets = 50_284_891_309_823_081_976

stETHev = Token.get_instance(0x5FE4B38520E856921978715C8579D2D7A4D2274F, Chain.ETHEREUM)
stETH = Token.get_instance(0xAE7AB96520DE3A18E5E111B5EAAB095312D7FE84, Chain.ETHEREUM)

expected_protocol_data = {
    "blockchain": Chain.ETHEREUM,
    "block_id": block_id,
    "protocol": "Pods",
    "version": 0,
    "wallet": str(wallet),
    "decimals": True,
    "positions": {
        pods.EthphoriaVault.default_addresses[Chain.ETHEREUM]: {
            "underlyings": [{"balance": Decimal("50.284891309823081976"), "address": str(stETH)}],
            "holdings": [{"balance": Decimal("49.940538321937547614"), "address": str(stETHev)}],
        },
    },
    "positions_key": "vault_address",
    "financial_metrics": {
        pods.EthphoriaVault.default_addresses[Chain.ETHEREUM]: {
            "management_fee": Decimal(0),
            "intervals": {
                "current_month": 1.0003212886971298,
                "current_year": None,
                "last_30_days": 1.000130521933334,
                "previous_month": 1.0047870372549657,  # 2023 06 to 07 app.pods.finance (0.479% OK)
            },
        },
        pods.StEthVolatilityVault.default_addresses[Chain.ETHEREUM]: {
            "management_fee": Decimal("0.001"),
            "intervals": {
                "current_month": 1.0015223607819195,
                "current_year": 1.0225490757701234,
                "last_30_days": 1.0016977725506917,
                "previous_month": 1.0023797940711472,  # 2023 06 to 07 app.pods.finance (0.238% OK)
            },
        },
        pods.UsdcFudVault.default_addresses[Chain.ETHEREUM]: {
            "management_fee": Decimal(0),
            "intervals": {
                "current_month": 1.0002621482802374,
                "current_year": None,
                "last_30_days": 1.000114112303449,
                "previous_month": 1.0012340165417097,  # 2023 06 to 07 app.pods.finance (0.184% differs)
                # maybe because it's the first interval
            },
        },
    },
}


@pytest.fixture(params=pods.vault_classes)
def vault(request):
    Vault = request.param
    return Vault(Chain.ETHEREUM, block_id)


def test_balance_of(vault):
    assert vault.balance_of(wallet) == (ethphoria_shares if isinstance(vault, pods.EthphoriaVault) else 0)


def test_get_protocol_data():
    d = pods.get_protocol_data(wallet, block_id)
    assert d == expected_protocol_data


def test_get_protocol_data_latest():
    d = pods.get_protocol_data(wallet, "latest")
    expected = {
        "blockchain": "ethereum",
        "protocol": "Pods",
        "version": 0,
        "wallet": str(wallet),
        "decimals": True,
        "positions_key": "vault_address",
    }
    assert isinstance(d["block_id"], int)
    return all(expected.get(key) == expected.get(key) for key in expected)


def test_underlyings_holdings():
    results = list(pods.underlyings_holdings(wallet, block_id, Chain.ETHEREUM))

    assert isinstance(results[0].vault, pods.StEthVolatilityVault)
    assert results[0].asset_amount == 0
    assert results[0].share_amount == 0

    assert isinstance(results[1].vault, pods.EthphoriaVault)
    assert results[1].asset_amount == "50.284891309823081976" * stETH
    assert results[1].share_amount == "49.940538321937547614" * stETHev

    assert isinstance(results[2].vault, pods.UsdcFudVault)
    assert results[2].asset_amount == 0
    assert results[2].share_amount == 0


def test_usd_fud_vault_aug_rate():
    vault = pods.UsdcFudVault(Chain.ETHEREUM, 18_037_988)
    assert vault.time == Time.from_calendar(2023, 9, 1, 0, 0, 11)
    assert vault.previous_month.initial == ChainedPrice(
        price=Decimal("2.007805"),
        block_id=17_816_434,
        time=Time.from_calendar(2023, 8, 1, 0, 0, 11),
    )
    assert vault.previous_month.final == ChainedPrice(
        price=Decimal("2.040849"),
        block_id=18_037_988,
        time=Time.from_calendar(2023, 9, 1, 0, 0, 11),
    )
    assert vault.previous_month.rate == 1.016457773538765
    assert vault.previous_month.rate.percent == 1.6457773538764986
    assert str(vault.previous_month.rate.percent) == "1.646%"  # Aug 1.629% in app.pods.finance
    assert vault.previous_month.apy == 1.0165224693302266
    assert vault.previous_month.apy.percent == 1.6522469330226608
    assert str(vault.previous_month.apy.percent) == "1.652%"
