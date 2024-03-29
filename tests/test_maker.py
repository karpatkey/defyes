from decimal import Decimal

from defabipedia import Chain
from defabipedia.tokens import EthereumTokenAddr
from karpatkit.node import get_node

from defyes import Maker

TEST_BLOCK = 17070386
# TEST_WALLET = '0xf929122994e177079c924631ba13fb280f5cd1f9'
# TEST_WALLET = '0x849D52316331967b6fF1198e5E32A0eB168D039d'
TEST_WALLET = "0x4971DD016127F390a3EF6b956Ff944d0E2e1e462"
VAULT_ID = 27353


def test_get_vault_data():
    x = Maker.get_vault_data(VAULT_ID, TEST_BLOCK)
    assert x == {
        "mat": Decimal("1.6"),
        "gem": EthereumTokenAddr.wstETH,
        "dai": EthereumTokenAddr.DAI,
        "ink": Decimal("57328.918780519001386926"),
        "art": Decimal("21811755.174275192209603126"),
        "Art": Decimal("131281671.560444627089962248"),
        "rate": Decimal("1.033782392295892171018325313"),
        "spot": Decimal("1456.9286150664385"),
        "line": Decimal("154522941.8359970071858062359"),
        "dust": Decimal("7500"),
    }


def test_underlying():
    x = Maker.underlying(VAULT_ID, TEST_BLOCK)
    assert x == [
        [EthereumTokenAddr.wstETH, Decimal("57328.918780519001386926")],
        [EthereumTokenAddr.DAI, Decimal("-22548608.44423451266093976218")],
    ]


def test_get_delegated_MKR():
    WEB3 = get_node(blockchain=Chain.ETHEREUM)
    x = Maker.get_delegated_MKR(TEST_WALLET, TEST_BLOCK, WEB3, decimals=False)
    assert x == [[EthereumTokenAddr.MKR, Decimal("583805204609736124092")]]


def test_protocol_data():
    wallet = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
    block = 17082971
    x = Maker.get_protocol_data(Chain.ETHEREUM, wallet, block)
    assert x == {
        "protocol": "Maker",
        "blockchain": "ethereum",
        "wallet": "0x849D52316331967b6fF1198e5E32A0eB168D039d",
        "block_id": 17082971,
        "positions_key": None,
        "positions": {
            "vaults": {
                27353: {
                    "liquidity": {
                        "underlyings": [
                            {
                                "address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
                                "balance": Decimal("57328.918780519001386926"),
                            },
                            {
                                "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                                "balance": Decimal("-22549744.64918634175568916183"),
                            },
                        ]
                    }
                },
                29954: {
                    "liquidity": {
                        "underlyings": [
                            {"address": "0x6810e776880C02933D47DB1b9fc05908e5386b96", "balance": Decimal("411500")},
                            {
                                "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                                "balance": Decimal("-3020631.639075140899415588649"),
                            },
                        ]
                    }
                },
            },
            "mananger": {
                "liquidity": {"underlyings": [{"address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "balance": 0}]}
            },
            "pot": {
                "liquidity": {"underlyings": [{"address": "0x6B175474E89094C44Da98b954EedeAC495271d0F", "balance": 0}]}
            },
        },
        "version": 0,
    }
