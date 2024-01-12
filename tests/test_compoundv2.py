from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.constants import Address
from karpatkit.node import get_node

from defyes import Compound

CTOKEN_CONTRACTS = {
    "cbat_contract": "0x6C8c6b02E7b2BE14d4fA6022Dfd6d75921D90E4E",
    "cdai_contract": "0x5d3a536E4D6DbD6114cc1Ead35777bAB948E3643",
    "ceth_contract": "0x4Ddc2D193948926D02f9B1fE9e1daa0718270ED5",
    "crep_contract": "0x158079Ee67Fce2f58472A96584A73C7Ab9AC95c1",
    "cusdc_contract": "0x39AA39c021dfbaE8faC545936693aC917d5E7563",
    "cusdt_contract": "0xf650C3d88D12dB855b8bf7D11Be6C55A4e07dCC9",
    "cwbtc_contract": "0xC11b1268C1A384e55C48c2391d8d480264A3A7F4",
    "czrx_contract": "0xB3319f5D18Bc0D84dD1b4825Dcde5d5f7266d407",
    "csai_contract": "0xF5DCe57282A584D2746FaF1593d3121Fcac444dC",
    "cuni_contract": "0x35A18000230DA775CAc24873d00Ff85BccdeD550",
    "ccomp_contract": "0x70e36f6BF80a52b3B46b3aF8e106CC0ed743E8e4",
    "cwbtc2_contract": "0xccF4429DB6322D5C611ee964527D42E5d685DD6a",
    "ctusd_contract": "0x12392F67bdf24faE0AF363c24aC620a2f67DAd86",
    "clink_contract": "0xFAce851a4921ce59e912d19329929CE6da6EB0c7",
    "cmkr_contract": "0x95b4eF2869eBD94BEb4eEE400a99824BF5DC325b",
    "csushi_contract": "0x4B0181102A0112A2ef11AbEE5563bb4a3176c9d7",
    "caave_contract": "0xe65cdB6479BaC1e22340E4E755fAE7E509EcD06c",
    "cyfi_contract": "0x80a2AE356fc9ef4305676f7a3E2Ed04e12C33946",
    "cusdp_contract": "0x041171993284df560249B57358F931D9eB7b925D",
    "cfei_contract": "0x7713DD9Ca933848F6819F38B8352D9A15EA73F67",
}

WALLET_N1 = "0x31cD267D34EC6368eac930Be4f412dfAcc71A844"
WALLET_N2 = "0x99e881e9e89152b0add27c367f0761f0fbe5ddc3"


def test_get_comptoller_address():
    comptroller_address = Compound.get_comptoller_address(Chain.ETHEREUM)
    assert Compound.COMPTROLLER_Chain == comptroller_address


def test_get_compound_lens_address():
    comp_lens_address = Compound.get_compound_lens_address(Chain.ETHEREUM)
    assert Compound.COMPOUND_LENS_Chain == comp_lens_address


def test_get_compound_token_address():
    comp_eth = Compound.get_compound_token_address(Chain.ETHEREUM)
    assert EthereumTokenAddr.COMP == comp_eth


def test_get_ctokens_contract_list():
    block = 16904422
    web3 = get_node(Chain.ETHEREUM)
    ctokens_list = Compound.get_ctokens_contract_list(Chain.ETHEREUM, web3, block)
    assert ctokens_list == list(CTOKEN_CONTRACTS.values())


def test_get_ctoken_data():
    block = 16904422
    wallet1_cdai = Compound.get_ctoken_data(CTOKEN_CONTRACTS["cdai_contract"], WALLET_N1, block, Chain.ETHEREUM)
    assert wallet1_cdai["underlying"] == EthereumTokenAddr.DAI
    assert wallet1_cdai["decimals"] == 8
    assert wallet1_cdai["borrowBalanceStored"] == 0
    assert wallet1_cdai["balanceOf"] == 4505674362
    assert wallet1_cdai["exchangeRateStored"] == 221942359677997719508746620

    block = 16906410
    wallet1_ceth = Compound.get_ctoken_data(CTOKEN_CONTRACTS["ceth_contract"], WALLET_N1, block, Chain.ETHEREUM)
    assert wallet1_ceth["underlying"] == Address.ZERO
    assert wallet1_ceth["decimals"] == 8
    assert wallet1_ceth["borrowBalanceStored"] == 0
    assert wallet1_ceth["balanceOf"] == 4979680
    assert wallet1_ceth["exchangeRateStored"] == 200816109095853438085339051

    block = 16906410
    wallet2_ccomp = Compound.get_ctoken_data(CTOKEN_CONTRACTS["ccomp_contract"], WALLET_N2, block, Chain.ETHEREUM)
    assert wallet2_ccomp["underlying"] == EthereumTokenAddr.COMP
    assert wallet2_ccomp["decimals"] == 8
    assert wallet2_ccomp["borrowBalanceStored"] == 0
    assert wallet2_ccomp["balanceOf"] == 24296781813013
    assert wallet2_ccomp["exchangeRateStored"] == 204174793505775477876721754


