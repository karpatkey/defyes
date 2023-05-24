from decimal import Decimal

from defi_protocols import Rocket
from defi_protocols.constants import E_ADDRESS, ETHEREUM

ANKR_ADDR = '0xE95A203B1a91a908F9B9CE46459d101078c2c3cb'
TOKEN_ADDR = '0xae78736Cd615f374D3085123A210448E74Fc6393'
WALLET = '0x834b1E1E6026E4e93833423d6462525AA2dee86F'
BLOCKCHAIN = ETHEREUM

def test_underlying():
    block = 17293000
    underlying = Rocket.underlying(WALLET, TOKEN_ADDR, block)
    assert underlying == [[E_ADDRESS, Decimal('991.795974817271166526')]]

def test_underlying_not_reth_address():
    block = 17293000
    underlying = Rocket.underlying(WALLET, ANKR_ADDR, block, BLOCKCHAIN)
    assert underlying == 'not a Ankr Staked ETH address'