import datetime

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr

from defyes.functions import (
    block_to_date,
    date_to_block,
    get_abi_function_signatures,
    get_symbol,
    search_proxy_impl_address,
)


def test_date_to_block():
    block = 16671547
    assert date_to_block("2023-02-20 18:30:00", Chain.ETHEREUM) == block
    date = datetime.datetime(year=2023, month=2, day=20, hour=18, minute=30, second=0, tzinfo=datetime.timezone.utc)
    assert date_to_block(date, Chain.ETHEREUM) == block

    with pytest.raises(ValueError):
        date = datetime.datetime(year=2023, month=2, day=20, hour=18, minute=30, second=0)
        assert date_to_block(date, Chain.ETHEREUM) == block


def test_block_to_date():
    block = 16671547
    assert block_to_date(block, Chain.ETHEREUM) == "2023-02-20 18:29:59"


def test_get_symbol():
    symbol = get_symbol(EthereumTokenAddr.DAI, blockchain=Chain.ETHEREUM, block=17380523)
    assert symbol == "DAI"

    symbol = get_symbol("0x0000000000000000000000000000000000000000", blockchain=Chain.ETHEREUM, block=17380523)
    assert symbol == "ETH"

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=Chain.ETHEREUM, block=17380523)
    assert symbol == "ETH"

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=Chain.GNOSIS, block=17380523)
    assert symbol == "GNOSIS"

    symbol = get_symbol("0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359", Chain.ETHEREUM)
    assert symbol == "DAI"


def test_search_proxy_impl_address():
    # OpenZeppelins' EIP-1967
    implementation = search_proxy_impl_address(
        "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb", Chain.ETHEREUM, block=16477000
    )
    assert implementation == "0x89632e27427109d64fFe1CdD98027139477E020F"

    implementation = search_proxy_impl_address(
        "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb", Chain.ETHEREUM, block=16475978
    )
    assert implementation == "0x1E5e5CF3652989A57736901D95749A326F5Cb60F"

    # OpenZeppelins' EIP-1167
    implementation = search_proxy_impl_address(
        "0x793fAF861a78B07c0C8c0ed1450D3919F3473226", Chain.GNOSIS, block=31782206
    )
    assert implementation == "0x45fFd460cC6642B8D8Fb12373DFd77Ceb0f4932B"

    # Custom proxy implementation (similar to EIP-1167)
    implementation = search_proxy_impl_address(
        "0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14", Chain.ETHEREUM, block=16475978
    )
    assert implementation == "0x2157A7894439191e520825fe9399aB8655E0f708"

    # OpenZeppelins' Unstructured Storage proxy pattern
    implementation = search_proxy_impl_address(EthereumTokenAddr.USDC, Chain.ETHEREUM, block=16475978)
    assert implementation == "0xa2327a938Febf5FEC13baCFb16Ae10EcBc4cbDCF"

    implementation = search_proxy_impl_address(EthereumTokenAddr.USDC, Chain.ETHEREUM, block=10800000)
    assert implementation == "0xB7277a6e95992041568D9391D09d0122023778A2"

    # OpenZeppelins' EIP-897 DelegateProxy
    implementation = search_proxy_impl_address(EthereumTokenAddr.stETH, Chain.ETHEREUM, block=18934617)
    assert implementation == "0x17144556fd3424EDC8Fc8A4C940B2D04936d17eb"

    implementation = search_proxy_impl_address(
        "0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B", Chain.ETHEREUM, block=18934617
    )
    assert implementation == "0xBafE01ff935C7305907c33BF824352eE5979B526"

    # Custom proxy implementation (used by Safes)
    implementation = search_proxy_impl_address(
        "0x4F2083f5fBede34C2714aFfb3105539775f7FE64", Chain.ETHEREUM, block=18934617
    )
    assert implementation == "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552"


def test_get_abi_function_signatures():
    signatures = get_abi_function_signatures("0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016", Chain.GNOSIS, block=16477000)
    assert signatures == [
        {
            "name": "claimValues",
            "signature": "claimValues(address,address)",
            "inline_signature": "claimValues(address,address)",
            "components": ["address", "address"],
            "components_names": ["_token", "_to"],
            "stateMutability": "nonpayable",
        },
        {
            "name": "owner",
            "signature": "owner()",
            "inline_signature": "owner()",
            "components": [],
            "components_names": [],
            "stateMutability": "view",
        },
        {
            "name": "transferOwnership",
            "signature": "transferOwnership(address)",
            "inline_signature": "transferOwnership(address)",
            "components": ["address"],
            "components_names": ["newOwner"],
            "stateMutability": "nonpayable",
        },
    ]

    signatures = get_abi_function_signatures(
        "0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016", Chain.GNOSIS, block=16477000, func_names=["foo"]
    )
    assert signatures == []

    signatures = get_abi_function_signatures(
        "0x4aa42145Aa6Ebf72e164C9bBC74fbD3788045016", Chain.GNOSIS, block=16477000, func_names=["claimValues"]
    )
    assert signatures == [
        {
            "name": "claimValues",
            "signature": "claimValues(address,address)",
            "inline_signature": "claimValues(address,address)",
            "components": ["address", "address"],
            "components_names": ["_token", "_to"],
            "stateMutability": "nonpayable",
        }
    ]
