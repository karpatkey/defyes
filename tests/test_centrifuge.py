from decimal import Decimal

from defyes.protocols.centrifuge import Chain, get_protocol_data_for


def test_get_protocol_data_for():
    expected_result = {
        "blockchain": "ethereum",
        "block": 20089547,
        "protocol": "Centrifuge",
        "positions_key": "lp_token",
        "version": 0,
        "wallet": "0x2923c1B5313F7375fdaeE80b7745106deBC1b53E",
        "decimals": "",
        "positions": {
            "0xB3AC09cd5201569a821d87446A4aF1b202B10aFd": {
                "holdings": {
                    "address": "0x30baA3BA9D7089fD8D020a994Db75D14CF7eC83b",
                    "balance": Decimal("1961178.818477"),
                },
                "underlying": {"address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", "balance": 1990508.617719},
            }
        },
    }
    result = get_protocol_data_for(
        Chain.ETHEREUM,
        "0x2923c1b5313f7375fdaee80b7745106debc1b53e",
        "0xB3AC09cd5201569a821d87446A4aF1b202B10aFd",
        block=20089547,
    )
    assert result == expected_result
