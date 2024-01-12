import json

import pytest
from defabipedia import Chain

from defyes.prices.db_functions import TOKEN_MAPPING_FILE
from defyes.prices.prices import get_price

avalanche = {
    "Wrapped AVAX": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",
}

arbitrum = {
    "LUSD": "0x93b346b6BC2548dA6A1E7d98E9a421B42541425b",
}


@pytest.mark.parametrize(
    "token, block, blockchain, expected_price",
    [
        (avalanche["Wrapped AVAX"], 39455385, Chain.AVALANCHE, 47.38),
        (arbitrum["LUSD"], 163257334, Chain.ARBITRUM, 0.99),
    ],
)
def test_price(token, block, blockchain, expected_price):
    price, provider, _ = get_price(token, block, blockchain)
    assert price == pytest.approx(expected_price, abs=0.01)


def test_get_price():
    price = get_price("0x1f9840a85d5af5bf1d1762f925bdaddc4201f984", 17628203, Chain.ETHEREUM, source="coingecko")
    assert price == (5.426491078544339, "coingecko", "ethereum")


def test_token_mapping_valid_json():
    with open(TOKEN_MAPPING_FILE) as f:
        json.load(f)
