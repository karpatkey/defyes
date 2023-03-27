from defi_protocols import Aave
from defi_protocols.constants import ETHEREUM
from defi_protocols.functions import get_node

STK_AAVE = '0x4da27a545c0c5B758a6BA100e3a049001de870f5'
STK_ABPT = '0xa1116930326D21fB917d5A27F1E9943A9595fb47'
UNUSED_ADDRESS = '0xf929122994e177079c924631ba13fb280f5cd1f9'

def test_get_staking_balance():
    web3 = get_node(ETHEREUM)
    data = Aave.get_staked(UNUSED_ADDRESS,block=16870553,blockchain=ETHEREUM,web3=web3)
    assert data == [[STK_AAVE, 11538.124991799179], [STK_ABPT, 0.0]]
