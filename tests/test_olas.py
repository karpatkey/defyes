from defyes.protocols.olas import get_protocol_data_for


def test_get_protocol_data_for():
    expected_result = {
        "blockchain": "ethereum",
        "block": 20062359,
        "protocol": "Olas",
        "positions_key": None,
        "version": 0,
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
        "decimals": "",
        "positions": {
            "veOLAS": {
                "holdings": [{"address": "0x7e01A500805f8A52Fad229b3015AD130A332B7b3", "balance": 6000000.0}],
                "underlyings": [{"address": "0x0001A500A6B18995B03f44bb040A5fFc28E45CB0", "balance": 6000000.0}],
            }
        },
    }
    result = get_protocol_data_for("ethereum", "0x849d52316331967b6ff1198e5e32a0eb168d039d", 20062359)
    assert result == expected_result
