import datetime

import pytz
from pytest import raises

from defyes.constants import ETHEREUM, STETH_ETH, USDC_ETH, XDAI, ETHTokenAddr
from defyes.functions import date_to_block, get_node, get_symbol, search_proxy_impl_address


def test_get_node():
    node = get_node(ETHEREUM)
    assert node


def test_date_to_block():
    block = 16671547
    assert date_to_block("2023-02-20 18:30:00", ETHEREUM) == block
    date = datetime.datetime(year=2023, month=2, day=20, hour=18, minute=30, second=0)
    assert date_to_block(date, ETHEREUM) == block
    date = datetime.datetime(year=2023, month=2, day=20, hour=18, minute=30, second=0, tzinfo=pytz.UTC)
    assert date_to_block(date, ETHEREUM) == block


def test_get_node_of_unknown_network():
    raises(ValueError, get_node, "unknown_network")


def test_get_symbol():
    symbol = get_symbol(ETHTokenAddr.DAI, blockchain=ETHEREUM, block=17380523)
    assert symbol == "DAI"

    symbol = get_symbol("0x0000000000000000000000000000000000000000", blockchain=ETHEREUM, block=17380523)
    assert symbol == "ETH"

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=ETHEREUM, block=17380523)
    assert symbol == "ETH"

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=XDAI, block=17380523)
    assert symbol == "XDAI"


def test_search_proxy_impl_address():
    # OpenZeppelins' EIP-1967
    implementation = search_proxy_impl_address("0xE95A203B1a91a908F9B9CE46459d101078c2c3cb", ETHEREUM)
    assert implementation == "0x3eD1DFBCCF893b7d2D730EAd3e5eDBF1f8f95a48"

    implementation = search_proxy_impl_address("0xE95A203B1a91a908F9B9CE46459d101078c2c3cb", ETHEREUM, block=16477000)
    assert implementation == "0x89632e27427109d64fFe1CdD98027139477E020F"

    implementation = search_proxy_impl_address("0xE95A203B1a91a908F9B9CE46459d101078c2c3cb", ETHEREUM, block=16475978)
    assert implementation == "0x1E5e5CF3652989A57736901D95749A326F5Cb60F"

    # OpenZeppelins' EIP-1167
    implementation = search_proxy_impl_address("0x793fAF861a78B07c0C8c0ed1450D3919F3473226", XDAI)
    assert implementation == "0x45fFd460cC6642B8D8Fb12373DFd77Ceb0f4932B"

    # Custom proxy implementation (similar to EIP-1167)
    implementation = search_proxy_impl_address("0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14", ETHEREUM)
    assert implementation == "0x2157A7894439191e520825fe9399aB8655E0f708"

    # OpenZeppelins' Unstructured Storage proxy pattern
    implementation = search_proxy_impl_address(USDC_ETH, ETHEREUM)
    assert implementation == "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF"

    implementation = search_proxy_impl_address(USDC_ETH, ETHEREUM, block=10800000)
    assert implementation == "0xB7277a6e95992041568D9391D09d0122023778A2"

    # OpenZeppelins' EIP-897 DelegateProxy
    implementation = search_proxy_impl_address(STETH_ETH, ETHEREUM)
    assert implementation == "0x17144556fd3424EDC8Fc8A4C940B2D04936d17eb"

    implementation = search_proxy_impl_address("0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B", ETHEREUM)
    assert implementation == "0xBafE01ff935C7305907c33BF824352eE5979B526"

    # Custom proxy implementation (used by Safes)
    implementation = search_proxy_impl_address("0x4F2083f5fBede34C2714aFfb3105539775f7FE64", ETHEREUM)
    assert implementation == "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552"
