from decimal import Decimal

from web3 import Web3

from defyes import Balancer
from defyes.constants import Chain, ETHTokenAddr, GnosisTokenAddr
from defyes.functions import date_to_block

WALLET_N1 = "0x31cD267D34EC6368eac930Be4f412dfAcc71A844"
WALLET_N2 = "0x4b0429F3db75dbA6B82c32a200C9C298ffC05839"
WALLET_N3 = "0xe8fAF95AD24A467ddDc4e100a68398B31D3dCdd6"
WALLET_N4 = "0x64aE36eeaC5BF9c1F4b7Cc6F0Fa32bBa19aaF9Bc"
WALLET_N5 = "0xce88686553686DA562CE7Cea497CE749DA109f9F"
WALLET_N6 = "0x43b650399F2E4D6f03503f44042fabA8F7D73470"
WALLET_39d = "0x849D52316331967b6fF1198e5E32A0eB168D039d"
B60WETH40DAI_ADDR = "0x0b09deA16768f0799065C475bE02919503cB2a35"
B50USDC50WETH_ADDR = "0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8"
B80BAL20WETH_ADDR = "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56"
BstETHSTABLE_ADDR = "0x32296969Ef14EB0c6d29669C550D4a0449130230"
B50wstETH50LDO_ADDR = "0x5f1f4e50ba51d723f12385a8a9606afc3a0555f5"
bbaUSD_ADDR = "0xA13a9247ea42D743238089903570127DdA72fE44"
bbaUSDT_ADDR = "0x2f4eb100552ef93840d5adc30560e5513dfffacb"
bbaUSDC_ADDR = "0x82698aecc9e28e9bb27608bd52cf57f704bd1b83"
bbaDAI_ADDR = "0xae37d54ae477268b9997d4161b96b8200755935c"
bbaUSDV3_ADDR = "0xfeBb0bbf162E64fb9D0dfe186E517d84C395f016"

# Gnosis Chain
WALLET_e6f = "0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f"
bb_ag_USD_ADDR = "0xfedb19ec000d38d92af4b21436870f115db22725"
B50bbagGNO50bbagUSD_ADDR = "0xB973Ca96a3f0D61045f53255E319AEDb6ED49240"
bb_ag_WXDAI_ADDR = "0x41211bba6d37f5a74b22e667533f080c7c7f3f13"
bb_ag_GNO_ADDR = "0xffff76a3280e95dc855696111c2562da09db2ac0"


def test_liquidity_pool():
    block = 16950590

    lp = Balancer.LiquidityPool(Chain.ETHEREUM, block, B60WETH40DAI_ADDR)
    assert (
        lp.poolid
        == b"\x0b\t\xde\xa1gh\xf0y\x90e\xc4u\xbe\x02\x91\x95\x03\xcb*5\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1a"
    )
    assert lp.decimals == 18
    assert lp.supply == 12835022143788475405205
    assert lp.bpt_index is None
    assert lp.scaling_factors is None

    lp = Balancer.LiquidityPool(Chain.ETHEREUM, block, bbaUSD_ADDR)
    assert (
        lp.poolid == b"\xa1:\x92G\xeaB\xd7C#\x80\x89\x905p\x12}\xdar\xfeD\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03]"
    )
    assert lp.decimals == 18
    assert lp.supply == 45626173875220118192194148
    assert lp.bpt_index == 2
    assert lp.scaling_factors == [
        1008896757769783573,
        1003250365192438010,
        1000000000000000000,
        1002548558018035032,
    ]


def test_gauge_address():
    block = 16978206
    assert Balancer.get_gauge_addresses(Chain.ETHEREUM, block, B60WETH40DAI_ADDR) == [
        "0x4ca6AC0509E6381Ca7CD872a6cdC0Fbf00600Fa1"
    ]


