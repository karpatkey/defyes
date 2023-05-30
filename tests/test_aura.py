import pytest
from decimal import Decimal
from tempfile import NamedTemporaryFile
from defi_protocols import Aura
from defi_protocols.constants import ETHEREUM, ETHTokenAddr, ZERO_ADDRESS
from defi_protocols.functions import get_node, get_contract


balancer_50OHM50wstETH_ADDR = "0xd4f79CA0Ac83192693bce4699d0c10C66Aa6Cf0F"
aura_OHMwstETH_TOKEN = "0x0EF97ef0e20F84e82ec2D79CBD9Eda923C3DAF09"
balancer_OHMwstETHgauge_ADDR = "0xE879f17910E77c01952b97E4A098B0ED15B6295c"
aura_OHMwstETHvault_ADDR = "0x636024F9Ddef77e625161b2cCF3A2adfbfAd3615"  # Aura base reward pool
aura_OHMwstETHstash_ADDR = "0x04B4e364FFBF1C8f938D6A6258bDC8cb503DEB64"  # Aura extra reward pool stash

balancer_auraBALSTABLE_ADDR = "0x3dd0843A028C86e0b760b1A76929d1C5Ef93a2dd"
aura_auraBALSTABLE_TOKEN = "0x12e9DA849f12d47707A94e29f781f1cd20A7f49A"
balancer_auraBALSTABLEgauge_ADDR = "0x0312AA8D0BA4a1969Fddb382235870bF55f7f242"
aura_auraBALSTABLEvault_ADDR = "0xACAdA51C320947E7ed1a0D0F6b939b0FF465E4c2"
aura_auraBALSTABLEstash_ADDR = "0x7b3307af981F55C8D6cd22350b08C39Ec7Ec481B"

balancer_50COW_50GNO = "0x92762b42a06dcdddc5b7362cfb01e631c4d44b40"

balancer_80GNO_20WETH = "0xF4C0DD9B82DA36C07605df83c8a416F11724d88b"

WALLET_N1 = "0xb74e5e06f50fa9e4eF645eFDAD9d996D33cc2d9D"
WALLET_N2 = "0x6d707F73f621722fEc0E6A260F43f24cCC8d4997"
WALLET_N3 = "0x76d3a0F4Cdc9E75E0A4F898A7bCB1Fb517c9da88"
WALLET_N4 = "0xB1f881f47baB744E7283851bC090bAA626df931d"
WALLET_N5 = "0x36cc7B13029B5DEe4034745FB4F24034f3F2ffc6"
WALLET_39d = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
WALLET_e1c = "0x58e6c7ab55aa9012eacca16d1ed4c15795669e1c"


@pytest.mark.xfail(reason="Checking if db needs update")
def test_db_uptodate():
    with NamedTemporaryFile() as tmpfile:
        uptodate = Aura.update_db(tmpfile.name)
        assert uptodate is False, "DB is outdated"


def test_get_pool_info():
    block = 17012817
    node = get_node(ETHEREUM, block)
    booster_contract = get_contract(Aura.BOOSTER, ETHEREUM, web3=node, abi=Aura.ABI_BOOSTER, block=block)
    pool_info = Aura.get_pool_info(booster_contract, balancer_50OHM50wstETH_ADDR, block)

    assert pool_info == [balancer_50OHM50wstETH_ADDR,
                         aura_OHMwstETH_TOKEN,
                         balancer_OHMwstETHgauge_ADDR,
                         aura_OHMwstETHvault_ADDR,
                         aura_OHMwstETHstash_ADDR,
                         False]


def test_get_rewards():
    block = 17020318
    node = get_node(ETHEREUM, block)
    rewarder_contract = get_contract(aura_OHMwstETHvault_ADDR, ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block)

    rewards = Aura.get_rewards(node, rewarder_contract, WALLET_N1, block, ETHEREUM)
    assert rewards == [ETHTokenAddr.BAL, Decimal('1.871667357372893151')]


def test_get_extra_rewards():
    block = 17020318
    node = get_node(ETHEREUM, block)
    rewarder_contract = get_contract(aura_auraBALSTABLEvault_ADDR, ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block)

    rewards = Aura.get_extra_rewards(node, rewarder_contract, WALLET_N2, block, ETHEREUM)
    assert rewards[0] == [ETHTokenAddr.AURA, Decimal('0.198621417050926001')]


def test_get_extra_rewards_airdrop():
    block = 16795239
    node = get_node(ETHEREUM, block)

    rewards = Aura.get_extra_rewards_airdrop(WALLET_N3, block, ETHEREUM, web3=node)
    assert rewards == [ETHTokenAddr.AURA, Decimal('4.902499061089478666')]


