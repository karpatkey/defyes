from decimal import Decimal
from unittest.mock import patch

from defyes import Votium

WALLET = "0x849d52316331967b6ff1198e5e32a0eb168d039d"


# Check if the output is a bool.
def test_check_claimed_or_unclaimed():
    index_number = 1404
    x = Votium.check_claimed_or_unclaimed(WALLET, index_number)
    assert isinstance(x, bool)


# Check output
def test_get_rewards_per_token():
    token_symbol = "LDO"
    decimals = 18
    round_number = "0013"
    x = Votium.get_rewards_per_token(WALLET, token_symbol, decimals, round_number)
    if Votium.check_claimed_or_unclaimed(WALLET, 1675):
        assert x == Decimal(0)
    else:
        assert round(x) == round(Decimal(439.959742214996885504))


# Check output
def test_get_all_rewards():
    with patch("defyes.Votium.get_rewards_per_token") as mock_inner:
        a = [None] * 44
        a[4] = 439.9597422149969
        a[17] = 14.214765596330048
        mock_inner.side_effect = a

        # Call the outer function
        output = Votium.get_all_rewards(WALLET)

        # Assertion to check the output
        assert output == {
            "protocol": "Votium",
            "block": "latest",
            "positions": [
                {
                    "position ID": "rewards",
                    "balances": [
                        {
                            "token": "0x5a98fcbea516cf06857215779fd812ca3bef1b32",
                            "balance": Decimal("439.95974221499687928371713496744632720947265625"),
                        },
                        {
                            "token": "0x03ab458634910aad20ef5f1c8ee96f1d6ac54919",
                            "balance": Decimal("14.2147655963300483250577599392272531986236572265625"),
                        },
                    ],
                }
            ],
        }
