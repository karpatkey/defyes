from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import GnosisTokenAddr
from karpatkit.node import get_node

from defyes import Agave
from defyes.functions import get_contract

STK_AGAVE = "0x610525b415c1BFAeAB1a3fc3d85D87b92f048221"
TEST_WALLET_ADDRESS = "0xc4d46395c01aa86389d4216c2830167878d7cab8"
UNUSED_ADDRESS = "0xcafe6395c01aa86389d4216c2830167878d7cab8"

TEST_BLOCK = 27187881
# 2023.04.14
# TEST_BLOCK = 27450341

WEB3 = get_node(blockchain=Chain.GNOSIS)

# 2023.03.29
TOP_WALLET_ADDRESS = "0xb4c575308221caa398e0dd2cdeb6b2f10d7b000a"
TOP_WALLET_W = [
    ["0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83", 129855918919],
    ["0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d", 204984404799221030364433],
    ["0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2", 116756629133928213523],
    ["0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb", 816596478974281580761],
    ["0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252", 20774443],
    ["0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1", 282650106097633403696],
    ["0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d", 4922397761223675816108],
    ["0x4ECaBa5870353805a9F068101A40E0f32ed605C6", 149615952],
]
# TODO: use descriptive constants

# 2023.04.14
GNOSIS_SAFE_IN_GNO = "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f"
GNOSIS_SAFE_UNDERLYING_ALL_WITH_REWARDS = [
    ["0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83", Decimal("861490609530")],
    ["0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d", Decimal("2861467152146117938998419")],
    ["0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb", Decimal("5004431568185442780597")],
    ["0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1", Decimal("552005140092550220243")],
    ["0x4ECaBa5870353805a9F068101A40E0f32ed605C6", Decimal("311298154329")],
    ["0x3a97704a1b25F08aa230ae53B352e2e72ef52843", Decimal("0")],
]

# TODO: use descriptive constants
GNOSIS_SAFE_DATA = {
    "collateral_ratio": Decimal("Infinity"),
    "liquidation_ratio": Decimal("127.0486596366408334392072164"),
    "xdai_price_usd": Decimal("0.99974566"),
    "collaterals": [
        {
            "token_address": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
            "token_amount": Decimal("861490.60953"),
            "token_price_usd": Decimal("0.99985874999999999944370486"),
        },
        {
            "token_address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
            "token_amount": Decimal("2861467.152146117938998419"),
            "token_price_usd": Decimal("0.99974566"),
        },
        {
            "token_address": "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb",
            "token_amount": Decimal("5004.431568185442780597"),
            "token_price_usd": Decimal("112.4299999999999999994793535"),
        },
        {
            "token_address": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
            "token_amount": Decimal("552.005140092550220243"),
            "token_price_usd": Decimal("1790.096799999999999999143554"),
        },
        {
            "token_address": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
            "token_amount": Decimal("311298.154329"),
            "token_price_usd": Decimal("1.00050699999999999942231082"),
        },
    ],
    "debts": [],
}

# https://gnosisscan.io/address/0x24dcbd376db23e4771375092344f5cbea3541fc0#readContract
# getAllReservesTokens
# 2023.03.29
RESERVES_TOKENS = [
    ("USDC", "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83"),
    ("WXDAI", "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d"),
    ("LINK", "0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2"),
    ("GNO", "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb"),
    ("WBTC", "0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252"),
    ("WETH", "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1"),
    ("FOX", "0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d"),
    ("USDT", "0x4ECaBa5870353805a9F068101A40E0f32ed605C6"),
    ("EURe", "0xcB444e90D8198415266c6a2724b7900fb12FC56E"),
]
# TODO: use descriptive constants


def test_get_reserves_tokens():
    pdp_contract = get_contract(Agave.PDP_GNOSIS, Chain.GNOSIS, web3=WEB3, abi=Agave.ABI_PDP)
    reserves_tokens = Agave.get_reserves_tokens(pdp_contract, TEST_BLOCK)
    assert reserves_tokens == [e[1] for e in RESERVES_TOKENS]


