from decimal import Decimal

from defyes import Aave
from defyes.constants import ETHEREUM, ETHTokenAddr

STK_AAVE = "0x4da27a545c0c5B758a6BA100e3a049001de870f5"
STK_ABPT = "0xa1116930326D21fB917d5A27F1E9943A9595fb47"
TEST_ADDRESS = "0xf929122994e177079c924631ba13fb280f5cd1f9"


def test_get_staking_balance():
    data = Aave.get_staked(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == [[ETHTokenAddr.AAVE, Decimal("11538.124991799179534465")], [ETHTokenAddr.ABPT, Decimal("0.0")]]


def test_get_apr():
    data = Aave.get_apr(ETHTokenAddr.DAI, block=16870553, blockchain=ETHEREUM)
    assert data == [
        {"metric": "apr", "type": "supply", "value": Decimal("0.003538039323536510307201982")},
        {"metric": "apr", "type": "variable_borrow", "value": Decimal("0.013718667484985489509565151")},
        {"metric": "apr", "type": "stable_borrow", "value": Decimal("0.106859333742492744754782576")},
    ]


def test_get_staking_apr():
    data = Aave.get_staking_apr(block=16870553, blockchain=ETHEREUM)
    assert data == [{"metric": "apr", "type": "staking", "value": Decimal("0.06083395929558314368366087980")}]


def test_underlying_all():
    data = Aave.underlying_all(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == [
        ["0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599", Decimal("-141.35367794")],
        ["0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F", Decimal("76289.38833267227462272")],
        ["0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", Decimal("-291.885786")],
        ["0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272", Decimal("351227.566030802369010452")],
        ["0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84", Decimal("6612.667414298343784257")],
    ]


def test_get_data():
    data = Aave.get_data(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == {
        "collateral_ratio": Decimal("315.204129806536684554885141551494598388671875"),
        "liquidation_ratio": Decimal("122.2792858889704084128148692"),
        "eth_price_usd": Decimal("1756.2"),
        "collaterals": [
            {
                "token_address": "0xC011a73ee8576Fb46F5E1c5751cA3B9Fe0af2a6F",
                "token_amount": Decimal("76289.38833267227462272"),
                "token_price_usd": Decimal("3.0891558"),
            },
            {
                "token_address": "0x8798249c2E607446EfB7Ad49eC89dD1865Ff4272",
                "token_amount": Decimal("351227.566030802369010452"),
                "token_price_usd": Decimal("1.6009054059164451174"),
            },
            {
                "token_address": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                "token_amount": Decimal("6612.667414298343784257"),
                "token_price_usd": Decimal("1752.87732205667435028"),
            },
        ],
        "debts": [
            {
                "token_address": "0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599",
                "token_amount": Decimal("141.35367794"),
                "token_price_usd": Decimal("27804.1952802"),
            },
            {
                "token_address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "token_amount": Decimal("291.885786"),
                "token_price_usd": Decimal("0.9937854059046764532"),
            },
        ],
    }


def test_get_all_rewards():
    data = Aave.get_all_rewards(TEST_ADDRESS, block=16870553, blockchain=ETHEREUM)
    assert data == [["0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9", Decimal("83.888023084390214623")]]
