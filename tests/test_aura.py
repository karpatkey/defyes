import json
from decimal import Decimal
from tempfile import NamedTemporaryFile

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr
from karpatkit.node import get_node

from defyes import Aura
from defyes.functions import get_contract

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
WALLET_N6 = "0xC47eC74A753acb09e4679979AfC428cdE0209639"
WALLET_N7 = "0x245cc372c84b3645bf0ffe6538620b04a217988b"  # olympusdao.eth
WALLET_N8 = "0x7cb71c594febace6b6ba11126abeb8cc860cb24a"
WALLET_39d = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
WALLET_e1c = "0x58e6c7ab55aa9012eacca16d1ed4c15795669e1c"

# Gnosis Chain Test Data
WALLET_N1_GC = "0x2E15D7AA0650dE1009710FDd45C3468d75AE1392"
bb_WETH_wstETH_GC = "0xbad20c15a773bf03ab973302f61fabcea5101f0a"


@pytest.mark.skip(reason="Takes too long")
def test_db_uptodate():
    block = 17012817
    with open(Aura.DB_FILE, "r") as db_file:
        db_stored = json.load(db_file)

    with NamedTemporaryFile() as tmpfile:
        db = Aura.update_db(tmpfile.name, block)

    assert db_stored == db


def test_get_pool_rewarder():
    block = 17012817
    node = get_node(Chain.ETHEREUM)
    booster_contract = get_contract(Aura.BOOSTER, Chain.ETHEREUM, web3=node, abi=Aura.ABI_BOOSTER, block=block)
    rewarders = Aura.get_pool_rewarders(booster_contract, balancer_50OHM50wstETH_ADDR, Chain.ETHEREUM, block)

    assert rewarders == [aura_OHMwstETHvault_ADDR]


def test_get_rewards():
    block = 17020318
    node = get_node(Chain.ETHEREUM)
    rewarder_contract = get_contract(
        aura_OHMwstETHvault_ADDR, Chain.ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block
    )

    rewards = Aura.get_rewards(node, rewarder_contract, WALLET_N1, block, Chain.ETHEREUM)
    assert rewards == [EthereumTokenAddr.BAL, Decimal("1.871667357372893151")]


def test_get_extra_rewards():
    block = 17020318
    node = get_node(Chain.ETHEREUM)
    rewarder_contract = get_contract(
        aura_auraBALSTABLEvault_ADDR, Chain.ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block
    )

    rewards = Aura.get_extra_rewards(node, rewarder_contract, WALLET_N2, block, Chain.ETHEREUM)
    assert rewards[0] == [EthereumTokenAddr.AURA, Decimal("0.198621417050926001")]


def test_get_extra_rewards_airdrop():
    block = 16795239
    node = get_node(Chain.ETHEREUM)

    rewards = Aura.get_extra_rewards_airdrop(WALLET_N3, block, Chain.ETHEREUM, web3=node)
    assert rewards == [EthereumTokenAddr.AURA, Decimal("4.902499061089478666")]


def test_get_aura_mint_amount():
    block = 17020318
    node = get_node(Chain.ETHEREUM)
    rewarder_contract = get_contract(
        aura_OHMwstETHvault_ADDR, Chain.ETHEREUM, web3=node, abi=Aura.ABI_REWARDER, block=block
    )

    bal_token, bal_earned = Aura.get_rewards(node, rewarder_contract, WALLET_N1, block, Chain.ETHEREUM)

    aura_minted = Aura.get_aura_mint_amount(node, bal_earned, block, Chain.ETHEREUM, aura_OHMwstETHvault_ADDR)
    assert aura_minted == [EthereumTokenAddr.AURA, Decimal("6.427305705218515080534")]


def test_get_all_rewards():
    block = 17437365
    node = get_node(Chain.ETHEREUM)
    rewards = Aura.get_all_rewards(WALLET_N6, balancer_auraBALSTABLE_ADDR, block, Chain.ETHEREUM, web3=node)
    assert rewards[EthereumTokenAddr.BAL] == Decimal("152.434820779238777988")
    assert rewards[EthereumTokenAddr.AURA] == Decimal("1321.548837567568249031232")


def test_get_locked():
    block = 17026907
    node = get_node(Chain.ETHEREUM)

    aura_locked, reward = Aura.get_locked(WALLET_N4, block, Chain.ETHEREUM, web3=node, reward=True)
    assert aura_locked == [EthereumTokenAddr.AURA, Decimal("1001043.348600000136133708")]
    assert reward == [EthereumTokenAddr.auraBAL, Decimal("3.504020381401144944")]


def test_get_staked():
    block = 17030603
    node = get_node(Chain.ETHEREUM)
    aurabal, bal, bb_a_usd, aura = Aura.get_staked(WALLET_N5, block, Chain.ETHEREUM, web3=node, reward=True)
    assert aurabal == [EthereumTokenAddr.auraBAL, Decimal("76788.355753847540232985")]
    assert bal == [EthereumTokenAddr.BAL, Decimal("5.959443245175147934")]
    assert bb_a_usd == [EthereumTokenAddr.BB_A_USD, Decimal("0")]
    assert aura == [EthereumTokenAddr.AURA, Decimal("20.44089033095075741362")]


