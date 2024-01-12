from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.constants import Address
from karpatkit.node import get_node

from defyes import Bancor

WALLET_N1 = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
WALLET_N2 = "0xc0167f4B1bb78912DF9920Bd146151942620Da15"

bnICHI_ADDR = "0x36FAbE4cAeF8c190550b6f93c306A5644E7dCef6"
bnETH_ADDR = "0x256Ed1d83E3e4EfDda977389A5389C3433137DDA"


def test_underlying():
    block = 17067718
    node = get_node(Chain.ETHEREUM)

    underlying = Bancor.underlying(bnICHI_ADDR, WALLET_N1, block, Chain.ETHEREUM, web3=node)
    assert underlying == [[EthereumTokenAddr.ICHI, Decimal("44351.005182315")], [EthereumTokenAddr.BNT, Decimal("0")]]
    underlying = Bancor.underlying(bnETH_ADDR, WALLET_N2, block, Chain.ETHEREUM, web3=node)
    assert underlying == [[Address.E, Decimal("0.149703304228299349")], [EthereumTokenAddr.BNT, Decimal("0")]]


@pytest.mark.skip(reason="It takes to long.")
def test_underlying_all():
    block = 17067718
    node = get_node(Chain.ETHEREUM)

    underlying = Bancor.underlying_all(WALLET_N2, block, Chain.ETHEREUM, web3=node)
    assert underlying == [
        [[Address.E, Decimal("0.149703304228299349")], [EthereumTokenAddr.BNT, Decimal("0")]],
        *(list() for _ in range(147)),  # plus 147 empty lists
    ]
