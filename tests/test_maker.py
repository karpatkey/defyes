
from defi_protocols import Maker
from defi_protocols.functions import get_node
from defi_protocols.constants import ETHEREUM, DAI_ETH, WETH_ETH, ETHTokenAddr


TEST_BLOCK = 17070386
WEB3 = get_node(blockchain=ETHEREUM, block=TEST_BLOCK)
# TEST_WALLET = '0xf929122994e177079c924631ba13fb280f5cd1f9'
TEST_WALLET_1 = '0x4971DD016127F390a3EF6b956Ff944d0E2e1e462'
TEST_WALLET_2 = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
VAULT_ID = 27353
TEST_WALLET_2_PROXY = '0xD758500ddEc05172aaA035911387C8E0e789CF6a'


def test_get_vault_data():
    x = Maker.get_vault_data(VAULT_ID, TEST_BLOCK, WEB3)
    assert x == {'mat': 1.6,
                 'gem': ETHTokenAddr.stETH,
                 'dai': DAI_ETH, 
                 'ink': 57328.918780519,
                 'art': 21811755.174275193,
                 'Art': 131281671.56044462,
                 'rate': 1.0337823922958922,
                 'spot': 1456.9286150664384,
                 'line': 154522941.83599702,
                 'dust': 7500.0}


def test_underlying():
    x = Maker.underlying(VAULT_ID, TEST_BLOCK, WEB3)
    assert x == [[ETHTokenAddr.stETH, 57328.918780519],
                 [DAI_ETH, -22548608.444234513]]


def test_get_delegated_MKR():
    x = Maker.get_delegated_MKR(TEST_WALLET_1, TEST_BLOCK, WEB3,
                                decimals=False)
    assert x == [[ETHTokenAddr.MKR, 583805204609736124092]]


def test_proxies():
    pr = Maker.ProxyRegistry(TEST_BLOCK)
    p = pr.proxies(TEST_WALLET_2)
    assert p == TEST_WALLET_2_PROXY


def test_vault_count():
    cdp = Maker.CDPManager(TEST_BLOCK)
    c = cdp.count(TEST_WALLET_2_PROXY)
    assert c == 2


def test_vaults_from_wallet():
    pr = Maker.ProxyRegistry(TEST_BLOCK)
    cdp = Maker.CDPManager(pr.block)
    _vs = cdp.vaults(pr.proxies(TEST_WALLET_2))
    assert _vs == [27353, 29954]
