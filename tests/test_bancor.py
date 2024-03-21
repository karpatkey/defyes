from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.constants import Address
from web3 import Web3

from defyes import Bancor

WALLET_N1 = "0x849d52316331967b6ff1198e5e32a0eb168d039d"
WALLET_N2 = "0xc0167f4B1bb78912DF9920Bd146151942620Da15"

bnICHI_ADDR = "0x36FAbE4cAeF8c190550b6f93c306A5644E7dCef6"
bnETH_ADDR = "0x256Ed1d83E3e4EfDda977389A5389C3433137DDA"



def test_token():
    block = 17067718

    result = Bancor.get_protocol_data_for(bnICHI_ADDR, WALLET_N1, Chain.ETHEREUM, block, reward=True)
    assert result == [[EthereumTokenAddr.ICHI, Decimal("44351.005182315")], [EthereumTokenAddr.BNT, Decimal("0")]]
    result = Bancor.get_protocol_data_for(bnETH_ADDR, WALLET_N2, Chain.ETHEREUM, block, reward=True)
    assert result == [[Address.E, Decimal("0.149703304228299349")], [EthereumTokenAddr.BNT, Decimal("0")]]


# @pytest.mark.skip(reason="It takes too long.")
def test_all_tokens():
    block = 17067718

    result = Bancor.get_protocol_data(Chain.ETHEREUM, WALLET_N2, block, reward=True)
    
    expected_balances = [
        [[Address.E, Decimal("0.149703304228299349")], [EthereumTokenAddr.BNT, Decimal("0")]],
        *(list() for _ in range(147)),  # plus 147 empty lists
    ]
    expected_result = {
        "protocol": "Bancor",
        "blockchain": Chain.ETHEREUM,
        "wallet": Web3.to_checksum_address(WALLET_N2),
        "block_id": block,
        "positions_key": "",
        "positions": expected_balances,
        "version": 0,
    }
    assert result == expected_result
