from defi_protocols import Agave
from defi_protocols.constants import XDAI
from defi_protocols.functions import get_node

STK_AGAVE = '0x610525b415c1BFAeAB1a3fc3d85D87b92f048221'
TEST_ADDRESS = '0xc4d46395c01aa86389d4216c2830167878d7cab8'
UNUSED_ADDRESS = '0xcafe6395c01aa86389d4216c2830167878d7cab8'


def test_get_staking_balance():
    TEST_BLOCK = 27038905
    web3 = get_node(blockchain=XDAI, block=TEST_BLOCK)
    data = Agave.get_staked(TEST_ADDRESS, block=TEST_BLOCK, blockchain=XDAI, web3=web3)
    assert data == [[STK_AGAVE, 103.6303835433784]]

    data = Agave.get_staked(UNUSED_ADDRESS, block=TEST_BLOCK, blockchain=XDAI, web3=web3)
    assert data == [[STK_AGAVE, 0.0]]
