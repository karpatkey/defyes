from decimal import Decimal

import pytest

from defyes.portfolio import Chain, Token, UnderlyingTokenPosition


def test_add():
    DAI = Token.objs.get(chain=Chain.ETHEREUM, symbol="DAI")
    tp0 = UnderlyingTokenPosition(token=DAI, amount=Decimal(1))
    tp1 = UnderlyingTokenPosition(token=DAI, amount=Decimal(2))
    tp_sum = tp0 + tp1
    assert tp_sum.amount == 3
    assert tp_sum.token == DAI


def test_add_fail():
    tp0 = UnderlyingTokenPosition(token=Token.objs.get(chain=Chain.ETHEREUM, symbol="DAI"), amount=Decimal(1))
    tp1 = UnderlyingTokenPosition(token=Token.objs.get(chain=Chain.ETHEREUM, symbol="sDAI"), amount=Decimal(2))
    with pytest.raises(ValueError):
        tp0 + tp1
