import itertools
from decimal import Decimal

import pytest

from defyes import pretty
from defyes.constants import Chain, ETHTokenAddr, GnosisTokenAddr, PolygonTokenAddr
from defyes.types import Addr, Token, TokenAmount

DAI = Token.get_instance(ETHTokenAddr.DAI, Chain.ETHEREUM)
USDC = Token.get_instance(ETHTokenAddr.USDC, Chain.ETHEREUM)


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


amounts = ["1_000.234", 1002300, "0.433222344", Decimal("3_902_932_323.22133")]
tokens_data = [
    (PolygonTokenAddr.MAI, Chain.POLYGON),
    (GnosisTokenAddr.GNO, Chain.GNOSIS),
    (ETHTokenAddr.BB_A_USD, Chain.ETHEREUM),
]
results = itertools.product(
    ["1_000.234", "1_002_300", "0.433222344", "3_902_932_323.22133"], ["miMATIC", "GNO", "bb-a-USD"]
)


def generate_parameters():
    for (amount, token_data), (expected_value, expected_token) in zip(itertools.product(amounts, tokens_data), results):
        yield amount, token_data, f"'{expected_value}'*{expected_token}"


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
    DAI = Token.get_instance(ETHTokenAddr.DAI, Chain.ETHEREUM)
    DAI2 = Token(ETHTokenAddr.DAI, Chain.ETHEREUM)
    token1 = TokenAmount("1", DAI)
    token2 = TokenAmount.from_teu("1_000_000_000_000_000_000", DAI2)
    assert token1 == token2


def test_token_amount_from_teu():
    assert 1 * USDC == TokenAmount.from_teu(1_000_000, USDC)


def test_repr():
    assert repr("1.004" * USDC) == "'1.004'*USDC"
    assert "1.004" * USDC == "'1.004'*USDC"  # __eq__ to str
    assert repr("0.004" * USDC) == "'0.004'*USDC"
    assert repr("0.0004" * USDC) == "'400e-6'*USDC"
    assert repr("0.00004" * USDC) == "'40e-6'*USDC"
    assert repr("0.000004" * USDC) == "'4e-6'*USDC"
    assert repr(Decimal("1.00004") * USDC) == "'1.00004'*USDC"
    assert repr("0.00005938" * DAI) == "'59.38e-6'*DAI"
    assert repr("0.0000005938" * DAI) == "'593.8e-9'*DAI"


@pytest.mark.parametrize("amount_str", ["1e-19", "1.1e-18"])
def test_token_amount_avoid_precision_loss_for_teu_amount_and_as_dict(amount_str):
    """
    Avoiding precision loss as the teu value 0.1 still has non zero decimals.
    """
    ta = TokenAmount(amount_str, DAI)

    with pytest.raises(ValueError):
        ta.teu_amount

    with pytest.raises(ValueError):
        ta.as_dict(decimal=True)

    with pytest.raises(ValueError):
        ta.as_dict(decimal=False)


@pytest.mark.parametrize("amount_str", ["1e-19", "1.1e-18", "1", "1e-18", "-2"])
def test_token_amount_allow_construtor_or_rmul(amount_str):
    """
    Allow the construction by contructor or rmul even if the amount has fractional tau.
    """
    amount_str * DAI
    TokenAmount(amount_str, DAI)


def test_token_amount_no_precision_loss():
    ta = "1e-18" * DAI
    assert ta.teu_amount == 1


def test_token_amount_explicit_precision_loss():
    ta = "1.1e-18" * DAI
    assert ta.teu_rounded.teu_amount == 1
