from decimal import Decimal

from defyes.protocols.sommelier import get_protocol_data_for


def test_get_protocol_data_for():
    blockchain = "ethereum"
    wallet = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
    position_identifier = "0x6c1edce139291Af5b84fB1e496c9747F83E876c9"
    block = 20168299

    expected_output = {
        "blockchain": "ethereum",
        "block": 20168299,
        "protocol": "Sommelier",
        "positions_key": "vault_address",
        "version": 0,
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
        "decimals": "",
        "positions": {
            "0x6c1edce139291Af5b84fB1e496c9747F83E876c9": {
                "underlyings": [
                    {
                        "address": "0xae78736Cd615f374D3085123A210448E74Fc6393",
                        "balance": Decimal("68.96354428592041708625285217"),
                    },
                    {
                        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                        "balance": Decimal("78.56737050333764450317058569"),
                    },
                ],
                "holdings": [{"address": "0x6c1edce139291Af5b84fB1e496c9747F83E876c9", "balance": 150.0}],
            }
        },
    }

    assert get_protocol_data_for(blockchain, wallet, position_identifier, block, decimals=True) == expected_output
