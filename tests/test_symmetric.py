import pytest
from decimal import Decimal
from tempfile import NamedTemporaryFile

from defi_protocols import Symmetric
from defi_protocols.functions import get_node
from defi_protocols.constants import XDAI, GnosisTokenAddr

WALLET = '0xa3E1282ac6116A698A49b2084c5c30fE1947b4A5'
LPTOKEN_ADDR = '0x650f5d96E83d3437bf5382558cB31F0ac5536684'


def test_get_vault_contract():
    block = 24502952
    node = get_node(XDAI, block)
    vault = Symmetric.get_vault_contract(node, block, XDAI)
    assert vault.address == '0x24F87b37F4F249Da61D89c3FF776a55c321B2773'


def test_get_chef_contract():
    block = 24502952
    node = get_node(XDAI, block)
    chef = Symmetric.get_chef_contract(node, block, XDAI)
    assert chef.address == '0xdf667DeA9F6857634AaAf549cA40E06f04845C03'


def test_get_pool_info():
    block = 24502952
    node = get_node(XDAI, block)
    pool = Symmetric.get_pool_info(node, LPTOKEN_ADDR, block, XDAI)
    assert pool['pool_info'] == {'poolId': 1, 'allocPoint': 15}
    assert pool['totalAllocPoint'] == 100


def test_get_lptoken_data():
    block = 24502952
    node = get_node(XDAI, block)
    data = Symmetric.get_lptoken_data(LPTOKEN_ADDR, block, XDAI, node)
    assert data['poolId'] == b'e\x0f]\x96\xe8=47\xbfS\x82U\x8c\xb3\x1f\n\xc5Sf\x84\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01'
    assert data['decimals'] == 18
    assert data['totalSupply'] == 968478930818485838115


def test_get_rewarder_contract():
    block = 26502427
    node = get_node(XDAI, block)
    chef = Symmetric.get_chef_contract(node, block, XDAI)
    pool = Symmetric.get_pool_info(node, LPTOKEN_ADDR, block, XDAI)
    rewarder = Symmetric.get_rewarder_contract(node, block, XDAI, chef, pool['pool_info']['poolId'])
    assert rewarder.address == '0x300b2CE5Dda4E3B30c1906ac45639E328dCe2E15'


def test_get_symm_rewards():
    block = 26502427
    node = get_node(XDAI, block)
    chef = Symmetric.get_chef_contract(node, block, XDAI)
    pool = Symmetric.get_pool_info(node, LPTOKEN_ADDR, block, XDAI)
    symm = Symmetric.get_symm_rewards(node, WALLET, chef, pool['pool_info']['poolId'], block, XDAI)
    assert symm == [GnosisTokenAddr.SYMM, Decimal('97.408879919684859779')]


def test_get_rewards():
    block = 26502427
    node = get_node(XDAI, block)
    chef = Symmetric.get_chef_contract(node, block, XDAI)
    pool = Symmetric.get_pool_info(node, LPTOKEN_ADDR, block, XDAI)
    rewards = Symmetric.get_rewards(node, WALLET, chef, pool['pool_info']['poolId'], block, XDAI)
    assert rewards == [[GnosisTokenAddr.GNO, Decimal('0')]]


def test_get_all_rewards():
    block = 26502427
    node = get_node(XDAI, block)
    rewards = Symmetric.get_all_rewards(WALLET, LPTOKEN_ADDR, block, XDAI, node)
    assert rewards == [[GnosisTokenAddr.SYMM, Decimal('97.408879919684859779')], [GnosisTokenAddr.GNO, Decimal('0')]]


def test_underlying():
    block = 25502427
    node = get_node(XDAI, block)
    underlying = Symmetric.underlying(WALLET, LPTOKEN_ADDR, block, XDAI, node, reward=True)
    assert underlying == [
        [[GnosisTokenAddr.GNO, Decimal('0'), Decimal('18.07623048385338968061676268')],
         [GnosisTokenAddr.WXDAI, Decimal('0'), Decimal('383.1488150228401270848778395')]],
        [[GnosisTokenAddr.SYMM, Decimal('17.618790701012049339')],
         [GnosisTokenAddr.GNO, Decimal('0')]]]


def test_pool_balances():
    block = 25502427
    node = get_node(XDAI, block)
    balances = Symmetric.pool_balances(LPTOKEN_ADDR, block, XDAI, node)
    assert balances == [[GnosisTokenAddr.GNO, Decimal('49.02805906564116928')],
                       [GnosisTokenAddr.WXDAI, Decimal('1039.212392796716432123')]]


def test_get_rewards_per_unit():
    block = 25502427
    node = get_node(XDAI, block)
    rewards = Symmetric.get_rewards_per_unit(LPTOKEN_ADDR, XDAI, node, block)
    assert rewards == [{'symm_address': GnosisTokenAddr.SYMM, 'symmPerSecond': Decimal('63269355361192.04081632653061')},
                       {'reward_address': GnosisTokenAddr.GNO, 'rewardPerSecond': Decimal('0')}]


@pytest.mark.xfail(reason="Checking if db needs update")
def test_db_uptodate():
    with NamedTemporaryFile() as tmpfile:
        uptodate = Symmetric.update_db(tmpfile.name)
        assert uptodate is False, "DB is outdated"


@pytest.mark.skip(reason="Bug in: lptoken_contract.functions.getCurrentTokens")
def test_swap_fees():
    block_start = 24323921
    block_end = 24502952
    fees = Symmetric.swap_fees(LPTOKEN_ADDR, block_start, block_end, XDAI)
    print(fees)
