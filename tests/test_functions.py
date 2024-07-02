import datetime

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from hexbytes import HexBytes
from web3.types import LogReceipt

from defyes.functions import (
    block_to_date,
    date_to_block,
    get_abi_function_signatures,
    get_logs_web3,
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
    symbol = get_symbol(EthereumTokenAddr.DAI, blockchain=Chain.ETHEREUM)
    assert symbol == "DAI"

    symbol = get_symbol("0x0000000000000000000000000000000000000000", blockchain=Chain.ETHEREUM)
    assert symbol == "ETH"

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=Chain.ETHEREUM)
    assert symbol == "ETH"

    symbol = get_symbol("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE", blockchain=Chain.GNOSIS)
    assert symbol == "GNOSIS"

    symbol = get_symbol("0x89d24A6b4CcB1B6fAA2625fE562bDD9a23260359", "ethereum")
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


def test_get_logs_web3():
    logs = get_logs_web3(
        blockchain=Chain.ETHEREUM,
        topics=["0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"],
        block_start=18934050,
        block_end=18934090,
    )
    assert logs == [
        LogReceipt(
            {
                "address": "0x89D3D732da8bf0f88659Cf3738E5E44e553f9ED7",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000000760a1e7fad40af8556"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 180,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x9E1104962D1019913269d8Db409c12456F362Df6",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000004cd9efc472cbadc0f2b"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 182,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0xDd1fE5AD401D4777cE89959b7fa587e569Bf125D",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x00000000000000000000000000000000000000000000004170b6c0de2336f900"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 185,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0xf66a72886749c96b18526E8E124cC2e18b7c72D2",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x00000000000000000000000000000000000000000000009d24cca03587c0ddf4"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 187,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0xAc16927429c5c7Af63dD75BC9d8a58c63FfD0147",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000004c06c8e072010b99a09"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 189,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x6f4bb9E23CA970681F3CABD0D52Fc36f8dfD8F91",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000a61de053e64a19c3f8d372a6a868f8c31a90e45e"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000000000000019011041e36"),
                "blockNumber": 18934053,
                "transactionHash": HexBytes("0x6dea357095f0caa3d17c87c874b545704196ca8865e871f947570bda94f2ef8c"),
                "transactionIndex": 107,
                "blockHash": HexBytes("0xb7b423cb9dc15ff646680fb5a839e9144f786d8218a24c9d13317262587672f0"),
                "logIndex": 202,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x19F3C877eA278e61fE1304770dbE5D78521792D2",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000346f1d297c98c28574742b067b67a80cda2dc0d9"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000001606d4eb1eb30ed12ee"),
                "blockNumber": 18934074,
                "transactionHash": HexBytes("0xbafd32001dc6fe53444a8c694c663f50cf6af3246506e1eef9ec4e6086126f82"),
                "transactionIndex": 86,
                "blockHash": HexBytes("0x82d495cf561d834614627b108ec052bfbe16f8a8744c72c135ed471e8ee3b2b3"),
                "logIndex": 187,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x3Fe65692bfCD0e6CF84cB1E7d24108E434A7587e",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000aa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434"),
                ],
                "data": HexBytes("0x000000000000000000000000000000000000000000000053a4e3ccac6b079708"),
                "blockNumber": 18934074,
                "transactionHash": HexBytes("0x2ad00c5426cb7724a8a4ce86290cee1a066b74642ca48113ec690c72b16d8367"),
                "transactionIndex": 122,
                "blockHash": HexBytes("0x82d495cf561d834614627b108ec052bfbe16f8a8744c72c135ed471e8ee3b2b3"),
                "logIndex": 252,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x7091dbb7fcbA54569eF1387Ac89Eb2a5C9F6d2EA",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000aa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434"),
                ],
                "data": HexBytes("0x00000000000000000000000000000000000000000000004927aec1fd73a4c2c4"),
                "blockNumber": 18934074,
                "transactionHash": HexBytes("0x2ad00c5426cb7724a8a4ce86290cee1a066b74642ca48113ec690c72b16d8367"),
                "transactionIndex": 122,
                "blockHash": HexBytes("0x82d495cf561d834614627b108ec052bfbe16f8a8744c72c135ed471e8ee3b2b3"),
                "logIndex": 254,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x449f2fd99174e1785CF2A1c79E665Fec3dD1DdC6",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000aa0c3f5f7dfd688c6e646f66cd2a6b66acdbe434"),
                ],
                "data": HexBytes("0x000000000000000000000000000000000000000000000009cf68d0927740abe8"),
                "blockNumber": 18934074,
                "transactionHash": HexBytes("0x2ad00c5426cb7724a8a4ce86290cee1a066b74642ca48113ec690c72b16d8367"),
                "transactionIndex": 122,
                "blockHash": HexBytes("0x82d495cf561d834614627b108ec052bfbe16f8a8744c72c135ed471e8ee3b2b3"),
                "logIndex": 256,
                "removed": False,
            }
        ),
    ]

    logs_2 = get_logs_web3(
        blockchain=Chain.ETHEREUM,
        tx_hash="0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c",
        topics=["0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"],
    )

    assert logs_2 == [
        LogReceipt(
            {
                "address": "0x89D3D732da8bf0f88659Cf3738E5E44e553f9ED7",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000000760a1e7fad40af8556"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 180,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0x9E1104962D1019913269d8Db409c12456F362Df6",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000004cd9efc472cbadc0f2b"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 182,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0xDd1fE5AD401D4777cE89959b7fa587e569Bf125D",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x00000000000000000000000000000000000000000000004170b6c0de2336f900"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 185,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0xf66a72886749c96b18526E8E124cC2e18b7c72D2",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x00000000000000000000000000000000000000000000009d24cca03587c0ddf4"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 187,
                "removed": False,
            }
        ),
        LogReceipt(
            {
                "address": "0xAc16927429c5c7Af63dD75BC9d8a58c63FfD0147",
                "topics": [
                    HexBytes("0xe2403640ba68fed3a2f88b7557551d1993f84b99bb10ff833f0cf8db0c5e0486"),
                    HexBytes("0x000000000000000000000000849d52316331967b6ff1198e5e32a0eb168d039d"),
                ],
                "data": HexBytes("0x0000000000000000000000000000000000000000000004c06c8e072010b99a09"),
                "blockNumber": 18934050,
                "transactionHash": HexBytes("0x1b99e432cfd9ba2411a49aa9e5544e7c02829c55c75d2dd9739d67917ef7188c"),
                "transactionIndex": 82,
                "blockHash": HexBytes("0x838560dea6b9c14f855d39411930ad377aaf0e1d6f96db1439c3c6523de3dfd7"),
                "logIndex": 189,
                "removed": False,
            }
        ),
    ]
