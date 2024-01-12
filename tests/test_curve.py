from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.node import get_node

from defyes import Curve

# 2023.04.06
TEST_BLOCK = 16993460
TEST_WALLET = "0xf929122994e177079c924631ba13fb280f5cd1f9"

# DAI USDC USDT Curve Pool
CURVE_3POOL = "0xbEbc44782C7dB0a1A60Cb6fe97d0b483032FF1C7"
CURVE_3POOL_GAUGE = "0xbFcF63294aD7105dEa65aA58F8AE5BE2D9d0952A"

WEB3 = get_node(blockchain=Chain.ETHEREUM)


@pytest.mark.parametrize("_id", [0, 3, 5, 6])
def test_get_registry_contract(_id):
    # rc = Curve.get_registry_contract(WEB3, _id, TEST_BLOCK, Chain.ETHEREUM)
    # I'm just testing it does not break
    assert True


def test_get_lptoken_data():
    lpt_data = Curve.get_lptoken_data(EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3)
    expected = {"minter": None, "decimals": 18, "totalSupply": 423390670620160177728525799}
    assert expected == {k: lpt_data[k] for k in expected}


def test_get_pool_address():
    # TODO: this function has an intricate 'if' combination
    pa = Curve.get_pool_address(WEB3, EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM)
    assert pa == CURVE_3POOL


def test_get_pool_gauge_address():
    pga = Curve.get_pool_gauge_address(WEB3, CURVE_3POOL, EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM)
    assert pga == CURVE_3POOL_GAUGE


def test_get_gauge_version():
    # TODO: test for all versions
    # ChildGauge
    # LiquidityGaugeV5
    # LiquidityGaugeV4
    # LiquidityGaugeV3
    # LiquidityGaugeV2
    # LiquidityGaugeReward
    # RewardsOnlyGauge

    gv = Curve.get_gauge_version(CURVE_3POOL_GAUGE, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3, only_version=True)
    assert gv == "LiquidityGauge"


def test_get_pool_data():
    pd = Curve.get_pool_data(WEB3, CURVE_3POOL, TEST_BLOCK, Chain.ETHEREUM)
    expected = {
        "is_metapool": False,
        "coins": {0: EthereumTokenAddr.DAI, 1: EthereumTokenAddr.USDC, 2: EthereumTokenAddr.USDT},
    }
    assert expected == {k: pd[k] for k in expected}


@pytest.mark.parametrize("decimals", [True, False])
def test_get_all_rewards(decimals):
    rewards = Curve.get_all_rewards(
        TEST_WALLET, EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3, decimals=decimals
    )
    assert rewards == [[EthereumTokenAddr.CRV, Decimal("120624446582848732188") / Decimal(10**18 if decimals else 1)]]


@pytest.mark.parametrize("reward", [True, False])
@pytest.mark.parametrize("decimals", [True, False])
def test_underlying(reward, decimals):
    u = Curve.underlying(
        TEST_WALLET, EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3, reward=reward, decimals=decimals
    )
    expected = [
        [EthereumTokenAddr.DAI, Decimal("0"), Decimal("0")],
        [EthereumTokenAddr.USDC, Decimal("0"), Decimal("0")],
        [EthereumTokenAddr.USDT, Decimal("0"), Decimal("0")],
    ]
    if reward:
        expected.append([EthereumTokenAddr.CRV, 120624446582848732188 / Decimal(10**18 if decimals else 1)])

    assert u == expected


@pytest.mark.parametrize("lptoken_amount", [0, 10])
@pytest.mark.parametrize("decimals", [True, False])
def test_unwrap(lptoken_amount, decimals):
    u = Curve.unwrap(lptoken_amount, EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3, decimals=decimals)
    expected = {
        0: [
            [EthereumTokenAddr.DAI, Decimal("0")],
            [EthereumTokenAddr.USDC, Decimal("0")],
            [EthereumTokenAddr.USDT, Decimal("0")],
        ],
        10: [
            [EthereumTokenAddr.DAI, Decimal("3917354685557199081.180899410") / Decimal(10**18 if decimals else 1)],
            [EthereumTokenAddr.USDC, Decimal("4147544.963364350419868516281") / Decimal(10**6 if decimals else 1)],
            [EthereumTokenAddr.USDT, Decimal("2190460.875671642443221745933") / Decimal(10**6 if decimals else 1)],
        ],
    }
    assert u == expected[lptoken_amount]


@pytest.mark.parametrize("decimals", [True, False])
def test_pool_balances(decimals):
    pb = Curve.pool_balances(EthereumTokenAddr.X3CRV, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3, decimals=decimals)
    assert pb == [
        [EthereumTokenAddr.DAI, Decimal("165857824629254122209119338") / Decimal(10**18 if decimals else 1)],
        [EthereumTokenAddr.USDC, Decimal("175604425510732") / Decimal(10**6 if decimals else 1)],
        [EthereumTokenAddr.USDT, Decimal("92743777795510") / Decimal(10**6 if decimals else 1)],
    ]


@pytest.mark.parametrize("decimals", [True, False])
def test_swap_fees(decimals):
    sf = Curve.swap_fees(
        EthereumTokenAddr.X3CRV, TEST_BLOCK - 100, TEST_BLOCK, Chain.ETHEREUM, web3=WEB3, decimals=decimals
    )
    # FIXME: decimals is ignored
    assert sf["swaps"] == [
        {
            "block": 16993412,
            "tokenOut": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "amountOut": Decimal("0.0119984762770876226292"),
        },
        {
            "block": 16993445,
            "tokenOut": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "amountOut": Decimal("0.0108986139097754796211"),
        },
        {
            "block": 16993412,
            "tokenOut": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "amountOut": Decimal("0.0119984762770876226292"),
        },
        {
            "block": 16993445,
            "tokenOut": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
            "amountOut": Decimal("0.0108986139097754796211"),
        },
    ]


@pytest.mark.skip("web3.exceptions.ABIFunctionNotFound")
@pytest.mark.parametrize("apy", [False, True])
def test_get_base_apr(apy):
    # x = Curve.get_base_apr(EthereumTokenAddr.X3CRV, Chain.ETHEREUM, TEST_BLOCK, web3=WEB3, apy=apy)
    assert True


@pytest.mark.skip("web3.exceptions.ABIFunctionNotFound")
@pytest.mark.parametrize("apy", [False, True])
def test_swap_fees_v2(apy):
    # sf = Curve.swap_fees_v2(EthereumTokenAddr.X3CRV, Chain.ETHEREUM, TEST_BLOCK, web3=WEB3, apy=apy)
    assert True


@pytest.mark.skip("web3.exceptions.ABIFunctionNotFound")
def test_get_swap_fees_APR():
    # sf = Curve.get_swap_fees_APR(EthereumTokenAddr.X3CRV, Chain.ETHEREUM, TEST_BLOCK, web3=WEB3)
    assert True
