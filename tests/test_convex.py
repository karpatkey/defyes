from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.node import get_node

from defyes import Convex
from defyes.functions import get_contract
from defyes.protocols.convex import get_staked_cvx

web3 = get_node(Chain.ETHEREUM)

CRV3CRYPTO = "0xc4AD29ba4B3c580e6D59105FFf484999997675Ff"
cDAI_plus_cUSDC = "0x845838DF265Dcd2c412A1Dc9e959c7d08537f8a2"
steCRV = "0x06325440D014e39736583c165C2963BA99fAf14E"


def test_get_pool_rewarder():
    rewarders = Convex.get_pool_rewarders(EthereumTokenAddr.X3CRV, 16993460)
    assert rewarders == ["0x689440f2Ff927E1f24c72F1087E1FAF471eCe1c8"]


def test_get_rewards():
    rewarders = Convex.get_pool_rewarders(CRV3CRYPTO, 16993460)
    rw_contract = get_contract(rewarders[0], Chain.ETHEREUM, web3=web3, abi=Convex.ABI_REWARDS)
    wallet = "0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C"
    rewards = Convex.get_rewards(web3, rw_contract, wallet, 16993460, Chain.ETHEREUM, decimals=False)
    assert rewards == [EthereumTokenAddr.CRV, Decimal("2628703131997023420479")]


# @pytest.mark.parametrize('lp_token', [CRV3CRYPTO, cDAI_plus_cUSDC, steCRV])
@pytest.mark.parametrize("lp_token", [steCRV])
# @pytest.mark.parametrize('wallet', [TEST_WALLET,
@pytest.mark.parametrize("wallet", ["0x849D52316331967b6fF1198e5E32A0eB168D039d"])
# '0x58e6c7ab55Aa9012eAccA16d1ED4c15795669E1C',
# '0x849D52316331967b6fF1198e5E32A0eB168D039d'])
def test_get_extra_rewards(lp_token, wallet):
    rewarders = Convex.get_pool_rewarders(lp_token, 16993460)
    rw_contract = get_contract(rewarders[0], Chain.ETHEREUM, web3=web3, abi=Convex.ABI_REWARDS)
    extra_rewards = Convex.get_extra_rewards(web3, rw_contract, wallet, 16993460, Chain.ETHEREUM, decimals=False)
    assert extra_rewards == [[EthereumTokenAddr.LDO, Decimal("1680694318843318519229")]]


def test_get_cvx_mint_amount():
    cvx_mint_amount = Convex.get_cvx_mint_amount(
        web3, Decimal("6649.47123882958317496"), 17499865, Chain.ETHEREUM, decimals=False
    )
    assert cvx_mint_amount == [EthereumTokenAddr.CVX, Decimal("106.9162438469377937584223851")]


def test_get_all_rewards():
    all_rewards = Convex.get_all_rewards(
        "0x704617048F435cB679252E24148638211fb4457D", EthereumTokenAddr.X3CRV, 17499865, Chain.ETHEREUM, web3
    )
    assert all_rewards[EthereumTokenAddr.CRV] == Decimal("6649.47123882958317496")
    assert all_rewards[EthereumTokenAddr.CVX] == Decimal("106.9162438469377937584223851")


def test_get_locked():
    locked = Convex.get_locked(
        "0x99e703dA6A29f68a603724BAc8B68d26d235ebf6", 17499865, Chain.ETHEREUM, web3, reward=False, decimals=False
    )
    assert locked == [[EthereumTokenAddr.CVX, Decimal("2269137508655082138108")]]

    locked = Convex.get_locked(
        wallet="0x849d52316331967b6ff1198e5e32a0eb168d039d", block=17499865, blockchain=Chain.ETHEREUM, reward=True
    )
    assert locked == [
        [EthereumTokenAddr.CVX, Decimal("15141.040500434822549545")],
        [EthereumTokenAddr.CVXCRV, Decimal("498.957290776022003025")],
        ["0xFEEf77d3f69374f66429C91d732A244f074bdf74", Decimal("0.706414240457270942")],
        ["0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0", Decimal("5.806260846190998503")],
    ]

    locked = Convex.get_locked(
        wallet="0x849d52316331967b6ff1198e5e32a0eb168d039d", block=17499865, blockchain=Chain.ETHEREUM, reward=True
    )
    assert locked == [
        [EthereumTokenAddr.CVX, Decimal("15141.040500434822549545")],
        [EthereumTokenAddr.CVXCRV, Decimal("498.957290776022003025")],
        ["0xFEEf77d3f69374f66429C91d732A244f074bdf74", Decimal("0.706414240457270942")],
        ["0x3432B6A60D23Ca0dFCa7761B7ab56459D9C964D0", Decimal("5.806260846190998503")],
    ]


def test_get_staked():
    staked = Convex.get_staked(
        "0xFDB3E523fc6F0D93fce8e57e282c503c5384d08F", 17499865, Chain.ETHEREUM, web3, reward=False, decimals=False
    )
    assert staked == [[EthereumTokenAddr.CVX, Decimal("656399329913009873936")]]


def test_underlying():
    underlying = Convex.underlying(
        "0x704617048F435cB679252E24148638211fb4457D",
        EthereumTokenAddr.X3CRV,
        17499865,
        Chain.ETHEREUM,
        web3,
        reward=True,
        decimals=False,
        no_curve_underlying=False,
    )

    assert underlying["balances"][EthereumTokenAddr.DAI] == Decimal("1977384398964183941684361.059")
    assert underlying["balances"][EthereumTokenAddr.USDC] == Decimal("2063566980143.462508297458104")
    assert underlying["balances"][EthereumTokenAddr.USDT] == Decimal("5558574151627.356090237218803")
    assert underlying["rewards"][EthereumTokenAddr.CRV] == Decimal("6649471238829583174960")
    assert underlying["rewards"][EthereumTokenAddr.CVX] == Decimal("106916243846937793758.4223851")


def test_pool_balances():
    balances = Convex.pool_balances(EthereumTokenAddr.X3CRV, 16993460, Chain.ETHEREUM, web3, decimals=False)
    assert balances == [
        [EthereumTokenAddr.DAI, Decimal("165857824629254122209119338")],
        [EthereumTokenAddr.USDC, Decimal("175604425510732")],
        [EthereumTokenAddr.USDT, Decimal("92743777795510")],
    ]


@pytest.mark.skip(reason="Takes too long")
def test_update_db():
    data = Convex.update_db(save_to="/dev/null")
    assert data


def test_get_staked_cvx_balance():
    result = get_staked_cvx(
        "0x205e795336610f5131be52f09218af19f0f3ec60", 19676136, Chain.ETHEREUM, reward=False, decimals=False
    )

    expected_result = {"balances": {"0x62B9c7356A2Dc64a1969e19C23e4f579F9810Aa7": Decimal("2105946483998423352150951")}}

    assert result == expected_result


def test_get_staked_cvx_reward():
    result = get_staked_cvx("0x205e795336610f5131be52f09218af19f0f3ec60", 19676136, Chain.ETHEREUM, reward=True)

    expected_result = {
        "0xD533a949740bb3306d119CC777fa900bA034cd52": Decimal("4296.861415111208660227"),
        "0x4e3FBD56CD56c3e72c1403e103b45Db9da5B9D2B": Decimal("539.434991370424529278"),
        "0x6c3F90f043a72FA612cbac8115EE7e52BDe6E490": Decimal("5163.86230295847308542"),
    }

    assert result == expected_result