def test_underlying():
    block = 17437427
    node = get_node(Chain.ETHEREUM)

    balances = Aura.underlying(WALLET_N6, balancer_auraBALSTABLE_ADDR, block, Chain.ETHEREUM, web3=node)["balances"]
    assert balances[EthereumTokenAddr.BAL] == Decimal("38369.1858805351275913999617")
    assert balances[EthereumTokenAddr.WETH] == Decimal("25.93597482398118254851195716")
    assert balances[EthereumTokenAddr.auraBAL] == Decimal("23621.36000159691559589201902")

    balances = Aura.underlying(
        WALLET_N7, balancer_50OHM50wstETH_ADDR, block, Chain.ETHEREUM, web3=node, decimals=False
    )["balances"]
    assert balances[EthereumTokenAddr.OHM] == Decimal("18201639099.93016793856133145")
    assert balances[EthereumTokenAddr.wstETH] == Decimal("92391287661971156.30751574987")

    balances = Aura.underlying(WALLET_N8, balancer_50COW_50GNO, block, Chain.ETHEREUM, web3=node)["balances"]
    assert balances[EthereumTokenAddr.GNO] == Decimal("4.900304056592836121847285939")
    assert balances[EthereumTokenAddr.COW] == Decimal("7837.281775186463382851500589")

    balances = Aura.underlying(WALLET_e1c, balancer_80GNO_20WETH, block, Chain.ETHEREUM, web3=node)["balances"]
    assert balances[EthereumTokenAddr.GNO] == Decimal("2857.614850691977937126713610")
    assert balances[EthereumTokenAddr.WETH] == Decimal("44.91525928857763211653589999")

    block = 17030603
    node = get_node(Chain.ETHEREUM)

    balances = Aura.underlying(WALLET_N5, balancer_auraBALSTABLE_ADDR, block, Chain.ETHEREUM, web3=node)["balances"]
    assert balances[EthereumTokenAddr.BAL] == Decimal("116433.7136895592470998702397")
    assert balances[EthereumTokenAddr.WETH] == Decimal("108.2807112332312627897739854")
    assert balances[EthereumTokenAddr.auraBAL] == Decimal("63020.44124792096385479026706")

    balances = Aura.underlying(
        WALLET_N1, balancer_50OHM50wstETH_ADDR, block, Chain.ETHEREUM, web3=node, decimals=False
    )["balances"]
    assert balances[EthereumTokenAddr.OHM] == Decimal("1231058673158.390859056243781")
    assert balances[EthereumTokenAddr.wstETH] == Decimal("6057140049865330402.887964025")

    balances = Aura.underlying(WALLET_e1c, balancer_50COW_50GNO, block, Chain.ETHEREUM, web3=node)["balances"]
    assert balances[EthereumTokenAddr.GNO] == Decimal("345.1743699207633159106677341")
    assert balances[EthereumTokenAddr.COW] == Decimal("470374.1748462563486273095973")

    balances = Aura.underlying(WALLET_e1c, balancer_80GNO_20WETH, block, Chain.ETHEREUM, web3=node)["balances"]
    assert balances[EthereumTokenAddr.GNO] == Decimal("2896.528986560673411023728067")
    assert balances[EthereumTokenAddr.WETH] == Decimal("42.53030185358673865030664650")

    block = 29644045
    node = get_node(Chain.GNOSIS)
    underlying = Aura.underlying(WALLET_N1_GC, bb_WETH_wstETH_GC, block, Chain.GNOSIS, web3=node, reward=True)
    assert underlying["balances"][GnosisTokenAddr.WETH] == Decimal("567.2201935195299328414182591")
    assert underlying["balances"][GnosisTokenAddr.wstETH] == Decimal("495.0387012245886911692522812")
    assert underlying["rewards"][GnosisTokenAddr.BAL] == Decimal("10.282343642703308831")
    assert underlying["rewards"][GnosisTokenAddr.AURA] == Decimal("63.00650369330178948597852008")


def test_pool_balances():
    block = 17030603
    balances = Aura.pool_balances(Chain.ETHEREUM, balancer_50OHM50wstETH_ADDR, block)
    assert balances == {
        EthereumTokenAddr.OHM: Decimal("23962.880591594"),
        EthereumTokenAddr.wstETH: Decimal("117.903822869058127723"),
    }


def test_get_compounded():
    block = 17131068
    node = get_node(Chain.ETHEREUM)

    aurabal, aura_rewards = Aura.get_compounded(WALLET_39d, block, Chain.ETHEREUM, web3=node, reward=True)
    assert aurabal == [EthereumTokenAddr.auraBAL, Decimal("173638.950900193303875756")]
    assert aura_rewards == [EthereumTokenAddr.AURA, Decimal("518.423812233736947225")]