def test_pool_balances():
    block = 16978206
    balances = Balancer.pool_balances(Chain.ETHEREUM, B50USDC50WETH_ADDR, block)
    assert balances == {
        ETHTokenAddr.USDC: Decimal("1129072.214823"),
        ETHTokenAddr.WETH: Decimal("601.535954342344676691"),
    }

    block = 17117344
    balances = Balancer.pool_balances(Chain.ETHEREUM, bbaUSD_ADDR, block)
    assert balances == {
        ETHTokenAddr.USDT: Decimal("11390997.35159545717004295106"),
        ETHTokenAddr.USDC: Decimal("13348617.10444504902242681224"),
        ETHTokenAddr.DAI: Decimal("13011285.62447645590205757650"),
    }

    usdt = Balancer.pool_balances(Chain.ETHEREUM, bbaUSDT_ADDR, block)
    assert usdt[ETHTokenAddr.USDT] == Decimal("11014973.47418")

    usdc = Balancer.pool_balances(Chain.ETHEREUM, bbaUSDC_ADDR, block)
    assert usdc[ETHTokenAddr.USDC] == Decimal("13116091.667863")

    dai = Balancer.pool_balances(Chain.ETHEREUM, bbaDAI_ADDR, block)
    assert dai[ETHTokenAddr.DAI] == Decimal("8173013.460308747444345661")

    balances = Balancer.pool_balances(Chain.ETHEREUM, bbaUSDV3_ADDR, block)
    assert balances == {
        ETHTokenAddr.DAI: Decimal("1050266.066617679685909312000"),
        ETHTokenAddr.USDT: Decimal("765001.8540369999844466201230"),
        ETHTokenAddr.USDC: Decimal("908244.4675409999892750711044"),
    }

    block = 29830048
    balances = Balancer.pool_balances(Chain.GNOSIS, bb_ag_WXDAI_ADDR, block)
    assert balances[GnosisTokenAddr.WXDAI] == Decimal("297.671114136700998186")

    balances = Balancer.pool_balances(Chain.GNOSIS, B50bbagGNO50bbagUSD_ADDR, block)
    assert balances == {
        GnosisTokenAddr.WXDAI: Decimal("12.64808842311978470699902288"),
        GnosisTokenAddr.USDT: Decimal("28.70958971431260849138745292"),
        GnosisTokenAddr.USDC: Decimal("12.05344858660931219370764335"),
        GnosisTokenAddr.GNO: Decimal("0.5348319581477661245738463077"),
    }

    gno = Balancer.pool_balances(Chain.GNOSIS, bb_ag_GNO_ADDR, block)
    assert gno[GnosisTokenAddr.GNO] == Decimal("13.253324184854298321")


def test_unwrap():
    block = 16950590
    lptoken_amount = 1
    unwrap = Balancer.unwrap(Chain.ETHEREUM, bbaUSD_ADDR, lptoken_amount, block)
    assert unwrap == {
        ETHTokenAddr.USDT: Decimal("0.2536037704765909166606592597"),
        ETHTokenAddr.USDC: Decimal("0.3691057462360258687781876952"),
        ETHTokenAddr.DAI: Decimal("0.3716984431123257030355323046"),
    }

    lptoken_amount = Decimal("0.0106223377584825466601881061023959773592650890350341796875")
    unwrap = Balancer.unwrap(Chain.ETHEREUM, B60WETH40DAI_ADDR, lptoken_amount, block)
    assert unwrap == {
        ETHTokenAddr.DAI: Decimal("0.3998802387901373103114663897"),
        ETHTokenAddr.WETH: Decimal("0.0003284487726480976462916290608"),
    }

    block = 27628264
    lptoken_amount = 1000
    unwrap = Balancer.unwrap(Chain.GNOSIS, B50bbagGNO50bbagUSD_ADDR, lptoken_amount, block)
    assert unwrap == {
        GnosisTokenAddr.WXDAI: Decimal("2057.534932715631909526303472"),
        GnosisTokenAddr.USDT: Decimal("1154.268905869372659697240476"),
        GnosisTokenAddr.USDC: Decimal("1912.892948230578252436479469"),
        GnosisTokenAddr.GNO: Decimal("48.74728477215118382303378165"),
    }

    block = 17543299
    lptoken_amount = 1
    unwrap = Balancer.unwrap(Chain.ETHEREUM, bbaUSDV3_ADDR, lptoken_amount, block)
    assert unwrap == {
        ETHTokenAddr.DAI: Decimal("0.3830201090764638710935863995"),
        ETHTokenAddr.USDT: Decimal("0.2468271706616370953541602940"),
        ETHTokenAddr.USDC: Decimal("0.3684855328623633958890680139"),
    }


def test_gauge_rewards():
    block = 16978206

    gauge_address = Balancer.get_gauge_addresses(Chain.ETHEREUM, block, B60WETH40DAI_ADDR)[0]
    gauge = Balancer.Gauge(Chain.ETHEREUM, block, gauge_address)
    rewards = gauge.get_rewards(WALLET_N1)
    assert rewards == {ETHTokenAddr.BAL: Decimal("0.000001267800098374")}

    gauge_address = Balancer.get_gauge_addresses(Chain.ETHEREUM, block, BstETHSTABLE_ADDR)[0]
    gauge = Balancer.Gauge(Chain.ETHEREUM, block, gauge_address)
    rewards = gauge.get_rewards(WALLET_N3)
    assert rewards == {ETHTokenAddr.LDO: 0, ETHTokenAddr.BAL: Decimal("0.000090529527458665")}


