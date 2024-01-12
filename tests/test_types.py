import itertools
from decimal import Decimal

import pytest
from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr, GnosisTokenAddr, PolygonTokenAddr

from defyes import pretty
from defyes.types import Addr, Token, TokenAmount


def test_addr():
    addr = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
    assert addr == Addr(0x849D52316331967B6FF1198E5E32A0EB168D039D)

    with pytest.raises(Exception) as e:
        Addr(0x84D52316331967B6FF1198E5E32A0EB168D039D)
    assert e.type == ValueError

    assert addr == Addr("0x849D52316331967b6fF1198e5E32A0eB168D039d")

    with pytest.raises(Exception) as e:
        Addr("0x849D52316331967B6FF1198E5E32A0EB168D039D")
    assert e.type == Addr.ChecksumError


amounts = ["1000.234", 1002300, "0.433222344", Decimal("3902932323.22133")]
tokens_data = [
    (PolygonTokenAddr.MAI, Chain.POLYGON),
    (GnosisTokenAddr.GNO, Chain.GNOSIS),
    (EthereumTokenAddr.BB_A_USD, Chain.ETHEREUM),
]
results = itertools.product(
    ["1_000.234", "1_002_300", "0.433222344", "3_902_932_323.22133"], ["miMATIC", "GNO", "bb-a-USD"]
)


def generate_parameters():
    for (amount, token_data), (expected_value, expected_token) in zip(itertools.product(amounts, tokens_data), results):
        yield amount, token_data, f"{expected_value}*{expected_token}"


@pytest.mark.parametrize("amount, token_data, expected_repr", list(generate_parameters()))
def test_tokens(amount, token_data, expected_repr):
    addr, chain = token_data
    token = Token(addr, chain)
    token_amount = amount * token
    assert addr == str(token)
    print()
    pretty.print(token_amount)
    assert token_amount == expected_repr


def test_compare_token_amount():
    DAI = Token.get_instance(EthereumTokenAddr.DAI, Chain.ETHEREUM)
    DAI2 = Token(EthereumTokenAddr.DAI, Chain.ETHEREUM)
    token1 = TokenAmount("1", DAI)
    token2 = TokenAmount.from_teu("1000000000000000000", DAI2)
    assert token1 == token2


def test_repr():
    DAI = Token.get_instance(EthereumTokenAddr.DAI, Chain.ETHEREUM)
    USDC = Token.get_instance(EthereumTokenAddr.USDC, Chain.ETHEREUM)
    assert "0.0004" * USDC == "0.0004*USDC"
    assert "0.00004" * USDC == "40.00000*teuUSDC"
    assert Decimal("1.00004") * USDC == "1.00004*USDC"
    assert "0.00005938" * DAI == "0.00005938*DAI"
    assert "0.0000005938" * DAI == "593_800_000_000.0000000000*teuDAI"
