from unittest.mock import Mock
from decimal import Decimal

from defi_protocols import HiddenHand
from defi_protocols.constants import ETHEREUM

WALLET_N1 = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

# use data of 17-05-2023
api_result = [
    {
        'chainId': 1,
        'claimMetadata': {
            'account': '0x849d52316331967b6ff1198e5e32a0eb168d039d',
            'amount': '1882870279673552604832',
            'identifier': '0x329ffd9b41345bc4959db47e686a0416d414457adeaa66a22d5c5d79d6830e1b',
            'merkleProof': ['xxx'],
        },
        'claimable': '56.771231052533362388',
        'decimals': 18,
        'name': 'Rocket Pool',
        'protocol': 'aura',
        'symbol': 'rpl',
        'token': '0xd33526068d116ce69f19a9ee46f0bd304f21a51f',
        'value': Decimal('2835.7229910740416'),
    },
    {
        'chainId': 1,
        'claimMetadata': {
            'account': '0x849d52316331967b6ff1198e5e32a0eb168d039d',
            'amount': '84806609263212397089872',
            'identifier': '0x8eee07e6aecfd58a059e9c795e092747309d76151e2ab9562faf60b2d64673fd',
            'merkleProof': ['xxx'],
        },
        'claimable': '1493.272693434831511272',
        'decimals': 18,
        'name': 'Aura Finance',
        'protocol': 'aura',
        'symbol': 'aura',
        'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
        'value': Decimal('2867.0835713948763'),
    },
    {
        'chainId': 1,
        'claimMetadata': {
            'account': '0x849d52316331967b6ff1198e5e32a0eb168d039d',
            'amount': '126688248498',
            'identifier': '0x3f5a22cb83118980ed5887bc9ed2b8405706479ce22435bdf0b199c2192702ac',
            'merkleProof': ['xxx'],
        },
        'claimable': '3269.873946',
        'decimals': 6,
        'name': 'USD Coin',
        'protocol': 'aura',
        'symbol': 'usdc',
        'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
        'value': Decimal('269.873946'),
    },
]

end_result = {'protocol': 'HiddenHand',
              'block': 'latest',
              'positions': [{'position ID': 'aura',
                             'balances':[{'token': '0xd33526068d116ce69f19a9ee46f0bd304f21a51f',
                                          'balance': Decimal('56.771231052533362388')},
                                         {'token': '0xc0c293ce456ff0ed870add98a0828dd4d2903dbf',
                                          'balance': Decimal('1493.272693434831511272')},
                                         {'token': '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48',
                                          'balance': Decimal('3269.873946')}
                                         ]}
                            ]}

api_json_result = '{"error": false, "data": [{"decimals": 18, "claimable": "56.771231052533362388", "value": 2835.7229910740416}]}'


def test_underlying_all(monkeypatch):
    monkeypatch.setattr(HiddenHand, "get_api_results", Mock(return_value=api_result))
    data = HiddenHand.underlying_all(WALLET_N1,ETHEREUM)
    assert data == end_result


def test_get_api_result(requests_mock):
    requests_mock.get(f"https://api.hiddenhand.finance/reward/1/{WALLET_N1}", text=api_json_result)
    api_results = HiddenHand.get_api_results(
        wallet=WALLET_N1,
        blockchain=ETHEREUM,
     )
    assert api_results == [
        {'decimals': 18, 'claimable': '56.771231052533362388', 'value': Decimal('2835.7229910740416')},
    ]
    assert isinstance(api_results[0]['value'], Decimal)