def test_vebal_rewards():
    block = 16950590

    vebal_rewards = Balancer.get_vebal_rewards(WALLET_N2, Chain.ETHEREUM, block)
    assert vebal_rewards == {
        ETHTokenAddr.BAL: Decimal("0.000019372013715193"),
        ETHTokenAddr.BB_A_USD_OLD: Decimal("0"),
        ETHTokenAddr.BB_A_USD: Decimal("0.000210261212072964"),
        ETHTokenAddr.BB_A_USD_V3: Decimal("0"),
    }


def test_protocol_data():
    block = 16978206
    underlying = Balancer.get_protocol_data_for(Chain.ETHEREUM, WALLET_N1, B60WETH40DAI_ADDR, block, reward=True)
    assert {
        "protocol": "Balancer",
        "blockchain": "ethereum",
        "block_id": 16978206,
        "wallet": WALLET_N1,
        "positions": {
            "0x0b09deA16768f0799065C475bE02919503cB2a35": {
                "staked": {
                    "staked_key": "gauge_address",
                    "0x4ca6AC0509E6381Ca7CD872a6cdC0Fbf00600Fa1": {
                        "holdings": [
                            {
                                "address": "0x0b09deA16768f0799065C475bE02919503cB2a35",
                                "balance": Decimal("0.010622337758482546"),
                            }
                        ],
                        "underlyings": [
                            {
                                "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                                "balance": Decimal("0.4064524767585684232500351728"),
                            },
                            {
                                "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                                "balance": Decimal("0.0003249882874596042694139236462"),
                            },
                        ],
                        "unclaimed_rewards": [
                            {
                                "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                                "balance": Decimal("0.000001267800098374"),
                            }
                        ],
                    },
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    underlying = Balancer.get_protocol_data_for(
        Chain.ETHEREUM, WALLET_N2, [B50USDC50WETH_ADDR, B80BAL20WETH_ADDR], block, reward=True
    )
    assert {
        "protocol": "Balancer",
        "blockchain": "ethereum",
        "wallet": WALLET_N2,
        "block_id": 16978206,
        "positions": {
            "0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8": {
                "liquidity": {
                    "holdings": [
                        {
                            "address": "0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8",
                            "balance": Decimal("0.41695566518203126"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                            "balance": Decimal("10.24608281454370054240898545"),
                        },
                        {
                            "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                            "balance": Decimal("0.005458806906415149638057440356"),
                        },
                    ],
                },
                "staked": {
                    "staked_key": "gauge_address",
                    "0x9AB7B0C7b154f626451c9e8a68dC04f58fb6e5Ce": {
                        "holdings": [
                            {
                                "address": "0x96646936b91d6B9D7D0c47C496AfBF3D6ec7B6f8",
                                "balance": Decimal("0.430936013419668177"),
                            }
                        ],
                        "underlyings": [
                            {
                                "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                                "balance": Decimal("10.58962966563745330384918783"),
                            },
                            {
                                "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                                "balance": Decimal("0.005641838408050662404836892297"),
                            },
                        ],
                        "unclaimed_rewards": [
                            {
                                "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                                "balance": Decimal("0.002255938639324377"),
                            }
                        ],
                    },
                },
                "locked": {
                    "unclaimed_rewards": [
                        {
                            "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                            "balance": Decimal("0.000019372013715193"),
                        },
                        {
                            "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                            "balance": Decimal("0.000210261212072964"),
                        },
                    ]
                },
            },
            "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56": {
                "locked": {
                    "holdings": [
                        {
                            "address": "0x5c6Ee304399DBdB9C8Ef030aB642B10820DB8F56",
                            "balance": Decimal("0.484855281271515415"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                            "balance": Decimal("1.000114468622601307282666145"),
                        },
                        {
                            "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                            "balance": Decimal("0.0009405381335007070147710888177"),
                        },
                    ],
                    "unclaimed_rewards": [
                        {
                            "address": "0xba100000625a3754423978a60c9317c58a424e3D",
                            "balance": Decimal("0.000019372013715193"),
                        },
                        {
                            "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                            "balance": Decimal("0.000210261212072964"),
                        },
                    ],
                },
            },
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    block = 17117344
    underlying = Balancer.get_protocol_data_for(Chain.ETHEREUM, WALLET_N4, BstETHSTABLE_ADDR, block)
    assert {
        "protocol": "Balancer",
        "blockchain": "ethereum",
        "block_id": 17117344,
        "wallet": WALLET_N4,
        "positions": {
            "0x32296969Ef14EB0c6d29669C550D4a0449130230": {
                "liquidity": {
                    "holdings": [
                        {
                            "address": "0x32296969Ef14EB0c6d29669C550D4a0449130230",
                            "balance": Decimal("21.590239479364203225"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
                            "balance": Decimal("10.15169431226039997458582647"),
                        },
                        {
                            "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
                            "balance": Decimal("10.93914528430790259522572181"),
                        },
                    ],
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    underlying = Balancer.get_protocol_data_for(Chain.ETHEREUM, WALLET_N5, B50wstETH50LDO_ADDR, block)
    assert {
        "protocol": "Balancer",
        "blockchain": "ethereum",
        "block_id": 17117344,
        "wallet": WALLET_N5,
        "positions": {
            "0x5f1f4E50ba51D723F12385a8a9606afc3A0555f5": {
                "liquidity": {
                    "holdings": [
                        {
                            "address": "0x5f1f4E50ba51D723F12385a8a9606afc3A0555f5",
                            "balance": Decimal("36.804073376884509435"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32",
                            "balance": Decimal("576.5066246253847582651532174"),
                        },
                        {
                            "address": "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0",
                            "balance": Decimal("0.5871242486850998522269758922"),
                        },
                    ],
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    underlying = Balancer.get_protocol_data_for(Chain.ETHEREUM, WALLET_N6, bbaUSD_ADDR, block)
    assert {
        "protocol": "Balancer",
        "blockchain": "ethereum",
        "block_id": 17117344,
        "wallet": WALLET_N6,
        "positions": {
            "0xA13a9247ea42D743238089903570127DdA72fE44": {
                "liquidity": {
                    "holdings": [
                        {
                            "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                            "balance": Decimal("115153.259450563547473691"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                            "balance": Decimal("34481.50498155417847374249388"),
                        },
                        {
                            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                            "balance": Decimal("40407.38426818377061669310919"),
                        },
                        {
                            "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                            "balance": Decimal("39386.25356751312943263976821"),
                        },
                    ],
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    underlying = Balancer.get_protocol_data_for(Chain.ETHEREUM, WALLET_39d, bbaUSD_ADDR, block)
    assert {
        "protocol": "Balancer",
        "blockchain": "ethereum",
        "block_id": 17117344,
        "wallet": WALLET_39d,
        "positions": {
            "0xA13a9247ea42D743238089903570127DdA72fE44": {
                "liquidity": {
                    "holdings": [
                        {
                            "address": "0xA13a9247ea42D743238089903570127DdA72fE44",
                            "balance": Decimal("28410.770133654655333456"),
                        }
                    ],
                    "underlyings": [
                        {
                            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7",
                            "balance": Decimal("8507.324209211599435789547375"),
                        },
                        {
                            "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
                            "balance": Decimal("9969.365275660933377069411768"),
                        },
                        {
                            "address": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
                            "balance": Decimal("9717.430508450752362261707289"),
                        },
                    ],
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    block = 28721619
    underlying = Balancer.get_protocol_data_for(
        Chain.GNOSIS, WALLET_e6f, "0xbad20c15a773bf03ab973302f61fabcea5101f0a", block, reward=True
    )
    assert {
        "protocol": "Balancer",
        "blockchain": "gnosis",
        "block_id": 28721619,
        "wallet": Web3.to_checksum_address(WALLET_e6f),
        "positions": {
            "0xbAd20c15A773bf03ab973302F61FAbceA5101f0A": {
                "staked": {
                    "staked_key": "gauge_address",
                    "0x27519F69b2Ac912aeb6fE066180FB25a17c71755": {
                        "holdings": [
                            {
                                "address": "0xbAd20c15A773bf03ab973302F61FAbceA5101f0A",
                                "balance": Decimal("2618.823016673511834775"),
                            }
                        ],
                        "underlyings": [
                            {
                                "address": "0x6A023CCd1ff6F2045C3309768eAd9E68F978f6e1",
                                "balance": Decimal("1330.644525157873920497987352"),
                            },
                            {
                                "address": "0x6C76971f98945AE98dD7d4DFcA8711ebea946eA6",
                                "balance": Decimal("1142.204886390243725927584743"),
                            },
                        ],
                        "unclaimed_rewards": [
                            {
                                "address": "0x7eF541E2a22058048904fE5744f9c7E4C57AF717",
                                "balance": Decimal("470.98333553991963146"),
                            }
                        ],
                    },
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    block = 28275634
    underlying = Balancer.get_protocol_data_for(Chain.GNOSIS, WALLET_e6f, bb_ag_USD_ADDR, block, reward=True)
    assert {
        "protocol": "Balancer",
        "blockchain": "gnosis",
        "block_id": 28275634,
        "wallet": Web3.to_checksum_address(WALLET_e6f),
        "positions": {
            "0xFEdb19Ec000d38d92Af4B21436870F115db22725": {
                "staked": {
                    "staked_key": "gauge_address",
                    "0xDe3B7eC86B67B05D312ac8FD935B6F59836F2c41": {
                        "holdings": [
                            {
                                "address": "0xFEdb19Ec000d38d92Af4B21436870F115db22725",
                                "balance": Decimal("576175.739891078705636246"),
                            }
                        ],
                        "underlyings": [
                            {
                                "address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
                                "balance": Decimal("224867.5522071186644467065688"),
                            },
                            {
                                "address": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
                                "balance": Decimal("156797.8000451423306782755605"),
                            },
                            {
                                "address": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
                                "balance": Decimal("191847.3777747815376180144618"),
                            },
                        ],
                        "unclaimed_rewards": [
                            {
                                "address": "0x7eF541E2a22058048904fE5744f9c7E4C57AF717",
                                "balance": Decimal("72.028749058272541921"),
                            }
                        ],
                    },
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying

    underlying = Balancer.get_protocol_data_for(Chain.GNOSIS, WALLET_e6f, B50bbagGNO50bbagUSD_ADDR, block, reward=True)
    assert {
        "protocol": "Balancer",
        "blockchain": "gnosis",
        "block_id": 28275634,
        "wallet": Web3.to_checksum_address(WALLET_e6f),
        "positions": {
            "0xB973Ca96a3f0D61045f53255E319AEDb6ED49240": {
                "staked": {
                    "staked_key": "gauge_address",
                    "0x7E13b8b95d887c2326C25e71815F33Ea10A2674e": {
                        "holdings": [
                            {
                                "address": "0xB973Ca96a3f0D61045f53255E319AEDb6ED49240",
                                "balance": Decimal("157560.502939494000916108"),
                            }
                        ],
                        "underlyings": [
                            {
                                "address": "0xe91D153E0b41518A2Ce8Dd3D7944Fa863463a97d",
                                "balance": Decimal("332546.5277054682282243345648"),
                            },
                            {
                                "address": "0x4ECaBa5870353805a9F068101A40E0f32ed605C6",
                                "balance": Decimal("231881.2271716350671750707592"),
                            },
                            {
                                "address": "0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83",
                                "balance": Decimal("283714.4741525013588273711511"),
                            },
                            {
                                "address": "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb",
                                "balance": Decimal("7323.347699280704544261534365"),
                            },
                        ],
                        "unclaimed_rewards": [
                            {
                                "address": "0x7eF541E2a22058048904fE5744f9c7E4C57AF717",
                                "balance": Decimal("422.039676607937704001"),
                            }
                        ],
                    },
                },
            }
        },
        "positions_key": "liquidity_pool_address",
        "version": 0,
    } == underlying


def test_swap_fees():
    blockstart = date_to_block("2023-02-20 18:25:00", Chain.ETHEREUM)
    blockend = date_to_block("2023-02-20 18:30:00", Chain.ETHEREUM)

    vault_address = Balancer.Vault(Chain.ETHEREUM, blockend).address
    lp = Balancer.LiquidityPool(Chain.ETHEREUM, blockend, B80BAL20WETH_ADDR)
    swaps = lp.swap_fees(vault_address, blockstart)
    assert swaps == [
        {
            "block": 16671528,
            "token_in": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "amount_in": Decimal("0.09017533361647305728"),
        },
        {
            "block": 16671542,
            "token_in": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
            "amount_in": Decimal("0.0795350748930228736"),
        },
    ]


def test_swap_fees_apr():
    blockend = date_to_block("2023-02-20 18:30:00", Chain.ETHEREUM)
    apr = Balancer.get_swap_fees_apr(B80BAL20WETH_ADDR, Chain.ETHEREUM, blockend)
    assert apr == Decimal("0.596125086010151913782740200")
    apy = Balancer.get_swap_fees_apr(B80BAL20WETH_ADDR, Chain.ETHEREUM, blockend, apy=True)
    assert apy == Decimal("0.815071898400229530363657020")
