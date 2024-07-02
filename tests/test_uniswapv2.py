from decimal import Decimal

from defyes.protocols.uniswapv2 import get_data_protocol_for


def test_get_data_protocol_for():
    result = get_data_protocol_for(
        "0xd28b432f06cb64692379758b88b5fcdfc4f56922", "0x2e7E978DA0C53404a8cf66ED4bA2c7706C07B62a", 19825299, "ethereum"
    )
    expected_result = {
        "blockchain": "ethereum",
        "block": 19825299,
        "protocol": "Uniswap V2",
        "positions_key": "lptoken_address",
        "version": 0,
        "wallet": "0xd28b432f06cb64692379758b88b5fcdfc4f56922",
        "decimals": 18,
        "positions": {
            "0x2e7E978DA0C53404a8cf66ED4bA2c7706C07B62a": {
                "holdings": {"address": "0x2e7E978DA0C53404a8cf66ED4bA2c7706C07B62a", "balance": 1007.1749934555891},
                "underlyings": [
                    {
                        "address": "0x5aFE3855358E112B5647B952709E6165e1c1eEEe",
                        "balance": Decimal("44364.48187350472406954723140"),
                    },
                    {
                        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                        "balance": Decimal("25.05146163026574108391083987"),
                    },
                ],
            }
        },
    }
    assert result == expected_result, "get_data_protocol_for did not return the expected result"
