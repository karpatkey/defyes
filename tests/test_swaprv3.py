from decimal import Decimal

from defyes.protocols.swaprv3 import get_protocol_data_for


def test_get_protocol_data_for():
    result = get_protocol_data_for(
        "gnosis", "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f", "0x91fD594c46D8B01E62dBDeBed2401dde01817834", 33972817
    )
    expected_result = {
        "blockchain": "gnosis",
        "block": 33972817,
        "protocol": "SwaprV3",
        "positions_key": "nft_id",
        "version": 3,
        "wallet": "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f",
        "decimals": 18,
        "positions": {
            172: {
                "underlyings": [
                    {
                        "address": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
                        "balance": Decimal("104.4126228581047671520043737"),
                    },
                    {
                        "address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
                        "balance": Decimal("190875.8622433801857079584968"),
                    },
                ],
                "holdings": {"address": "0x91fD594c46D8B01E62dBDeBed2401dde01817834", "balance": 1},
                "rewards": [
                    {
                        "address": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
                        "balance": Decimal("1.494714104077160171135150133"),
                    },
                    {
                        "address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
                        "balance": Decimal("4646.554299626385230113753693"),
                    },
                ],
            }
        },
    }
    assert result == expected_result