def test_get_reserves_tokens_balances():
    balances = Agave.get_reserves_tokens_balances(WEB3, TOP_WALLET_ADDRESS, TEST_BLOCK, Chain.GNOSIS, decimals=False)
    assert balances == TOP_WALLET_W


def test_get_data():
    data = Agave.get_data(GNOSIS_SAFE_IN_GNO, TEST_BLOCK, Chain.GNOSIS, web3=WEB3)
    assert data == GNOSIS_SAFE_DATA


def test_get_all_rewards():
    all_rewards = Agave.get_all_rewards(TEST_WALLET_ADDRESS, TEST_BLOCK, Chain.GNOSIS, web3=WEB3, decimals=True)
    assert all_rewards == [["0x3a97704a1b25F08aa230ae53B352e2e72ef52843", Decimal("14.334056377962964551")]]


@pytest.mark.parametrize("reward", [True, False])
def test_underlying_all(reward, decimals=False):
    # TODO: maybe test for decimals=True
    ua = Agave.underlying_all(GNOSIS_SAFE_IN_GNO, TEST_BLOCK, Chain.GNOSIS, web3=WEB3, reward=reward, decimals=decimals)
    # print(f'for {reward = } and {decimals = }: {ua}')
    expected = GNOSIS_SAFE_UNDERLYING_ALL_WITH_REWARDS
    if not reward:
        expected = expected[:-1]
    assert ua == expected


@pytest.mark.parametrize("apy", [True, False])
def test_get_apr(apy):
    TOKEN_ADDRESS = "0x3a97704a1b25F08aa230ae53B352e2e72ef52843"
    apr = Agave.get_apr(TOKEN_ADDRESS, TEST_BLOCK, Chain.GNOSIS, web3=WEB3, apy=apy)
    # FIXME: make this more interesting:
    assert (
        apr
        == {
            True: [
                {"metric": "apy", "type": "supply", "value": Decimal("0")},
                {"metric": "apy", "type": "variable_borrow", "value": Decimal("0")},
                {"metric": "apy", "type": "stable_borrow", "value": Decimal("0")},
            ],
            False: [
                {"metric": "apr", "type": "supply", "value": Decimal("0")},
                {"metric": "apr", "type": "variable_borrow", "value": Decimal("0")},
                {"metric": "apr", "type": "stable_borrow", "value": Decimal("0")},
            ],
        }[apy]
    )


# FIXME: This test seems to depend on fluctuating values
@pytest.mark.parametrize("apy", [True, False])
def test_get_staking_apr(apy):
    stk_apr = Agave.get_staking_apr(TEST_BLOCK, Chain.GNOSIS, web3=WEB3, apy=apy)
    assert (
        stk_apr
        == {
            True: [{"metric": "apy", "type": "staking", "value": Decimal("0.127412720014978996749268306")}],
            False: [{"metric": "apr", "type": "staking", "value": Decimal("0.1199253794401285060793250841")}],
        }[apy]
    )


@pytest.mark.parametrize("wallet_address", [TEST_WALLET_ADDRESS, UNUSED_ADDRESS])
@pytest.mark.parametrize("decimals", [True, False])
def test_get_staked(wallet_address, decimals):
    expected = {
        TEST_WALLET_ADDRESS: Decimal("103630383543378402291") / Decimal(10**18 if decimals else 1),
        UNUSED_ADDRESS: 0,
    }[wallet_address]

    data = Agave.get_staked(wallet_address, block=TEST_BLOCK, blockchain=Chain.GNOSIS, web3=WEB3, decimals=decimals)
    assert data == [[GnosisTokenAddr.AGVE, expected]]