def test_underlying():
    block = 16904422
    node = get_node(Chain.ETHEREUM)
    dai_underlying = Compound.underlying(WALLET_N1, EthereumTokenAddr.DAI, block, Chain.ETHEREUM, web3=node)
    assert dai_underlying == [["0x6B175474E89094C44Da98b954EedeAC495271d0F", Decimal("0.9999999998429369002850268805")]]

    block = 16906410
    eth_underlying = Compound.underlying(WALLET_N1, Address.ZERO, block, Chain.ETHEREUM, web3=node)
    assert eth_underlying == [
        ["0x0000000000000000000000000000000000000000", Decimal("0.0009999999621424394485648011655")]
    ]


def test_underlying_all():
    block = 16906410
    node = get_node(Chain.ETHEREUM)
    underlyings = Compound.underlying_all(WALLET_N1, block, Chain.ETHEREUM, web3=node)
    assert underlyings == [
        [EthereumTokenAddr.DAI, Decimal("1.000010884057654258470225384")],
        [Address.ZERO, Decimal("0.0009999999621424394485648011655")],
    ]


def test_all_comp_rewards():
    block = 16924820
    node = get_node(Chain.ETHEREUM)
    rewards = Compound.all_comp_rewards(WALLET_N1, block, Chain.ETHEREUM, web3=node)
    assert rewards[0][0] == EthereumTokenAddr.COMP
    assert rewards[0][1] == Decimal("0.000001508535739321")


def test_unwrap():
    block = 16924820
    node = get_node(Chain.ETHEREUM)
    wallet1_cdai = Compound.get_ctoken_data(
        CTOKEN_CONTRACTS["cdai_contract"], WALLET_N1, block, Chain.ETHEREUM, web3=node
    )
    ctoken_amount = wallet1_cdai["balanceOf"]
    ctoken_address = CTOKEN_CONTRACTS["cdai_contract"]
    unwrapped_data = Compound.unwrap(ctoken_amount, ctoken_address, block, Chain.ETHEREUM, web3=node)
    assert unwrapped_data == [EthereumTokenAddr.DAI, Decimal("100012432.3088823602890022154")]


def test_get_apr():
    block = 16924820
    node = get_node(Chain.ETHEREUM)
    comp_apr = Compound.get_apr(EthereumTokenAddr.COMP, block, Chain.ETHEREUM, web3=node)
    assert comp_apr == [
        {"metric": "apr", "type": "supply", "value": Decimal("0.002830267264410439852176000")},
        {"metric": "apr", "type": "borrow", "value": Decimal("0.055007566655502029090688000")},
    ]

    dai_apy = Compound.get_apr(EthereumTokenAddr.DAI, block, Chain.ETHEREUM, web3=node, apy=True)
    assert dai_apy == [
        {"metric": "apy", "type": "supply", "value": Decimal("0.017116487300260146197020843")},
        {"metric": "apy", "type": "borrow", "value": Decimal("0.035955872211446296931789467")},
    ]

    dai_apr_with_contract = Compound.get_apr(
        EthereumTokenAddr.DAI, block, Chain.ETHEREUM, web3=node, ctoken_address=CTOKEN_CONTRACTS["cdai_contract"]
    )
    assert dai_apr_with_contract == [
        {"metric": "apr", "type": "supply", "value": Decimal("0.016971650630021105741808000")},
        {"metric": "apr", "type": "borrow", "value": Decimal("0.035324548559412767558064000")},
    ]


def test_get_comp_apr():
    block = 16924820
    node = get_node(Chain.ETHEREUM)
    usdt_comp_apr = Compound.get_comp_apr(EthereumTokenAddr.USDT, block, Chain.ETHEREUM, web3=node)
    assert usdt_comp_apr == [
        {"metric": "apr", "type": "supply", "value": Decimal("0")},
        {"metric": "apr", "type": "borrow", "value": Decimal("0.004109317817792878835568000")},
    ]

    dai_comp_apy = Compound.get_comp_apr(EthereumTokenAddr.DAI, block, Chain.ETHEREUM, web3=node, apy=True)
    assert dai_comp_apy == [
        {"metric": "apy", "type": "supply", "value": Decimal("0.007943711809619570636738672")},
        {"metric": "apy", "type": "borrow", "value": Decimal("0.014096985721529171800616936")},
    ]

    sushi_apr_contract = Compound.get_comp_apr(
        EthereumTokenAddr.SUSHI, block, Chain.ETHEREUM, web3=node, ctoken_address=CTOKEN_CONTRACTS["csushi_contract"]
    )
    assert sushi_apr_contract == [
        {"metric": "apr", "type": "supply", "value": Decimal("0")},
        {"metric": "apr", "type": "borrow", "value": Decimal("0")},
    ]
