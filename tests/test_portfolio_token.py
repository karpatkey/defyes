from defyes.portfolio import Chain, DeployedToken, Token


def test_get_or_create():
    sDAI = Token.objs.get(chain=Chain.ETHEREUM, symbol="sDAI")
    sDAI2 = DeployedToken.objs.get_or_create(
        **{"chain": "ethereum", "symbol": "sDAI", "address": "0x83F20F44975D03b1b09e64809B757c47f942BEeA"}
    )
    assert sDAI is sDAI2
