from decimal import Decimal

from defabipedia import Chain

from defyes import aavev3

TEST_ADDRESS_ETH = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
TEST_ADDRESS_OP = "0xb2289e329d2f85f1ed31adbb30ea345278f21bcf"
TEST_ADDRESS_POL = "0xe8599f3cc5d38a9ad6f3684cd5cea72f10dbc383"
TEST_ADDRESS_AVAX = "0x5ba7fd868c40c16f7adfae6cf87121e13fc2f7a0"
TEST_ADDRESS_METIS = "0xb5b64c7e00374e766272f8b442cd261412d4b118"


def test_underlying_all():
    data = aavev3.underlying_all(TEST_ADDRESS_ETH, block=17645934, blockchain=Chain.ETHEREUM)
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
    data = aavev3.get_data(TEST_ADDRESS_ETH, block=17645934, blockchain=Chain.ETHEREUM)
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


def test_get_all_rewards_opt():
    data = aavev3.get_all_rewards(TEST_ADDRESS_OP, block=117635043, blockchain=Chain.OPTIMISM)
    assert data == [["0x4200000000000000000000000000000000000042", Decimal("1184.97911595167452278")]]


def test_get_all_rewards_pol():
    data = aavev3.get_all_rewards(TEST_ADDRESS_POL, block=54837791, blockchain=Chain.POLYGON)
    assert data == [
        ["0x1d734A02eF1e1f5886e66b0673b71Af5B53ffA94", Decimal("0.654462508016313944")],
        ["0xC3C7d422809852031b44ab29EEC9F1EfF2A58756", Decimal("1.547537980607527448")],
        ["0x3A58a54C066FdC0f2D55FC9C89F0415C92eBf3C4", Decimal("0")],
        ["0xfa68FB4628DFF1028CFEc22b4162FCcd0d45efb6", Decimal("0")],
    ]


def test_get_all_rewards_avax():
    data = aavev3.get_all_rewards(TEST_ADDRESS_AVAX, block=43011322, blockchain=Chain.AVALANCHE)
    assert data == [["0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7", Decimal("1508.826587369953482126")]]


def test_get_all_rewards_metis():
    data = aavev3.get_all_rewards(TEST_ADDRESS_METIS, block=14328262, blockchain=Chain.METIS)
    assert data == [["0xDeadDeAddeAddEAddeadDEaDDEAdDeaDDeAD0000", Decimal("0.241803989707412017")]]