def test_get_aura_mint_amount():
    block = 17020318
    node = get_node(ETHEREUM, block)
    rewarder_contract = get_contract(aura_OHMwstETHvault_ADDR, ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block)

    bal_token, bal_earned = Aura.get_rewards(node, rewarder_contract, WALLET_N1, block, ETHEREUM)

    aura_minted = Aura.get_aura_mint_amount(node, bal_earned, block, ETHEREUM)
    assert aura_minted == [ETHTokenAddr.AURA, Decimal('6.428092448343376000232498822')]


def test_get_all_rewards():
    block = 17018536
    node = get_node(ETHEREUM, block)
    bal_rewards, aura_rewards = Aura.get_all_rewards(WALLET_N2, balancer_auraBALSTABLE_ADDR, block, ETHEREUM, web3=node)
    assert bal_rewards == [ETHTokenAddr.BAL,  Decimal('0.064024732718053571')]
    assert aura_rewards == [ETHTokenAddr.AURA, Decimal('0.406220080813836023749526866')]


def test_get_locked():
    block = 17026907
    node = get_node(ETHEREUM, block)

    aura_locked, reward = Aura.get_locked(WALLET_N4, block, ETHEREUM, web3=node, reward=True)
    assert aura_locked == [ETHTokenAddr.AURA, Decimal('1001043.348600000136133708')]
    assert reward == [ETHTokenAddr.auraBAL, Decimal('3.504020381401144944')]


def test_get_staked():
    block = 17030603
    node = get_node(ETHEREUM, block)
    aurabal, bal, bb_a_usd, aura = Aura.get_staked(WALLET_N5, block, ETHEREUM, web3=node, reward=True)
    assert aurabal == [ETHTokenAddr.auraBAL, Decimal('76788.355753847540232985')]
    assert bal == [ETHTokenAddr.BAL, Decimal('5.959443245175147934')]
    assert bb_a_usd == [ETHTokenAddr.BB_A_USD, Decimal('0')]
    assert aura == [ETHTokenAddr.AURA, Decimal('20.42193231463296825575926092')]


def test_underlying():
    block = 17030603
    node = get_node(ETHEREUM, block)

    bal, eth, aurabal = Aura.underlying(WALLET_N5, balancer_auraBALSTABLE_ADDR, block, ETHEREUM, web3=node)
    assert bal == [ETHTokenAddr.BAL, Decimal('116433.7136895592470998702397')]
    assert eth == [ETHTokenAddr.WETH, Decimal('108.2807112332312627897739854')]
    assert aurabal == [ETHTokenAddr.auraBAL, Decimal('63020.44124792096385479026706')]

    ohm, steth = Aura.underlying(WALLET_N1, balancer_50OHM50wstETH_ADDR, block, ETHEREUM, web3=node, decimals=False)
    assert ohm == [ETHTokenAddr.OHM, Decimal('1231058673158.390859056243781')]
    assert steth == [ETHTokenAddr.wstETH, Decimal('6057140049865330402.887964025')]

    gno, cow = Aura.underlying(WALLET_e1c, balancer_50COW_50GNO, block, ETHEREUM, web3=node)
    assert gno == [ETHTokenAddr.GNO, Decimal('345.1743699207633159106677341')]
    assert cow == [ETHTokenAddr.COW, Decimal('470374.1748462563486273095973')]

    gno, weth = Aura.underlying(WALLET_e1c, balancer_80GNO_20WETH, block, ETHEREUM, web3=node)
    assert gno == [ETHTokenAddr.GNO, Decimal('2896.528986560673411023728067')]
    assert weth == [ETHTokenAddr.WETH, Decimal('42.53030185358673865030664650')]


def test_pool_balances():
    block = 17030603
    node = get_node(ETHEREUM, block)

    ohm, steth = Aura.pool_balances(balancer_50OHM50wstETH_ADDR, block, ETHEREUM, web3=node)
    assert ohm == [ETHTokenAddr.OHM, Decimal('23962.880591594')]
    assert steth == [ETHTokenAddr.wstETH, Decimal('117.903822869058127723')]


def test_get_compounded():
    block = 17131068
    node = get_node(ETHEREUM, block)

    aurabal, aura_rewards = Aura.get_compounded(WALLET_39d, block, ETHEREUM, web3=node, reward=True)
    assert aurabal == [ETHTokenAddr.auraBAL, Decimal('173638.950900193303875756')]
    assert aura_rewards == [ETHTokenAddr.AURA, Decimal('518.423812233736947225')]
