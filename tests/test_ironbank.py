from decimal import Decimal

import pytest

from defyes import IronBank
from defyes.constants import OPTIMISM
from defyes.functions import get_node

# 2023.04.27
TEST_BLOCK = 94882677
TEST_WALLET = "0x5eD64f02588C8B75582f2f8eFd7A5521e3F897CC"
WEB3 = get_node(blockchain=OPTIMISM, block=TEST_BLOCK)

iUSDC = "0x1d073cf59Ae0C169cbc58B6fdD518822ae89173a"
USDC = "0x7F5c764cBc14f9669B88837ca1490cCa17c31607"
IB = "0x00a35FD824c717879BF370E70AC6868b95870Dfb"
veIB = "0x707648dfbF9dF6b0898F78EdF191B85e327e0e05"


def test_get_itoken_data():
    data = IronBank.get_itoken_data(iUSDC, TEST_WALLET, TEST_BLOCK, OPTIMISM, WEB3, None)
    expected = {
        "underlying": USDC,
        "decimals": 8,
        "borrowBalanceStored": 0,
        "balanceOf": 37470207787145,
        "exchangeRateStored": 101609986612647,
    }
    assert {k: data[k] for k in expected} == expected


@pytest.mark.parametrize("decimals", [True, False])
def test_get_all_rewards(decimals):
    x = IronBank.get_all_rewards(TEST_WALLET, iUSDC, TEST_BLOCK, OPTIMISM, WEB3, decimals=decimals)
    assert x == [[IB, Decimal("0")]]


@pytest.mark.parametrize("decimals", [True, False])
def test_all_rewards(decimals):
    x = IronBank.all_rewards(TEST_WALLET, TEST_BLOCK, OPTIMISM, WEB3, decimals=decimals)
    assert x == [[IB, Decimal("0")]]


# FIXME: fluctuating balances
@pytest.mark.parametrize("decimals", [True, False])
@pytest.mark.parametrize("reward", [True, False])
def test_get_locked(decimals, reward):
    x = IronBank.get_locked(TEST_WALLET, TEST_BLOCK, OPTIMISM, 302, WEB3, reward=reward, decimals=decimals)
    y = Decimal(10**18 if decimals else 1)
    assert (
        x
        == [
            [veIB, pytest.approx(Decimal("54181897005598451410657") / y, rel=Decimal(1e-2))],
            [IB, pytest.approx(Decimal("69825279969409816077552") / y, rel=Decimal(1e-2))],
            [IB, Decimal("26357551702575691254852") / y],
            [iUSDC, Decimal("17289739240114") / Decimal(10 ** (8 if decimals else 0))],
        ][: (4 if reward else 2)]
    )


@pytest.mark.parametrize("decimals", [True, False])
@pytest.mark.parametrize("reward", [True, False])
def test_underlying(decimals, reward):
    x = IronBank.underlying(TEST_WALLET, USDC, TEST_BLOCK, OPTIMISM, WEB3, decimals=decimals, reward=reward)
    y = Decimal(10**6 if decimals else 1)
    assert x == [[USDC, Decimal("3807347311.624904820141022815") / y, 0], [IB, Decimal("0")]][: (2 if reward else 1)]


@pytest.mark.parametrize("decimals", [True, False])
@pytest.mark.parametrize("reward", [True, False])
def test_underlying_all(decimals, reward):
    x = IronBank.underlying_all(TEST_WALLET, TEST_BLOCK, OPTIMISM, WEB3, decimals=decimals, reward=reward)
    y = Decimal(10**6 if decimals else 1)
    assert x == [[USDC, Decimal("3807347311.624904820141022815") / y, 0], [IB, Decimal("0")]][: (2 if reward else 1)]


@pytest.mark.parametrize("decimals", [True, False])
def test_unwrap(decimals):
    x = IronBank.unwrap(Decimal(198489), iUSDC, TEST_BLOCK, OPTIMISM, WEB3, decimals=decimals)
    y = Decimal(10**6 if decimals else 1)
    assert x == [USDC, Decimal("2016846463.2757690383") / y]
