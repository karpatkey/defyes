from decimal import Decimal

import pytest

from defyes import Stakewise
from defyes.constants import ETHEREUM, XDAI
from defyes.functions import get_node

WALLET_N1 = "0x05E61adDCef87ad8548236eb5Cbf2f699C834935"
WALLET_N2 = "0x53811010085382D49eF12bCC55902bbFCEB57790"


@pytest.mark.parametrize("reward", [True, False])
def test_check_uniswap_v3_pools(reward):
    block = 17438389
    blockchain = ETHEREUM
    node = get_node(blockchain, block)
    pools = Stakewise.check_uniswap_v3_pools(WALLET_N1, block, blockchain, web3=node, reward=reward)
    assert (
        pools
        == {
            "WETH-sETH2": {
                "NFT ID": 519045,
                "balances": [
                    {
                        "token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                        "balance": Decimal("0.199985076842016013023196507"),
                    },
                    {
                        "token": "0xFe2e637202056d30016725477c5da089Ab0A043A",
                        "balance": Decimal("0.1724483369988353747402367949"),
                    },
                ],
                "fees": [
                    {
                        "token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                        "balance": Decimal("2.538555372051508404845944501E-9"),
                    },
                    {
                        "token": "0xFe2e637202056d30016725477c5da089Ab0A043A",
                        "balance": Decimal("4.764036522980764132925874182E-8"),
                    },
                ],
            }
        }
        if reward
        else {
            "WETH-sETH2": {
                "NFT ID": 519045,
                "balances": [
                    {
                        "token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                        "balance": Decimal("0.199985076842016013023196507"),
                    },
                    {
                        "token": "0xFe2e637202056d30016725477c5da089Ab0A043A",
                        "balance": Decimal("0.1724483369988353747402367949"),
                    },
                ],
            }
        }
    )


@pytest.mark.parametrize("reward", [True, False])
def test_check_curve_pools(reward):
    block = 28357764
    blockchain = XDAI
    node = get_node(blockchain, block)
    pools = Stakewise.check_curve_pools(WALLET_N2, block, blockchain, web3=node, reward=reward)
    assert (
        pools
        == {
            "sGNO-GNO": {
                "LP token": "0xBdF4488Dcf7165788D438b62B4C8A333879B7078",
                "balances": [
                    {
                        "token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("78.79376345379012490489136847"),
                    },
                    {
                        "token": "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("72.45915574443603897500649474"),
                    },
                ],
                "rewards": [{"token": "0x712b3d230F3C1c19db860d80619288b1F0BDd0Bd", "balance": Decimal("0")}],
            },
            "rGNO-sGNO": {
                "LP token": "0x5d7309a01b727d6769153fcb1df5587858d53b9c",
                "balances": [
                    {
                        "token": "0x6aC78efae880282396a335CA2F79863A1e6831D4",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("0E-18"),
                    },
                    {
                        "token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("0E-18"),
                    },
                ],
                "rewards": [{"token": "0x712b3d230F3C1c19db860d80619288b1F0BDd0Bd", "balance": Decimal("0")}],
            },
        }
        if reward
        else {
            "sGNO-GNO": {
                "LP token": "0xBdF4488Dcf7165788D438b62B4C8A333879B7078",
                "balances": [
                    {
                        "token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("78.79376345379012490489136847"),
                    },
                    {
                        "token": "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("72.45915574443603897500649474"),
                    },
                ],
            },
            "rGNO-sGNO": {
                "LP token": "0x5d7309a01b727d6769153fcb1df5587858d53b9c",
                "balances": [
                    {
                        "token": "0x6aC78efae880282396a335CA2F79863A1e6831D4",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("0E-18"),
                    },
                    {
                        "token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445",
                        "unstaked": Decimal("0E-18"),
                        "staked": Decimal("0E-18"),
                    },
                ],
            },
        }
    )


@pytest.mark.parametrize("pools", [True, False])
def test_underlying(pools):
    block = 17438389
    blockchain = ETHEREUM
    node = get_node(blockchain, block)
    underlying = Stakewise.underlying(WALLET_N1, block, blockchain, web3=node, pools=pools, decimals=False)
    assert (
        underlying
        == {
            "protocol": "Stakewise",
            "blockchain": "ethereum",
            "block": 17438389,
            "balances": [
                {"token": "0xFe2e637202056d30016725477c5da089Ab0A043A", "balance": Decimal("0.849414886512576674")},
                {"token": "0x20BC832ca081b91433ff6c17f85701B6e92486c5", "balance": Decimal("0.000462283209172035")},
            ],
            "Uniswap V3 pools": {
                "WETH-sETH2": {
                    "NFT ID": 519045,
                    "balances": [
                        {
                            "token": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                            "balance": Decimal("199985076842016013.0231965070"),
                        },
                        {
                            "token": "0xFe2e637202056d30016725477c5da089Ab0A043A",
                            "balance": Decimal("172448336998835374.7402367949"),
                        },
                    ],
                }
            },
        }
        if pools
        else {
            "protocol": "Stakewise",
            "blockchain": "ethereum",
            "block": 17438389,
            "balances": [
                {"token": "0xFe2e637202056d30016725477c5da089Ab0A043A", "balance": Decimal("0.849414886512576674")},
                {"token": "0x20BC832ca081b91433ff6c17f85701B6e92486c5", "balance": Decimal("0.000462283209172035")},
            ],
        }
    )

    block = 28357764
    blockchain = XDAI
    node = get_node(blockchain, block)
    underlying = Stakewise.underlying(WALLET_N2, block, blockchain, web3=node, pools=pools, decimals=False)
    assert (
        underlying
        == {
            "protocol": "Stakewise",
            "blockchain": "xdai",
            "block": 28357764,
            "balances": [
                {"token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445", "balance": Decimal("0")},
                {"token": "0x6aC78efae880282396a335CA2F79863A1e6831D4", "balance": Decimal("130.658666761645960747")},
            ],
            "Curve pools": {
                "sGNO-GNO": {
                    "LP token": "0xBdF4488Dcf7165788D438b62B4C8A333879B7078",
                    "balances": [
                        {
                            "token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445",
                            "unstaked": Decimal("0"),
                            "staked": Decimal("78793763453790124904.89136847"),
                        },
                        {
                            "token": "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb",
                            "unstaked": Decimal("0"),
                            "staked": Decimal("72459155744436038975.00649474"),
                        },
                    ],
                },
                "rGNO-sGNO": {
                    "LP token": "0x5d7309a01b727d6769153fcb1df5587858d53b9c",
                    "balances": [
                        {
                            "token": "0x6aC78efae880282396a335CA2F79863A1e6831D4",
                            "unstaked": Decimal("0"),
                            "staked": Decimal("0"),
                        },
                        {
                            "token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445",
                            "unstaked": Decimal("0"),
                            "staked": Decimal("0"),
                        },
                    ],
                },
            },
        }
        if pools
        else {
            "protocol": "Stakewise",
            "blockchain": "xdai",
            "block": 28357764,
            "balances": [
                {"token": "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445", "balance": Decimal("0")},
                {"token": "0x6aC78efae880282396a335CA2F79863A1e6831D4", "balance": Decimal("130.658666761645960747")},
            ],
        }
    )


# TODO: Adding tests for Stakewise.get_all_rewards which can currently only query the last block
