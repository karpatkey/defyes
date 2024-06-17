from defyes.protocols.opus_pool import get_protocol_data_for

block = 20114053
blockchain = "ethereum"
wallet = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
address = "0xe6d8d8aC54461b1C5eD15740EEe322043F696C08"


def test_get_protocol_data_for():
    expected_result = {
        "blockchain": "ethereum",
        "block": 20114053,
        "protocol": "Opus Pool",
        "positions_key": "token_vault",
        "version": 0,
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
        "decimals": "",
        "positions": {
            "ETH": {
                "underlyings": [
                    {"address": "0x0000000000000000000000000000000000000000", "balance": 2011.4699299708243}
                ]
            }
        },
    }
    result = get_protocol_data_for(
        "ethereum", "0x849d52316331967b6ff1198e5e32a0eb168d039d", "0xe6d8d8aC54461b1C5eD15740EEe322043F696C08", 20114053
    )
    assert result == expected_result
