from decimal import Decimal

from defi_protocols import Notional
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node


cETH = '0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5'
nETH = '0xabc07BF91469C5450D6941dD0770E6E6761B90d6'
cDAI = '0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643'
nDAI = '0x6EbcE2453398af200c688C7c4eBD479171231818'
cUSDC = '0x39AA39c021dfbaE8faC545936693aC917d5E7563'
nUSDC = '0x18b0Fc5A233acF1586Da7C199Ca9E3f486305A29'
cWBTC = '0xccF4429DB6322D5C611ee964527D42E5d685DD6a'
nWBTC = '0x0Ace2DC3995aCD739aE5e0599E71A5524b93b886'

WALLET_N1 = '0x79a98A9F41051e119cad1b9fFeFe523cd0Be65f0'


def test_get_nproxy_address():
    nproxy_address = Notional.get_nproxy_address(ETHEREUM)
    assert Notional.NPROXY_ETHEREUM == nproxy_address


def test_get_snote_address():
    snote_address = Notional.get_snote_address(ETHEREUM)
    assert Notional.SNOTE_ETH == snote_address


def test_get_markets_data():
    block = 17049450
    node = get_node(ETHEREUM, block)

    eth, dai, usdc, wbtc = Notional.get_markets_data(block, ETHEREUM, web3=node)
    assert eth['currencyId'] == 1
    assert eth['underlyingToken'] == {'address': ZERO_ADDRESS, 'decimals': 1000000000000000000}
    assert eth['cToken'] == {'address': cETH,
                             'decimals': 100000000,
                             'rate': Decimal('0.0200824210777124347051837671')}
    assert eth['nToken'] == {'address': nETH,
                             'decimals': 100000000,
                             'rate': Decimal('0.02026470831212603197181101555')}
    assert dai['currencyId'] == 2
    assert dai['underlyingToken'] == {'address': ETHTokenAddr.DAI, 'decimals': 1000000000000000000}
    assert dai['cToken'] == {'address': cDAI,
                             'decimals': 100000000,
                             'rate': Decimal('0.0222122989542929724290904699')}
    assert dai['nToken'] == {'address': nDAI,
                             'decimals': 100000000,
                             'rate': Decimal('0.02203539273368051175084592366')}
    assert usdc['currencyId'] == 3
    assert usdc['underlyingToken'] == {'address': ETHTokenAddr.USDC, 'decimals': 1000000}
    assert usdc['cToken'] == {'address': cUSDC,
                              'decimals': 100000000,
                              'rate': Decimal('0.0228110536444391')}
    assert usdc['nToken'] == {'address': nUSDC,
                              'decimals': 100000000,
                              'rate': Decimal('0.02259557247497749094707358256')}
    assert wbtc['currencyId'] == 4
    assert wbtc['underlyingToken'] == {'address': ETHTokenAddr.WBTC, 'decimals': 100000000}
    assert wbtc['cToken'] == {'address': cWBTC,
                              'decimals': 100000000,
                              'rate': Decimal('0.020074330123395874')}
    assert wbtc['nToken'] == {'address': nWBTC,
                              'decimals': 100000000,
                              'rate': Decimal('0.02011875437472354694396376286')}


def test_get_all_note_rewards():
    block = 17049450
    node = get_node(ETHEREUM, block)

    note_reward = Notional.all_note_rewards(WALLET_N1, block, ETHEREUM, web3=node)
    assert note_reward == [[ETHTokenAddr.NOTE, Decimal('20787.1858851')]]


def test_get_staked():
    block = 17049450
    node = get_node(ETHEREUM, block)

    staked = Notional.get_staked(WALLET_N1, block, ETHEREUM, web3=node)
    assert staked == [[ETHTokenAddr.WETH, Decimal('0')], [ETHTokenAddr.NOTE, Decimal('0')]]


def test_underlying_all():
    block = 17049450
    node = get_node(ETHEREUM, block)

    underlying = Notional.underlying_all(WALLET_N1, block, ETHEREUM, web3=node)
    assert underlying == [[ZERO_ADDRESS, Decimal('9.237913695747719964384532866E-9')],
                          [ETHTokenAddr.DAI, Decimal('-209743.3234')],
                          [ETHTokenAddr.USDC, Decimal('836657.9853193511111313755831')]]


def test_underlying():
    block = 17049450
    node = get_node(ETHEREUM, block)

    underlying = Notional.underlying(WALLET_N1, ETHTokenAddr.USDC, block, ETHEREUM, web3=node)
    assert underlying == [[ETHTokenAddr.USDC, Decimal('836657.9853193511111313755831')]]
