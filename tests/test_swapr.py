import pytest
from decimal import Decimal

from defi_protocols import Swapr
from defi_protocols.functions import get_node, get_contract
from defi_protocols.constants import XDAI, ETHEREUM, GNO_XDAI, WETH_XDAI

TEST_BLOCK = 27450341
TEST_WALLET = '0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f'
WEB3 = get_node(blockchain=XDAI, block=TEST_BLOCK)

# DXS is the lptoken for BER+GNO pair
DXS = '0x1Ad6A0cFF3870b252492597B557F3e61F130663D'
BER_XDAI = '0x05698e7346Ea67Cfb088f64Ad8962B18137d17c0'


# There is no point in testing:
# get_staking_rewards_contract
# It's just a switch


#FIXME: this function can't be tested for db=False because it takes forever
@pytest.mark.parametrize('campaigns', [0, 1, 'all'])
@pytest.mark.parametrize('db', [True])
def test_get_distribution_contracts(campaigns, db):
    staking_rewards_contract = get_contract(Swapr.SRC_XDAI, XDAI, web3=WEB3, abi=Swapr.ABI_SRC, block=TEST_BLOCK)
    x = Swapr.get_distribution_contracts(WEB3, GNO_XDAI, staking_rewards_contract, campaigns, TEST_BLOCK, XDAI, db=db)
    assert x == []


def test_get_lptoken_data():
    x = Swapr.get_lptoken_data(DXS, TEST_BLOCK, XDAI, WEB3)
    expected = {'decimals': 18,
                'totalSupply': 94233751915117971705,
                'token0': BER_XDAI,
                'token1': GNO_XDAI,
                'reserves': [1071822921647535396369, 8286413444006866465, 1677145545],
                'kLast': 8880000000000000000000000000000000000000,
                'virtualTotalSupply': Decimal('94235138257570979954.58402272')}
    assert {k: x[k] for k in expected} == expected


# FIXME: this function can't be tested for db=False because it takes forever
@pytest.mark.parametrize('campaigns', [0, 1, 'all'])
@pytest.mark.parametrize('db', [True])
def test_get_all_rewards(campaigns, db):
    x = Swapr.get_all_rewards(TEST_WALLET, DXS, TEST_BLOCK, XDAI, WEB3,
                              decimals=True, campaigns=campaigns, distribution_contracts=None, db=db)
    # FIXME: find a better wallet
    assert x == []


# FIXME: this function can't be tested for db=False because it takes forever
@pytest.mark.parametrize('campaigns', [0, 1, 'all'])
@pytest.mark.parametrize('db', [True])
@pytest.mark.parametrize('decimals', [True, False])
@pytest.mark.parametrize('reward', [True, False])
def test_underlying(campaigns, db, decimals, reward):
    x = Swapr.underlying(TEST_WALLET, DXS, TEST_BLOCK, XDAI, WEB3,
                         decimals=decimals, reward=reward, campaigns=campaigns, db=db)
    y = Decimal(10**18 if decimals else 1)
    assert x == [[BER_XDAI, Decimal('1071807153499412909748.616424') / y, Decimal('0')],
                 [GNO_XDAI, Decimal('8286291538240577738.223834754') / y, Decimal('0')]]


@pytest.mark.parametrize('decimals', [True, False])
def test_pool_balances(decimals):
    x = Swapr.pool_balances(DXS, TEST_BLOCK, XDAI, WEB3, decimals=decimals)
    y = Decimal(10**18 if decimals else 1)
    assert x == [[BER_XDAI, Decimal('1071822921647535396369') / y],
                 [GNO_XDAI, Decimal('8286413444006866465') / y]]


@pytest.mark.parametrize('decimals', [False, True])
def test_swap_fees(decimals):
    x = Swapr.swap_fees(DXS, TEST_BLOCK - 100, 27568826, XDAI, WEB3, decimals=decimals)
    y = Decimal(10**18 if decimals else 1)
    assert x['swaps'] == [{'block': 27494581, 'token': BER_XDAI, 'amount': Decimal('249999999999999999.8900') / y},
                          {'block': 27494618, 'token': BER_XDAI, 'amount': Decimal('1562499999999999999.3975') / y},
                          {'block': 27494972, 'token': GNO_XDAI, 'amount': Decimal('2537125747349638.0950') / y},
                          {'block': 27507943, 'token': GNO_XDAI, 'amount': Decimal('10825598350382.8550') / y},
                          {'block': 27508016, 'token': BER_XDAI, 'amount': Decimal('2497385336193485.3650') / y},
                          {'block': 27508197, 'token': GNO_XDAI, 'amount': Decimal('10752897685489.7700') / y},
                          {'block': 27510159, 'token': BER_XDAI, 'amount': Decimal('104140624994283793.4525') / y}]


@pytest.mark.skip('This takes forever')
def test_update_db():
    Swapr.update_db()
    assert True
