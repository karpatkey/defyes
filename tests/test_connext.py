import pytest

from defi_protocols import Connext
from defi_protocols.functions import get_node
from defi_protocols.constants import XDAI, GnosisTokenAddr

WALLET_969 = "0x10e4597ff93cbee194f4879f8f1d54a370db6969"
WALLET_e6f = "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f"

CUSDCLP = "0xA639FB3f8C52e10E10a8623616484d41765d5F82"
CWETHLP = "0x7aC5bBefAE0459F007891f9Bd245F6beaa91076c"

def test_underlying():
    block = 27795362
    node = get_node(XDAI, block)

    next_usdc, usdc = Connext.underlying(WALLET_969, CUSDCLP, block, XDAI, web3=node)
    assert next_usdc == [GnosisTokenAddr.nextUSDC, 1064967.162791]
    assert usdc == [GnosisTokenAddr.USDC, 1439222.771596]

    next_weth, weth = Connext.underlying(WALLET_e6f, CWETHLP, block, XDAI, web3=node)
    assert next_weth == [GnosisTokenAddr.nextWETH, 234.5241174340622]
    assert weth == [GnosisTokenAddr.WETH, 301.6659895421681]

def test_underlying_all():
    block = 27795362
    node = get_node(XDAI, block)

    [next_dai, wxdai], [next_usdc, usdc], [next_usdt, usdt] = Connext.underlying_all(WALLET_969, block, XDAI, web3=node)
    assert next_dai == [GnosisTokenAddr.nextDAI, 599315.7823990333]
    assert wxdai == [GnosisTokenAddr.WXDAI, 601284.9833695958]
    assert next_usdc == [GnosisTokenAddr.nextUSDC, 1064967.162791]
    assert usdc == [GnosisTokenAddr.USDC, 1439222.771596]
    assert next_usdt == [GnosisTokenAddr.nextUSDT, 679990.427185]
    assert usdt == [GnosisTokenAddr.USDT, 680007.569573]

def test_unwrap():
    block = 27795362
    node = get_node(XDAI, block)

    usdc = Connext.unwrap(2496314.966980158115136554, CUSDCLP, block, XDAI, web3=node)
    assert usdc == [GnosisTokenAddr.USDC, 2504189.9343870003]