def test_get_agave_tokens():
    blockchain = Chain.GNOSIS
    block = 28471737
    assert Agave.get_agave_tokens(blockchain, block) == [
        {
            "underlying": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
            "interest bearing": "0x291B5957c9CBe9Ca6f0b98281594b4eB495F4ec1",
            "stable debt": "0x05c43e14d38bC5123F6408A57BE03714aB689F6e",
            "variable debt": "0xa728C8f1CF7fC4d8c6d5195945C3760c87532724",
        },
        {
            "underlying": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
            "interest bearing": "0xd4e420bBf00b0F409188b338c5D87Df761d6C894",
            "stable debt": "0xF4401355B41c867edbF09C821FA7B4fffbed5C82",
            "variable debt": "0xec72De30C3084023F7908002A2252a606CCe0B2c",
        },
        {
            "underlying": "0xE2e73A1c69ecF83F464EFCE6A5be353a37cA09b2",
            "interest bearing": "0xa286Ce70FB3a6269676c8d99BD9860DE212252Ef",
            "stable debt": "0x4f9401Fb52fe53de977dcbF05A0F6237AaDC7Eb1",
            "variable debt": "0x5b0568531322759EAB69269a86448b39B47e2AE8",
        },
        {
            "underlying": "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb",
            "interest bearing": "0xA26783eAd6C1f4744685c14079950622674ae8A8",
            "stable debt": "0x0DfD401903bA960B2EED32A10f8aeB601Cd9A7A5",
            "variable debt": "0x99272C6E2Baa601cEA8212b8fBAA7920A9f916F0",
        },
        {
            "underlying": "0x8e5bBbb09Ed1ebdE8674Cda39A0c169401db4252",
            "interest bearing": "0x4863cfaF3392F20531aa72CE19E5783f489817d6",
            "stable debt": "0xca0f3B157165FE11692a047ea14963ffAdfB31fD",
            "variable debt": "0x110C5A1494F0AB6C851abB72AA2efa3dA738aB72",
        },
        {
            "underlying": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
            "interest bearing": "0x44932e3b1E662AdDE2F7bac6D5081C5adab908c6",
            "stable debt": "0x43Ae4A9474eA23b0BC04C99F9fF2A9B4c2d5554c",
            "variable debt": "0x73Ada33D706085d6B93350B5e6aED6178905Fb8A",
        },
        {
            "underlying": "0x21a42669643f45Bc0e086b8Fc2ed70c23D67509d",
            "interest bearing": "0xA916A4891D80494c6cB0B49b11FD68238AAaF617",
            "stable debt": "0x6Ca958336e7A1BDCDf7762aeb81613EaDdCc3110",
            "variable debt": "0x7388cbdeb284902E1e07be616F92Adb3660Ed3a4",
        },
        {
            "underlying": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
            "interest bearing": "0x5b4Ef67c63d091083EC4d30CFc4ac685ef051046",
            "stable debt": "0xB067faD853d099EDd9c86483682e7D947B7983E5",
            "variable debt": "0x474f83d77150bDDC6a6F34eEe4F5574EAfD05938",
        },
        {
            "underlying": "0xcB444e90D8198415266c6a2724b7900fb12FC56E",
            "interest bearing": "0xEB20B07a9abE765252E6b45e8292b12CB553CcA6",
            "stable debt": "0x78A69aFc50E7705Ad4588cB57cF8D27B29161e51",
            "variable debt": "0xA4a45B550897dD5d8a44c68DBD245C5934EbAcd9",
        },
        {
            "underlying": "0x6C76971f98945AE98dD7d4DFcA8711ebea946eA6",
            "interest bearing": "0x606B2689ba4A9F798f449fa6495186021486dD9f",
            "stable debt": "0xeC7f91f26E7fD42E90fFa53ca0B0b02095A6B450",
            "variable debt": "0xd0b168FD6a4e220f1a8FA99De97F8f428587e178",
        },
    ]


@pytest.mark.parametrize("decimals", [True, False])
def test_get_extra_rewards(decimals):
    block = 25830991
    blockchain = Chain.GNOSIS
    wallet = "0x458cD345B4C05e8DF39d0A07220feb4Ec19F5e6f"
    assert Agave.get_extra_rewards(wallet, block, blockchain, decimals=decimals) == [
        [
            "0x870Bb2C024513B5c9A69894dCc65fB5c47e422f3",
            Decimal("150.738302841301982923") if decimals else Decimal("150738302841301982923"),
        ]
    ]
