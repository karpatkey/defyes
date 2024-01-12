from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.node import get_node

from defyes import Compoundv3

WALLET_N1 = "0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669"
TOKEN_ADDRESS = "0xc3d688B66703497DAA19211EEdff47f25384cdc3"


def test_underlying():
    block = 17151264
    node = get_node(Chain.ETHEREUM)

    underlying = Compoundv3.underlying(WALLET_N1, TOKEN_ADDRESS, block, Chain.ETHEREUM, web3=node)
    assert underlying == [[EthereumTokenAddr.USDC, Decimal("2208438.458228")]]


def test_get_all_rewards():
    block = 17836566
    node = get_node(Chain.ETHEREUM)

    all_rewards = Compoundv3.get_all_rewards(WALLET_N1, TOKEN_ADDRESS, block, Chain.ETHEREUM, web3=node)
    assert all_rewards == [[EthereumTokenAddr.COMP, Decimal("9.743306")]]
