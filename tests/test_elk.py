from decimal import Decimal

from defyes import Elk
from defyes.constants import ETHEREUM, POLYGON, XDAI, ETHTokenAddr, GnosisTokenAddr, PolygonTokenAddr
from defyes.functions import get_contract, get_node

WALLET_N1 = "0x61BEC4cAa9493Df4D8600B63bfC0Ec5FE5A52caC"
WALLET_N2 = "0x7A05B87F0e95c3ABE3f296017C69b5A62C82e286"
WALLET_N2 = "0x52d49ac444e7FEF91B77B112cc5702d6332CD138"


def test_get_pool_address():
    block = 17190299
    node = get_node(ETHEREUM, block)
    addr = Elk.get_pool_address(node, ETHTokenAddr.WETH, ETHTokenAddr.ELK, block, ETHEREUM)
    assert addr == "0xF220eA963D27Ebe782f09403017B29692A4fC4aE"

    node = get_node(POLYGON, block)
    addr = Elk.get_pool_address(node, PolygonTokenAddr.USDC, PolygonTokenAddr.ELK, block, POLYGON)
    assert addr == "0xd7D71e4BC981B50696fa536D330bf745aE563E25"

    node = get_node(XDAI, block)
    addr = Elk.get_pool_address(node, GnosisTokenAddr.XGT, GnosisTokenAddr.ELK, block, XDAI)
    assert addr == "0xc35EcbcA23597747a11E34e733EFe54c2D774F1a"


def test_get_lptoken_data():
    block = 27713194
    node = get_node(POLYGON, block)
    lptoken_address = "0xf99c496C4bc62D4ce47f79bc7D367Af4FFab105B"
    data = Elk.get_lptoken_data(lptoken_address, block, POLYGON, node)
    assert data["decimals"] == 18
    assert data["totalSupply"] == 81447682420161883
    assert data["token0"] == PolygonTokenAddr.USDC
    assert data["token1"] == PolygonTokenAddr.ELK
    assert data["reserves"] == [98702122122, 68490727413069028375424, 1651228303]
    assert data["kLast"] == 0
    assert data["virtualTotalSupply"] == 81447682420161883


def test_get_elk_rewards():
    block = 27713194
    node = get_node(POLYGON, block)
    pool_address = "0xd7D71e4BC981B50696fa536D330bf745aE563E25"
    pool_contract = get_contract(pool_address, POLYGON, node, abi=Elk.ABI_POOL, block=block)
    rewards = Elk.get_elk_rewards(node, pool_contract, WALLET_N1, block, POLYGON, decimals=True)
    assert rewards == [PolygonTokenAddr.ELK, Decimal("16.065293278501301744")]


def test_get_booster_rewards():
    block = 41902330
    node = get_node(POLYGON, block)
    pool_address = "0xDb59EF120FF1FA5013Bb5047e513162003034723"
    pool_contract = get_contract(pool_address, POLYGON, node, abi=Elk.ABI_POOL, block=block)
    rewards = Elk.get_booster_rewards(node, pool_contract, WALLET_N2, block, POLYGON, decimals=True)
    assert rewards == ["0x8A953CfE442c5E8855cc6c61b1293FA648BAE472", Decimal("0")]


def test_get_all_rewards():
    block = 41902330
    node = get_node(POLYGON, block)
    lptoken_address = "0xf99c496C4bc62D4ce47f79bc7D367Af4FFab105B"
    all_rewards = Elk.get_all_rewards(
        WALLET_N1, lptoken_address, block, POLYGON, web3=node, decimals=True, pool_contract=None
    )
    assert all_rewards == [[PolygonTokenAddr.ELK, Decimal("132.497466741066924339")]]


def test_underlying():
    block = 41902330
    node = get_node(POLYGON, block)
    lptoken_address = "0xf99c496C4bc62D4ce47f79bc7D367Af4FFab105B"
    underlying = Elk.underlying(WALLET_N1, lptoken_address, block, POLYGON, node, reward=True)
    assert underlying == [
        [
            [PolygonTokenAddr.USDC, Decimal("0"), Decimal("6842.636923250133597020104181")],
            [PolygonTokenAddr.ELK, Decimal("0"), Decimal("45806.10835723145688926330223")],
        ],
        [[PolygonTokenAddr.ELK, Decimal("132.497466741066924339")]],
    ]


def test_pool_balances():
    block = 41902330
    node = get_node(POLYGON, block)
    lptoken_address = "0xf99c496C4bc62D4ce47f79bc7D367Af4FFab105B"
    balances = Elk.pool_balances(lptoken_address, block, POLYGON, node)
    assert balances == [
        [PolygonTokenAddr.USDC, Decimal("38375.067612")],
        [PolygonTokenAddr.ELK, Decimal("256891.096951031127088188")],
    ]


def test_swap_fees():
    block_start = 42102839
    block_end = 42116600
    lptoken_address = "0xf99c496C4bc62D4ce47f79bc7D367Af4FFab105B"
    fees = Elk.swap_fees(lptoken_address, block_start, block_end, POLYGON)
    assert fees == {
        "swaps": [
            {"block": 42102839, "token": PolygonTokenAddr.USDC, "amount": Decimal("0.1470259439999999885912984610")},
            {"block": 42110314, "token": PolygonTokenAddr.USDC, "amount": Decimal("0.09")},
            {"block": 42110997, "token": PolygonTokenAddr.ELK, "amount": Decimal("0.574093083498075328")},
            {"block": 42112549, "token": PolygonTokenAddr.ELK, "amount": Decimal("0.007968556424428902")},
            {"block": 42116600, "token": PolygonTokenAddr.ELK, "amount": Decimal("0.988986089582322688")},
        ]
    }
