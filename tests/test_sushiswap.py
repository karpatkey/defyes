from decimal import Decimal

from defyes import SushiSwap
from defyes.cache import const_call
from defyes.constants import CVX_ETH, ETHEREUM, SUSHI_ETH, USDC_ETH, WETH_ETH, XDAI
from defyes.functions import get_node

SUSHISWAP_POOL_USDC_WETH = "0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"
UNUSED_ADDRESS = "0xCafe7CceDfB2deBE0a49830D3C2777721E3728A5"
TEST_BLOCK = 16836190


def test_get_lptoken_data():
    data = SushiSwap.get_lptoken_data(SUSHISWAP_POOL_USDC_WETH, TEST_BLOCK, ETHEREUM)
    assert data["token0"] == USDC_ETH
    assert data["token1"] == WETH_ETH
    assert data["decimals"] == 18


def test_get_lptoken_data_on_gnosis_differ_to_ethereum_when_using_const_call():
    web3 = get_node(XDAI, block=16836190)
    contract = SushiSwap.get_chef_contract(web3=web3, block="latest", blockchain=XDAI)
    gnosis_lptoken0_address = const_call(contract.functions.lpToken(0))
    web3 = get_node(ETHEREUM, block=16836190)
    contract = SushiSwap.get_chef_contract(web3=web3, block="latest", blockchain=ETHEREUM)
    eth_lptoken0_address = const_call(contract.functions.lpToken(0))
    assert gnosis_lptoken0_address != eth_lptoken0_address


def test_underlying_of_empty_address():
    data = SushiSwap.underlying(UNUSED_ADDRESS, SUSHISWAP_POOL_USDC_WETH, TEST_BLOCK, ETHEREUM)
    assert data == [[USDC_ETH, Decimal("0"), Decimal("0")], [WETH_ETH, Decimal("0"), Decimal("0")]]


def test_underlying_of_empty_address_with_rewards():
    data = SushiSwap.underlying(
        UNUSED_ADDRESS, SUSHISWAP_POOL_USDC_WETH, TEST_BLOCK, ETHEREUM, reward=True, decimals=True
    )
    assert data == [
        [[USDC_ETH, Decimal("0"), Decimal("0")], [WETH_ETH, Decimal("0"), Decimal("0")]],
        [[SUSHI_ETH, Decimal("0")]],
    ]


def test_get_pool_info_v1():
    web3 = get_node(ETHEREUM)
    data = SushiSwap.get_pool_info(web3, SUSHISWAP_POOL_USDC_WETH, block=TEST_BLOCK, blockchain=ETHEREUM, use_db=True)
    assert data["pool_info"] == {"poolId": 1, "allocPoint": 8300}
    assert data["totalAllocPoint"] == 1639550


def test_get_pool_info_v2():
    web3 = get_node(ETHEREUM)
    data = SushiSwap.get_pool_info(
        web3, "0x269Db91Fc3c7fCC275C2E6f22e5552504512811c", block=TEST_BLOCK, blockchain=ETHEREUM, use_db=True
    )
    assert data["pool_info"] == {"poolId": 3, "allocPoint": 5}
    assert data["totalAllocPoint"] == 1125


def test_get_pool_info_v2_without_db():
    web3 = get_node(ETHEREUM)
    data = SushiSwap.get_pool_info(
        web3, "0x269Db91Fc3c7fCC275C2E6f22e5552504512811c", block=TEST_BLOCK, blockchain=ETHEREUM, use_db=False
    )
    assert data["pool_info"] == {"poolId": 3, "allocPoint": 5}
    assert data["totalAllocPoint"] == 1125


def test_get_virtual_total_supply():
    supply = SushiSwap.get_virtual_total_supply(SUSHISWAP_POOL_USDC_WETH, TEST_BLOCK, ETHEREUM)
    assert supply == Decimal("233694888028051879.8288163543")


def test_get_rewarder_contract():
    web3 = get_node(ETHEREUM)
    contract = SushiSwap.get_chef_contract(web3, TEST_BLOCK, ETHEREUM)
    rewarder = SushiSwap.get_rewarder_contract(web3, TEST_BLOCK, ETHEREUM, contract, pool_id=1)
    assert rewarder.address == "0x9e01aaC4b3e8781a85b21d9d9F848e72Af77B362"


def test_get_rewards():
    web3 = get_node(ETHEREUM)
    contract = SushiSwap.get_chef_contract(web3, TEST_BLOCK, ETHEREUM)
    rewards = SushiSwap.get_rewards(web3, UNUSED_ADDRESS, contract, pool_id=1, block=TEST_BLOCK, blockchain=ETHEREUM)
    assert rewards == [[CVX_ETH, Decimal("0")]]


def test_pool_balances():
    balances = SushiSwap.pool_balances(SUSHISWAP_POOL_USDC_WETH, block=TEST_BLOCK, blockchain=ETHEREUM)
    assert balances == [[USDC_ETH, Decimal("16413544.906577")], [WETH_ETH, Decimal("9860.137476763535111002")]]


def test_get_rewards_per_unit():
    rwds = SushiSwap.get_rewards_per_unit(SUSHISWAP_POOL_USDC_WETH, block=TEST_BLOCK, blockchain=ETHEREUM)
    assert rwds == [{"sushiPerBlock": Decimal("506236467323350919.4596078192"), "sushi_address": SUSHI_ETH}]


def test_get_wallet_by_tx():
    wallet = SushiSwap.get_wallet_by_tx(SUSHISWAP_POOL_USDC_WETH, block=TEST_BLOCK, blockchain=ETHEREUM)
    assert wallet == "0x9a044da6762352cefc5f7f1eaf1bda7f1e60fd11"


def test_swap_fees():
    fees = SushiSwap.swap_fees(
        SUSHISWAP_POOL_USDC_WETH, block_start=TEST_BLOCK, block_end=TEST_BLOCK + 100, blockchain=ETHEREUM
    )
    assert fees == {
        "swaps": [
            {"block": 16836208, "token": WETH_ETH, "amount": Decimal("0.001260902533618112")},
            {"block": 16836209, "token": WETH_ETH, "amount": Decimal("0.00201")},
            {"block": 16836228, "token": WETH_ETH, "amount": Decimal("0.000297375")},
            {"block": 16836229, "token": USDC_ETH, "amount": Decimal("0.9")},
            {"block": 16836265, "token": WETH_ETH, "amount": Decimal("0.00078")},
            {"block": 16836287, "token": USDC_ETH, "amount": Decimal("0.75")},
        ]
    }
