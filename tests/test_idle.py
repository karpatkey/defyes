from decimal import Decimal

from defyes import Idle
from defyes.constants import Chain, ETHTokenAddr

TEST_WALLET = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
TEST_WALLET2 = "0x542256Ef33279C5545AA71f4b3B6298990f30Ffc"
TEST_BLOCK = 18073189


def test_get_all_rewards():
    gauge = "0x675eC042325535F6e176638Dd2d4994F645502B9"
    rewards = Idle.get_all_rewards(TEST_WALLET2, gauge, TEST_BLOCK, Chain.ETHEREUM)
    assert rewards == [
        [ETHTokenAddr.IDLE, Decimal("11.966264216568462645")],
        [ETHTokenAddr.LDO, Decimal("36.724756125561987935")],
    ]


def test_get_balances():
    amounts = Idle.get_balances(
        tranche={"AATrancheToken": "0xdf17c739b666B259DA3416d01f0310a6e429f592", "AAGauge": None},
        cdo_address="0x8E0A8A5c1e5B3ac0670Ea5a613bB15724D51Fc37",
        underlying_token=ETHTokenAddr.stETH,
        wallet=TEST_WALLET,
        block=TEST_BLOCK,
        blockchain=Chain.ETHEREUM,
    )
    assert amounts == {
        "0xdf17c739b666B259DA3416d01f0310a6e429f592": {
            "holdings": [
                {"address": "0xdf17c739b666B259DA3416d01f0310a6e429f592", "balance": Decimal("895.399109134177361276")}
            ],
            "underlying": [
                {
                    "address": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                    "balance": Decimal("901.3654400065544057400061691"),
                }
            ],
        }
    }


def test_underlying():
    underlying = Idle.underlying(
        wallet=TEST_WALLET2,
        tranche_address="0x2688FC68c4eac90d9E5e1B94776cF14eADe8D877",
        block=TEST_BLOCK,
        blockchain=Chain.ETHEREUM,
        reward=True,
    )

    assert underlying == {
        "blockchain": "ethereum",
        "block": 18073189,
        "protocol": "Idle",
        "positions_key": "tranche_token",
        "decimals": True,
        "version": 0,
        "wallet": "0x542256Ef33279C5545AA71f4b3B6298990f30Ffc",
        "positions": {
            "0x2688FC68c4eac90d9E5e1B94776cF14eADe8D877": {
                "holdings": [
                    {"address": "0x2688FC68c4eac90d9E5e1B94776cF14eADe8D877", "balance": Decimal("0")},
                    {
                        "address": "0x675eC042325535F6e176638Dd2d4994F645502B9",
                        "balance": Decimal("6.02414999652349193"),
                    },
                ],
                "underlying": [
                    {
                        "address": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                        "balance": Decimal("6.311082708276993882703532594"),
                    }
                ],
                "rewards": [
                    {
                        "address": "0x875773784Af8135eA0ef43b5a374AaD105c5D39e",
                        "balance": Decimal("11.966264216568462645"),
                    },
                    {
                        "address": "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",
                        "balance": Decimal("36.724756125561987935"),
                    },
                ],
            }
        },
    }


# def test_underlying_all():
#     wallet = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
#     underlying = Idle.underlying_all(wallet, 17295010, ETHEREUM, rewards=True)
#     assert underlying == [
#         [
#             [ETHTokenAddr.STETH, Decimal("931.756327134769968317289982")],
#             [[ETHTokenAddr.IDLE, Decimal("0")], [ETHTokenAddr.LDO, Decimal("31065.052700304643473107")]],
#         ]
#     ]


