from decimal import Decimal

import pytest

from defyes.protocols.dolomite import get_protocol_data_for  # replace with the actual module name


def test_get_protocol_data_for():
    result = get_protocol_data_for("arbitrum", "0xFD322Dd727419D1e437686Ba11ED562F8A8Ad573", 213566930)
    expected = {
        "blockchain": "arbitrum",
        "block": 213566930,
        "protocol": "Dolomite",
        "positions_key": "position_type",
        "version": 0,
        "wallet": "0xFD322Dd727419D1e437686Ba11ED562F8A8Ad573",
        "decimals": 18,
        "positions": {
            "deposits": [],
            "isolation": [
                {
                    "address": "0x1d9E10B161aE54FEAbe1E3F71f658cac3468e3C3",
                    "balance": Decimal("50059.794294912620713906"),
                },
                {
                    "address": "0x912CE59144191C1204E64559FE8253a0e49E6548",
                    "balance": Decimal("-35104.247977908949513039"),
                },
            ],
        },
    }
    assert result == expected


def test_get_protocol_data_for_wrong_blockchain():
    with pytest.raises(ValueError):
        get_protocol_data_for("wrong_blockchain", "0xFD322Dd727419D1e437686Ba11ED562F8A8Ad573", 213566930)
