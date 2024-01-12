from decimal import Decimal

import pytest
from defabipedia import Chain

from defyes import Angle

agEUR = "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8"
WALLET = "0x849D52316331967b6fF1198e5E32A0eB168D039d"


def test_angle_treasury():
    block = 17451062

    t = Angle.Treasury(Chain.ETHEREUM, block)
    assert t.stablecoin == agEUR
    assert [
        "0x241D7598BD1eb819c0E9dEd456AcB24acA623679",
        "0x1beCE8193f8Dc2b170135Da9F1fA8b81C7aD18b1",
        "0x73aaf8694BA137a7537E7EF544fcf5E2475f227B",
        "0x8E2277929B2D849c0c344043D9B9507982e6aDd0",
        "0xdEeE8e8a89338241fe622509414Ff535fB02B479",
        "0x0652B4b3D205300f9848f0431296D67cA4397f3b",
        "0xE1C084e6E2eC9D32ec098e102a73C4C27Eb9Ee58",
        "0x0B3AF9fb0DE42AE70432ABc5aaEaB8F9774bf87b",
        "0x989ed2DDCD4D2DC237CE014432aEb40EfE738E31",
        "0x29e9D3D8e295E23B1B39DCD3D8D595761E032306",
        "0xe0C8B6c4ea301C8A221E8838ca5B80Ac76E7A10b",
        "0x913E8e1eD659C27613E937a6B6119b91D985094c",
        "0x96de5c30F2BF4683c7903F3e921F720602F8868A",
    ] == t.get_all_vault_managers_addrs()


@pytest.mark.parametrize("decimals", [True, False])
def test_protocol_data(decimals):
    block = 17451062
    underlying = Angle.get_protocol_data(Chain.ETHEREUM, WALLET, block, decimals=decimals)
    assert {
        "block_id": 17451062,
        "wallet": WALLET,
        "blockchain": "ethereum",
        "positions": {
            "19": {
                "financial_metrics": {
                    "anual_interest_rate": Decimal("0.004987542475021200498864000"),
                    "available_to_borrow": {
                        "address": "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8",
                        "balance": Decimal("431692.91115667917318028225")
                        if decimals
                        else Decimal("431692911156679173180282.2500"),
                    },
                    "collateral_ratio": Decimal("3.684106784023604012084994729"),
                    "liquidation_price_in_stablecoin_fiat": Decimal("642.5954462304000723178755981"),
                    "liquidation_ratio": Decimal("1.298701298701298701298701299"),
                },
                "liquidity": {
                    "underlyings": [
                        {
                            "address": "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8",
                            "balance": Decimal("-235029.284458768826450263") if decimals else -235029284458768826450263,
                        },
                        {
                            "address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
                            "balance": Decimal("475") if decimals else 475000000000000000000,
                        },
                    ]
                },
            }
        },
        "positions_key": "vault_id",
        "protocol": "Angle",
        "version": 0,
    } == underlying
