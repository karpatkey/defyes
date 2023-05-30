import pytest
from decimal import Decimal

from defi_protocols import Honeyswap, add_stderr_logger
from defi_protocols.functions import get_node
from defi_protocols.constants import XDAI, WETH_XDAI, GNO_XDAI


TEST_BLOCK = 27450341
TEST_WALLET = '0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f'
WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)

UNIv2 = '0x28dbd35fd79f48bfa9444d330d14683e7101d817'


def test_get_lptoken_data():
    data = Honeyswap.get_lptoken_data(UNIv2, TEST_BLOCK, XDAI, WEB3)
    expected = {'decimals': 18,
                'totalSupply': 2780438593422870570963,
                'token0': WETH_XDAI,
                'token1': GNO_XDAI,
                'reserves': [697389190335766422886,
                             11931109898533386964234,
                             1681509230],
                'kLast': 8320457320306632575150389158633998324068504,
                'virtualTotalSupply': Decimal('2780443320502662251210.953287')}
    assert expected == {k: data[k] for k in expected}


@pytest.mark.parametrize('decimals', [True, False])
def test_underlying(decimals):
    x = Honeyswap.underlying(TEST_WALLET, UNIv2, TEST_BLOCK, XDAI,
                             WEB3, decimals=decimals)
    assert x == [[WETH_XDAI, Decimal('697386974825513061735.0076492') / (10**18 if decimals else 1)],
                 [GNO_XDAI, Decimal('11931071995026019072977.21406') / (10**18 if decimals else 1)]]


@pytest.mark.parametrize('decimals', [True, False])
def test_pool_balances(decimals):
    x = Honeyswap.pool_balances(UNIv2, TEST_BLOCK, XDAI, WEB3,
                                decimals=decimals)
    assert x == [[WETH_XDAI, Decimal('697389190335766422886') / (10**18 if decimals else 1)],
                 [GNO_XDAI, Decimal('11931109898533386964234') / (10**18 if decimals else 1)]]


@pytest.mark.parametrize('decimals', [True, False])
def test_swap_fees(decimals):
    x = Honeyswap.swap_fees(UNIv2, TEST_BLOCK - 1000, TEST_BLOCK, XDAI, WEB3,
                            decimals=decimals)
    assert x['swaps'] == [{'block': 27449397,
                           'token': GNO_XDAI,
                           'amount': Decimal('18914160864473195.745') / Decimal(10**18 if decimals else 1)},
                          {'block': 27450198,
                           'token': GNO_XDAI,
                           'amount': Decimal('2825275064344436.103') / (10**18 if decimals else 1)}]
