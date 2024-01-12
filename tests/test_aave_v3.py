from decimal import Decimal

from defabipedia import Chain

from defyes import aavev3

TEST_ADDRESS = "0x849D52316331967b6fF1198e5E32A0eB168D039d"


def test_underlying_all():
    data = aavev3.underlying_all(TEST_ADDRESS, block=17645934, blockchain=Chain.ETHEREUM)
    assert data == {
        "block": 17645934,
        "blockchain": "ethereum",
        "decimals": True,
        "positions": {
            "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599": {
                "holdings": [
                    {"address": "0x5Ee5bf7ae06D1Be5997A1A72006FE6C607eC6DE8", "balance": Decimal("0")},
                    {"address": "0xA1773F1ccF6DB192Ad8FE826D15fe1d328B03284", "balance": Decimal("0")},
                    {"address": "0x40aAbEf1aa8f0eEc637E0E7d92fbfFB2F26A8b7B", "balance": Decimal("25.34428395")},
                ],
                "underlying": [
                    {"address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", "balance": Decimal("-25.34428395")}
                ],
            },
            "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0": {
                "holdings": [
                    {
                        "address": "0x0B925eD163218f6662a35e0f0371Ac234f9E9371",
                        "balance": Decimal("1254.646812557225928204"),
                    },
                    {"address": "0x39739943199c0fBFe9E5f1B5B160cd73a64CB85D", "balance": Decimal("0")},
                    {"address": "0xC96113eED8cAB59cD8A66813bCB0cEb29F06D2e4", "balance": Decimal("0")},
                ],
                "underlying": [
                    {
                        "address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
                        "balance": Decimal("1254.646812557225928204"),
                    }
                ],
            },
        },
        "positions_key": "underlying_token_address",
        "protocol": "Aave v3",
        "version": 0,
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
    }


def test_get_data():
    data = aavev3.get_data(TEST_ADDRESS, block=17645934, blockchain=Chain.ETHEREUM)
    assert data == {
        "collateral_ratio": Decimal("345.39002674115403124233125708997249603271484375"),
        "collaterals": [
            {
                "token_address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
                "token_amount": Decimal("1254.646812557225928204"),
                "token_price_usd": Decimal("2114.16013635"),
            }
        ],
        "debts": [
            {
                "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "token_amount": Decimal("25.34428395"),
                "token_price_usd": Decimal("30301.87823323"),
            }
        ],
        "liquidation_ratio": Decimal("125"),
        "native_token_price_usd": Decimal("1869.01357"),
    }
