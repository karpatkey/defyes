from decimal import Decimal

from defi_protocols import Element
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, E_ADDRESS


LPTOKEN_ADDR = '0x06325440D014e39736583c165C2963BA99fAf14E'
WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

# calculate spot price:
# t = (expiration - unitseconds time now) / seconds in one year
# with getPoolTokens get supply of stETH and supply of Pt
# calculate stETH(Pt+TotalSupply) * t

# calculate fixed APY
# ((1 - spotprice)/spotprice/timeremaining)*100


def test_addresses():
    block = 17000000
    addresses = Element.get_addresses(block, ETHEREUM)
    assert len(addresses) == 37
    assert [item[-1] for item in addresses] == [1663355860, 1663341022, 1663361092, 1663348630, 1663354791, 1663336829,
                                                1677243924, 1677243756, 1677243924, 1683206136, 1624831814, 1625028466,
                                                1632834462, 1640620258, 1628997564, 1634325622, 1702000550, 1634346845,
                                                1635528110, 1636746083, 1637941844, 1643382476, 1643382514, 1643382446,
                                                1643382460, 1644601070, 1644601070, 1644604852, 1650025565, 1639727861,
                                                1651240496, 1651247155, 1651253068, 1651267340, 1651265241, 1651264326,
                                                1651275535]


def test_underlying():
    block = 16627530
    name = 'LP Element Principal Token yvCurve-stETH-24FEB23'
    underlying = Element.underlying(name, WALLET, block, blockchain=ETHEREUM)
    assert underlying == [[E_ADDRESS, Decimal('744.5556663118056659868728133')],
                          [ETHTokenAddr.stETH, Decimal('766.3546455242681872680648993')]]


def test_underlying_all():
    block = 16627530
    underlying = Element.underlying_all(WALLET, block, blockchain=ETHEREUM)
    assert underlying == [{'protocol': 'Element',
                           'tranche': 'LP Element Principal Token yvCurve-stETH-24FEB23',
                           'amounts': [[E_ADDRESS, Decimal('744.5556663118056659868728133')],
                                       [ETHTokenAddr.stETH, Decimal('766.3546455242681872680648993')]],
                           'lptoken_address': '0x06325440D014e39736583c165C2963BA99fAf14E',
                           'wallet': '0x849D52316331967b6fF1198e5E32A0eB168D039d'},
                          {'protocol': 'Element',
                           'tranche': 'LP Element Principal Token yvcrvSTETH-28JAN22',
                           'amounts': [[E_ADDRESS, Decimal('0.00005176494310919112209866330221')],
                                       [ETHTokenAddr.stETH, Decimal('0.00005328050866033555510409296175')]],
                           'lptoken_address': '0x06325440D014e39736583c165C2963BA99fAf14E',
                           'wallet': '0x849D52316331967b6fF1198e5E32A0eB168D039d'},
                          {'protocol': 'Element', 'tranche': 'LP Element Principal Token yvcrvSTETH-15APR22',
                           'amounts': [[E_ADDRESS, Decimal('0.0002652668934750846726152143699')],
                                       [ETHTokenAddr.stETH, Decimal('0.0002730333342642093108247451032')]],
                           'lptoken_address': '0x06325440D014e39736583c165C2963BA99fAf14E',
                           'wallet': '0x849D52316331967b6fF1198e5E32A0eB168D039d'}]