def test_get_addresses_subgraph():
    addresses = Idle.get_addresses_subgraph(TEST_BLOCK, Chain.ETHEREUM)
    assert addresses == {
        "cdos": [
            {
                "CDO": "0x008C589c471fd0a13ac2B9338B69f5F7a1A843e1",
                "underlyingToken": "0x43b4FdFD4Ff969587185cDB6f0BD875c5Fc83f8c",
                "AATranche": {
                    "AATrancheToken": "0x790E38D85a364DD03F682f5EcdC88f8FF7299908",
                    "AAGauge": "0x21dDA17dFF89eF635964cd3910d167d562112f57",
                },
                "BBTranche": {"BBTrancheToken": "0xa0E8C9088afb3Fa0F40eCDf8B551071C34AA1aa4", "BBGauge": None},
            },
            {
                "CDO": "0x1329E8DB9Ed7a44726572D44729427F132Fa290D",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x9CAcd44cfDf22731bc99FaCf3531C809d56BD4A2", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xf85Fd280B301c0A6232d515001dA8B6c8503D714", "BBGauge": None},
            },
            {
                "CDO": "0x151e89e117728AC6c93aae94C621358B0EBD1866",
                "underlyingToken": "0x5a6A4D54456819380173272A5E8E9B9904BdF41B",
                "AATranche": {
                    "AATrancheToken": "0xFC96989b3Df087C96C806318436B16e44c697102",
                    "AAGauge": "0x8cC001dd6C9f8370dB99c1e098e13215377Ecb95",
                },
                "BBTranche": {"BBTrancheToken": "0x5346217536852CD30A5266647ccBB6f73449Cbd1", "BBGauge": None},
            },
            {
                "CDO": "0x16d88C635e1B439D8678e7BAc689ac60376fBfA6",
                "underlyingToken": "0x1AEf73d49Dedc4b1778d0706583995958Dc862e6",
                "AATranche": {
                    "AATrancheToken": "0x4585F56B06D098D4EDBFc5e438b8897105991c6A",
                    "AAGauge": "0xAbd5e3888ffB552946Fc61cF4C816A73feAee42E",
                },
                "BBTranche": {"BBTrancheToken": "0xFb08404617B6afab0b19f6cEb2Ef9E07058D043C", "BBGauge": None},
            },
            {
                "CDO": "0x1f5A97fB665e295303D2F7215bA2160cc5313c8E",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x868bb78fb045576162B510ba33358C9f93e7959e", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x6EdE2522347E6a5A0420F41f42e021246e97B540", "BBGauge": None},
            },
            {
                "CDO": "0x2398Bc075fa62Ee88d7fAb6A18Cd30bFf869bDa4",
                "underlyingToken": "0x1a7e4e63778B4f12a199C062f3eFdD288afCBce8",
                "AATranche": {
                    "AATrancheToken": "0x624DfE05202b66d871B8b7C0e14AB29fc3a5120c",
                    "AAGauge": "0x8f195979F7aF6C500b4688E492d07036c730c1B2",
                },
                "BBTranche": {"BBTrancheToken": "0xcf5FD05F72cA777d71FB3e38F296AAD7cE735cB7", "BBGauge": None},
            },
            {
                "CDO": "0x264E1552Ee99f57a7D9E1bD1130a478266870C39",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {"AATrancheToken": "0x62Eb6a8c7A555eae3e0B17D42CA9A3299af2787E", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x56263BDE26b72b3e3D26d8e03399a275Aa8Bbfb2", "BBGauge": None},
            },
            {
                "CDO": "0x34dCd573C5dE4672C8248cd12A99f875Ca112Ad8",
                "underlyingToken": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                "AATranche": {
                    "AATrancheToken": "0x2688FC68c4eac90d9E5e1B94776cF14eADe8D877",
                    "AAGauge": "0x675eC042325535F6e176638Dd2d4994F645502B9",
                },
                "BBTranche": {"BBTrancheToken": "0x3a52fa30c33cAF05fAeE0f9c5Dfe5fd5fe8B3978", "BBGauge": None},
            },
            {
                "CDO": "0x440ceAd9C0A0f4ddA1C81b892BeDc9284Fc190dd",
                "underlyingToken": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "AATranche": {"AATrancheToken": "0x745e005a5dF03bDE0e55be811350acD6316894E1", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xF0C177229Ae1cd41BF48dF6241fae3e6A14A6967", "BBGauge": None},
            },
            {
                "CDO": "0x46c1f702A6aAD1Fd810216A5fF15aaB1C62ca826",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {
                    "AATrancheToken": "0x852c4d2823E98930388b5cE1ed106310b942bD5a",
                    "AAGauge": "0x57d59d4bBb0E2432f1698F33D4A47B3C7a9754f3",
                },
                "BBTranche": {"BBTrancheToken": "0x6629baA8C7c6a84290Bf9a885825E3540875219D", "BBGauge": None},
            },
            {
                "CDO": "0x4bC5E595d2e0536Ea989a7a9741e9EB5c3CAea33",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x5f45A578491A23AC5AEE218e2D405347a0FaFa8E", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x982E46e81E99fbBa3Fb8Af031A7ee8dF9041bb0C", "BBGauge": None},
            },
            {
                "CDO": "0x4CCaf1392a17203eDAb55a1F2aF3079A8Ac513E7",
                "underlyingToken": "0xd632f22692FaC7611d2AA1C0D552930D43CAEd3B",
                "AATranche": {
                    "AATrancheToken": "0x15794DA4DCF34E674C18BbFAF4a67FF6189690F5",
                    "AAGauge": "0x7ca919Cf060D95B3A51178d9B1BCb1F324c8b693",
                },
                "BBTranche": {"BBTrancheToken": "0x18cf59480d8c16856701F66028444546B7041307", "BBGauge": None},
            },
            {
                "CDO": "0x5dcA0B3Ed7594A6613c1A2acd367d56E1f74F92D",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {"AATrancheToken": "0x43eD68703006add5F99ce36b5182392362369C1c", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x38D36353D07CfB92650822D9c31fB4AdA1c73D6E", "BBGauge": None},
            },
            {
                "CDO": "0x70320A388c6755Fc826bE0EF9f98bcb6bCCc6FeA",
                "underlyingToken": "0xe2f2a5C287993345a840Db3B0845fbC70f5935a5",
                "AATranche": {
                    "AATrancheToken": "0xfC558914b53BE1DfAd084fA5Da7f281F798227E7",
                    "AAGauge": "0x41653c7AF834F895Db778B1A31EF4F68Be48c37c",
                },
                "BBTranche": {"BBTrancheToken": "0x91fb938FEa02DFd5303ACeF5a8A2c0CaB62b94C7", "BBGauge": None},
            },
            {
                "CDO": "0x77648A2661687ef3B05214d824503F6717311596",
                "underlyingToken": "0x956F47F50A910163D8BF957Cf5846D573E7f87CA",
                "AATranche": {"AATrancheToken": "0x9cE3a740Df498646939BcBb213A66BBFa1440af6", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x2490D810BF6429264397Ba721A488b0C439aA745", "BBGauge": None},
            },
            {
                "CDO": "0x7EcFC031758190eb1cb303D8238D553b1D4Bc8ef",
                "underlyingToken": "0x06325440D014e39736583c165C2963BA99fAf14E",
                "AATranche": {
                    "AATrancheToken": "0x060a53BCfdc0452F35eBd2196c6914e0152379A6",
                    "AAGauge": "0x30a047d720f735Ad27ad384Ec77C36A4084dF63E",
                },
                "BBTranche": {"BBTrancheToken": "0xd83246d2bCBC00e85E248A6e9AA35D0A1548968E", "BBGauge": None},
            },
            {
                "CDO": "0x858F5A3a5C767F8965cF7b77C51FD178C4A92F05",
                "underlyingToken": "0xb9446c4Ef5EBE66268dA6700D26f96273DE3d571",
                "AATranche": {
                    "AATrancheToken": "0x158e04225777BBEa34D2762b5Df9eBD695C158D2",
                    "AAGauge": "0xDfB27F2fd160166dbeb57AEB022B9EB85EA4611C",
                },
                "BBTranche": {"BBTrancheToken": "0x3061C652b49Ae901BBeCF622624cc9f633d01bbd", "BBGauge": None},
            },
            {
                "CDO": "0x860B1d25903DbDFFEC579d30012dA268aEB0d621",
                "underlyingToken": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "AATranche": {"AATrancheToken": "0x6796FCd41e4fb26855Bb9BDD7Cad41128Da1Fd59", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x00B80FCCA0fE4fDc3940295AA213738435B0f94e", "BBGauge": None},
            },
            {
                "CDO": "0x8E0A8A5c1e5B3ac0670Ea5a613bB15724D51Fc37",
                "underlyingToken": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                "AATranche": {"AATrancheToken": "0xdf17c739b666B259DA3416d01f0310a6e429f592", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x990b3aF34dDB502715E1070CE6778d8eB3c8Ea82", "BBGauge": None},
            },
            {
                "CDO": "0x9C13Ff045C0a994AF765585970A5818E1dB580F8",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x376B2dCF9eBd3067BB89eb6D1020FbE604092212", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x86a40De6d77331788Ba24a85221fb8DBFcBC9bF0", "BBGauge": None},
            },
            {
                "CDO": "0xb3F717a5064D2CBE1b8999Fdfd3F8f3DA98339a6",
                "underlyingToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "AATranche": {"AATrancheToken": "0x6c0c8708e2FD507B7057762739cb04cF01b98d7b", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xd69c52E6AF3aE708EE4b3d3e7C0C5b4CF4d6244B", "BBGauge": None},
            },
            {
                "CDO": "0xc4574C60a455655864aB80fa7638561A756C5E61",
                "underlyingToken": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "AATranche": {"AATrancheToken": "0x0a6f2449C09769950cFb76f905Ad11c341541f70", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x3Eb6318b8D9f362a0e1D99F6032eDB1C4c602500", "BBGauge": None},
            },
            {
                "CDO": "0xc8c64CC8c15D9aa1F4dD40933f3eF742A7c62478",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {"AATrancheToken": "0xd54E5C263298E60A5030Ce2C8ACa7981EaAaED4A", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xD3E4C5C37Ba3185410550B836557B8FA51d5EA3b", "BBGauge": None},
            },
            {
                "CDO": "0xd0DbcD556cA22d3f3c142e9a3220053FD7a247BC",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {"AATrancheToken": "0xE9ada97bDB86d827ecbaACCa63eBcD8201D8b12E", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x730348a54bA58F64295154F0662A08Cbde1225c2", "BBGauge": None},
            },
            {
                "CDO": "0xd12f9248dEb1D972AA16022B399ee1662d51aD22",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x00b51Fc6384A120Eac68bEA38b889Ea92524ab93", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xe6De3A77B4e71356F4E5e52fd695EAD5E5DBcd27", "BBGauge": None},
            },
            {
                "CDO": "0xD5469DF8CA36E7EaeDB35D428F28E13380eC8ede",
                "underlyingToken": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                "AATranche": {
                    "AATrancheToken": "0xE0f126236d2a5b13f26e72cBb1D1ff5f297dDa07",
                    "AAGauge": "0x0C3310B0B57b86d376040B755f94a925F39c4320",
                },
                "BBTranche": {"BBTrancheToken": "0xb1EC065abF6783BCCe003B8d6B9f947129504854", "BBGauge": None},
            },
            {
                "CDO": "0xDB82dDcb7e2E4ac3d13eBD1516CBfDb7b7CE0ffc",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {"AATrancheToken": "0x69d87d0056256e3df7Be9b4c8D6429B4b8207C5E", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xB098AF638aF0c4Fa3edb1A24f807E9c22dA0fE73", "BBGauge": None},
            },
            {
                "CDO": "0xDBCEE5AE2E9DAf0F5d93473e08780C9f45DfEb93",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0xb86264c21418aA75F7c337B1821CcB4Ff4d57673", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x4D9d9AA17c3fcEA05F20a87fc1991A045561167d", "BBGauge": None},
            },
            {
                "CDO": "0xDBd47989647Aa73f4A88B51f2B5Ff4054De1276a",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0xa0154A44C1C45bD007743FA622fd0Da4f6d67D57", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x7a625a2882C9Fc8DF1463d5E538a3F39B5DBD073", "BBGauge": None},
            },
            {
                "CDO": "0xDcE26B2c78609b983cF91cCcD43E238353653b0E",
                "underlyingToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                "AATranche": {"AATrancheToken": "0x1692F6574a6758ADfbD12544e209146dD4510BD7", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xCb980b5A4f5BdB81d0B4b97A9eDe64578ba9D48A", "BBGauge": None},
            },
            {
                "CDO": "0xe4CECD8e7Cc1F8a45F0e7Def15466bE3D8031841",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0xB8110bCAC56472E687885aD4f39035fa026E171E", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x668a006E8A1043Eaec5117996644f0c393D188e6", "BBGauge": None},
            },
            {
                "CDO": "0xE7C6A4525492395d65e736C3593aC933F33ee46e",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0xdcA1daE87f5c733c84e0593984967ed756579BeE", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xbcC845bB731632eBE8Ac0BfAcdE056170aaaaa06", "BBGauge": None},
            },
            {
                "CDO": "0xec964d06cD71a68531fC9D083a142C48441F391C",
                "underlyingToken": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                "AATranche": {"AATrancheToken": "0x2B7Da260F101Fb259710c0a4f2EfEf59f41C0810", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x2e80225f383F858E8737199D3496c5Cf827670a5", "BBGauge": None},
            },
            {
                "CDO": "0xf324Dca1Dc621FCF118690a9c6baE40fbD8f09b7",
                "underlyingToken": "0xC9467E453620f16b57a34a770C6bceBECe002587",
                "AATranche": {
                    "AATrancheToken": "0x4657B96D587c4d46666C244B40216BEeEA437D0d",
                    "AAGauge": "0x2bEa05307b42707Be6cCE7a16d700a06fF93a29d",
                },
                "BBTranche": {"BBTrancheToken": "0x3872418402d1e967889aC609731fc9E11f438De5", "BBGauge": None},
            },
            {
                "CDO": "0xf52834404A51f5af1CDbeEdaA95B60c8B2187ba0",
                "underlyingToken": "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84",
                "AATranche": {"AATrancheToken": "0xbb26dD53dD37f2dC4b91E93C947d6b8683b85279", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0xC136E01f74FB0DAEfA29f0AAc9c250EF069e684d", "BBGauge": None},
            },
            {
                "CDO": "0xF5a3d259bFE7288284Bd41823eC5C8327a314054",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {
                    "AATrancheToken": "0x1e095cbF663491f15cC1bDb5919E701b27dDE90C",
                    "AAGauge": "0x1CD24F833Af78ae877f90569eaec3174d6769995",
                },
                "BBTranche": {"BBTrancheToken": "0xe11679CDb4587FeE907d69e9eC4a7d3F0c2bcf3B", "BBGauge": None},
            },
            {
                "CDO": "0xf615a552c000B114DdAa09636BBF4205De49333c",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x1AF0294524093BFdF5DA5135853dC2fC678C12f7", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x271db794317B44827EfE81DeC6193fFc277050F6", "BBGauge": None},
            },
            {
                "CDO": "0xf6B692CC9A5421E4C66D32511d65F94c64fbD043",
                "underlyingToken": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                "AATranche": {"AATrancheToken": "0x3e041C9980Bc03011cc30491d0c4ccD53602F89B", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x65237B6Fc6E62B05B62f1EbE53eDAadcCd1684Ad", "BBGauge": None},
            },
            {
                "CDO": "0xF87ec7e1Ee467d7d78862089B92dd40497cBa5B8",
                "underlyingToken": "0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",
                "AATranche": {"AATrancheToken": "0xAEf4FCC4E5F2dc270760063446d4116D24704Ad1", "AAGauge": None},
                "BBTranche": {"BBTrancheToken": "0x077212c69A66261CF7bD1fd3b5C5db7CfFA948Ee", "BBGauge": None},
            },
        ]
    }


def test_get_gauges():
    gauges = Idle.get_gauges(TEST_BLOCK, Chain.ETHEREUM)
    assert gauges == [
        ["0x21dDA17dFF89eF635964cd3910d167d562112f57", "0x790E38D85a364DD03F682f5EcdC88f8FF7299908"],
        ["0x675eC042325535F6e176638Dd2d4994F645502B9", "0x2688FC68c4eac90d9E5e1B94776cF14eADe8D877"],
        ["0x7ca919Cf060D95B3A51178d9B1BCb1F324c8b693", "0x15794DA4DCF34E674C18BbFAF4a67FF6189690F5"],
        ["0x8cC001dd6C9f8370dB99c1e098e13215377Ecb95", "0xFC96989b3Df087C96C806318436B16e44c697102"],
        ["0xDfB27F2fd160166dbeb57AEB022B9EB85EA4611C", "0x158e04225777BBEa34D2762b5Df9eBD695C158D2"],
        ["0x30a047d720f735Ad27ad384Ec77C36A4084dF63E", "0x060a53BCfdc0452F35eBd2196c6914e0152379A6"],
        ["0xAbd5e3888ffB552946Fc61cF4C816A73feAee42E", "0x4585F56B06D098D4EDBFc5e438b8897105991c6A"],
        ["0x41653c7AF834F895Db778B1A31EF4F68Be48c37c", "0xfC558914b53BE1DfAd084fA5Da7f281F798227E7"],
        ["0x2bEa05307b42707Be6cCE7a16d700a06fF93a29d", "0x4657B96D587c4d46666C244B40216BEeEA437D0d"],
        ["0x8f195979F7aF6C500b4688E492d07036c730c1B2", "0x624DfE05202b66d871B8b7C0e14AB29fc3a5120c"],
        ["0x1CD24F833Af78ae877f90569eaec3174d6769995", "0x1e095cbF663491f15cC1bDb5919E701b27dDE90C"],
        ["0x57d59d4bBb0E2432f1698F33D4A47B3C7a9754f3", "0x852c4d2823E98930388b5cE1ed106310b942bD5a"],
        ["0x0C3310B0B57b86d376040B755f94a925F39c4320", "0xE0f126236d2a5b13f26e72cBb1D1ff5f297dDa07"],
    ]
