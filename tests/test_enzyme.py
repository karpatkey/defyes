from decimal import Decimal

from defyes.protocols.enzyme import get_protocol_data_for


def test_get_protocol_data_for():
    blockchain = "ethereum"
    wallet = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
    block = 20169638
    position_identifier = "0x1ce8aAfb51e79F6BDc0EF2eBd6fD34b00620f6dB"
    decimals = True

    expected_output = {
        "blockchain": "ethereum",
        "block": 20169638,
        "protocol": "Enzyme",
        "positions_key": "vault_address",
        "version": 0,
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
        "decimals": "",
        "positions": {
            "0x1ce8aAfb51e79F6BDc0EF2eBd6fD34b00620f6dB": {
                "underlyings": [
                    {
                        "address": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                        "balance": Decimal("3086.226878579833721778809843"),
                    }
                ],
                "holdings": [{"address": "0x1ce8aAfb51e79F6BDc0EF2eBd6fD34b00620f6dB", "balance": 3007.5677264584024}],
            }
        },
    }

    assert get_protocol_data_for(blockchain, wallet, position_identifier, block, decimals) == expected_output
