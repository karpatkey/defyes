from decimal import Decimal

from defyes import Connext
from defyes.constants import XDAI, GnosisTokenAddr
from defyes.functions import get_node

WALLET_969 = "0x10e4597ff93cbee194f4879f8f1d54a370db6969"
WALLET_e6f = "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f"

CUSDCLP = "0xA639FB3f8C52e10E10a8623616484d41765d5F82"
CWETHLP = "0x7aC5bBefAE0459F007891f9Bd245F6beaa91076c"


def test_underlying():
    block = 27795362
    node = get_node(XDAI, block)

    next_usdc, usdc = Connext.underlying(WALLET_969, CUSDCLP, block, XDAI, web3=node)
    assert next_usdc == [GnosisTokenAddr.nextUSDC, Decimal("1064967.162791")]
    assert usdc == [GnosisTokenAddr.USDC, Decimal("1439222.771596")]

    next_weth, weth = Connext.underlying(WALLET_e6f, CWETHLP, block, XDAI, web3=node)
    assert next_weth == [GnosisTokenAddr.nextWETH, Decimal("234.524117434062197999")]
    assert weth == [GnosisTokenAddr.WETH, Decimal("301.665989542168124866")]


def test_underlying_all():
    block = 27795362
    node = get_node(XDAI, block)

    [next_dai, wxdai], [next_usdc, usdc], [next_usdt, usdt] = Connext.underlying_all(WALLET_969, block, XDAI, web3=node)
    assert next_dai == [GnosisTokenAddr.nextDAI, Decimal("599315.782399033321427464")]
    assert wxdai == [GnosisTokenAddr.WXDAI, Decimal("601284.983369595820396222")]
    assert next_usdc == [GnosisTokenAddr.nextUSDC, Decimal("1064967.162791")]
    assert usdc == [GnosisTokenAddr.USDC, Decimal("1439222.771596")]
    assert next_usdt == [GnosisTokenAddr.nextUSDT, Decimal("679990.427185")]
    assert usdt == [GnosisTokenAddr.USDT, Decimal("680007.569573")]


def test_unwrap():
    block = 27795362
    node = get_node(XDAI, block)

    usdc = Connext.unwrap(2496314.966980158115136554, CUSDCLP, block, XDAI, web3=node)
    assert usdc == [GnosisTokenAddr.USDC, Decimal("2504189.934387")]
