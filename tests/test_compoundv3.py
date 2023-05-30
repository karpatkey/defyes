from decimal import Decimal

from defi_protocols import Compoundv3
from defi_protocols.constants import ETHEREUM, ETHTokenAddr
from defi_protocols.functions import get_node

WALLET_N1 = '0x616dE58c011F8736fa20c7Ae5352F7f6FB9F0669'
TOKEN_ADDRESS = '0xc3d688B66703497DAA19211EEdff47f25384cdc3'


def test_underlying():
    block = 17151264
    node = get_node(ETHEREUM, block)

    underlying = Compoundv3.underlying(WALLET_N1, TOKEN_ADDRESS, block, ETHEREUM, web3=node)
    assert underlying == [[ETHTokenAddr.USDC, Decimal('2208438.458228')]]


def test_get_all_rewards():
    block = 17151264
    node = get_node(ETHEREUM, block)

    all_rewards = Compoundv3.get_all_rewards(WALLET_N1, TOKEN_ADDRESS, block, ETHEREUM, web3=node)
    assert all_rewards == [[ETHTokenAddr.COMP, Decimal('0')]]
