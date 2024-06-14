from defyes.protocols.arrakis import get_protocol_data_for


def test_get_protocol_data_for():
    expected_result = {
        "blockchain": "gnosis",
        "block": 34457746,
        "protocol": "Arrakis",
        "positions_key": None,
        "version": 0,
        "wallet": "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f",
        "decimals": "",
        "positions": {
            "0x3889C8B1f064A1A576caB04D5767a00Bf2308bD4": {
                "underlying": [
                    {"address": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1", "balance": 71.3390542200428},
                    {"address": "0xaf204776c7245bF4147c2612BF6e5972Ee483701", "balance": 200443.3714747083},
                ]
            }
        },
    }
    result = get_protocol_data_for(
        "gnosis",
        "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f",
        "0x3889C8B1f064A1A576caB04D5767a00Bf2308bD4",
        block=34457746,
    )
    assert result == expected_result
