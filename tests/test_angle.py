from decimal import Decimal

from defi_protocols import Angle
from defi_protocols.Angle import Asset
from defi_protocols.constants import ETHEREUM

agEUR = "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8"
WALLET = "0x849D52316331967b6fF1198e5E32A0eB168D039d"


def test_angle_treasury():
    block = 17451062

    t = Angle.Treasury(ETHEREUM)
    assert t.stable_token == agEUR
    assert ['0x241D7598BD1eb819c0E9dEd456AcB24acA623679',
            '0x1beCE8193f8Dc2b170135Da9F1fA8b81C7aD18b1',
            '0x73aaf8694BA137a7537E7EF544fcf5E2475f227B',
            '0x8E2277929B2D849c0c344043D9B9507982e6aDd0',
            '0xdEeE8e8a89338241fe622509414Ff535fB02B479',
            '0x0652B4b3D205300f9848f0431296D67cA4397f3b',
            '0xE1C084e6E2eC9D32ec098e102a73C4C27Eb9Ee58',
            '0x0B3AF9fb0DE42AE70432ABc5aaEaB8F9774bf87b',
            '0x989ed2DDCD4D2DC237CE014432aEb40EfE738E31',
            '0x29e9D3D8e295E23B1B39DCD3D8D595761E032306',
            '0xe0C8B6c4ea301C8A221E8838ca5B80Ac76E7A10b',
            '0x913E8e1eD659C27613E937a6B6119b91D985094c',
            '0x96de5c30F2BF4683c7903F3e921F720602F8868A'] == t.get_all_vault_managers_addrs(block)


def test_underlying():
    block = 17451062
    underlying = Angle.underlying(ETHEREUM, WALLET, block)
    assert underlying == {'equivalent_amount': Decimal('431692.91115667917318028225'),
                          'equivalent_uint': 'EUR',
                          'positions': [
                              {'debt': Asset('ethereum',
                                             '0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8',
                                             Decimal('235029.284458768826450263')),
                               'available_to_borrow': Asset('ethereum',
                                                            '0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8',
                                                            Decimal('431692.91115667917318028225')),
                               'collateral_deposit': Asset('ethereum',
                                                           '0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0',
                                                           Decimal('475')),
                               'health_factor': Decimal('2.836762223698175089305445941'),
                               'loan_to_value': Decimal('0.2714362146983829164458752415'),
                               'anual_interest_rate': Decimal('0.004987542475021200498864000'),
                               'liquidation_price_in_stablecoin_fiat': Decimal('642.5954462304000723178755981')}
                              ]
                          }