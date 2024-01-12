import json
import logging
from decimal import Decimal

import requests
from defabipedia import Chain
from karpatkit.constants import Address
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import balance_of, last_block, to_token_amount

from . import curve, uniswapv3

logger = logging.getLogger(__name__)

WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
sETH2 = "0xFe2e637202056d30016725477c5da089Ab0A043A"
rETH2 = "0x20BC832ca081b91433ff6c17f85701B6e92486c5"
SWISE_eth = "0x48C3399719B582dD63eB5AADf12A40B4C3f52FA2"
SWISE_gno = "0xfdA94F056346d2320d4B5E468D6Ad099b2277746"
sGNO = "0xA4eF9Da5BA71Cc0D2e5E877a910A37eC43420445"
rGNO = "0x6aC78efae880282396a335CA2F79863A1e6831D4"
GNO = "0x9C58BAcC331c9aa871AFD802DB6379a98e80CEdb"

tokens = {
    "ethereum": {
        "underlying": Address.ZERO,
        "staking": sETH2,
        "rewards": rETH2,
    },
    Chain.GNOSIS: {
        "underlying": GNO,
        "staking": sGNO,
        "rewards": rGNO,
    },
}
# Tokens that can be accrued as rewards by depositing funds in the Curve or Uniswap V3 pools
reward_addresses = {"ethereum": [rETH2, SWISE_eth], Chain.GNOSIS: [rGNO, SWISE_gno]}

Pools = {
    Chain.GNOSIS: {
        "curve": [
            {"name": "sGNO-GNO", "LPtoken": "0xBdF4488Dcf7165788D438b62B4C8A333879B7078"},
            {
                "name": "rGNO-sGNO",
                "LPtoken": "0x5d7309a01b727d6769153fcb1df5587858d53b9c",
            },
        ]
    },
    "ethereum": {
        "uniswap v3": [
            {"name": "WETH-sETH2", "tokens": [WETH, sETH2], "fee": 3000},
            {"name": "rETH2-sETH2", "tokens": [rETH2, sETH2], "fee": 500},
            {"name": "SWISE-sETH2", "tokens": [SWISE_eth, sETH2], "fee": 3000},
        ]
    },
}


def check_curve_pools(
    wallet: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True, reward: bool = False
):
    if blockchain is not Chain.GNOSIS:
        raise ValueError("Stakewise Curve pools are only deployed on Gnosis Chain.")

    if web3 is None:
        web3 = get_node(blockchain)

    # FIXME: this will change once we change curve.underlying so that it returns a dictionary
    result = {}

    for item in Pools[Chain.GNOSIS]["curve"]:
        balances = curve.underlying(wallet, item["LPtoken"], block, blockchain, web3=web3, decimals=decimals)

        result[item["name"]] = {"LP token": item["LPtoken"], "balances": []}
        for element in balances:
            result[item["name"]]["balances"].append({"token": element[0], "unstaked": element[1], "staked": element[2]})
        if reward:
            rewards = curve.get_all_rewards(wallet, item["LPtoken"], block, blockchain, web3=web3, decimals=decimals)
            result[item["name"]]["rewards"] = []

            for element in rewards:
                result[item["name"]]["rewards"].append({"token": element[0], "balance": element[1]})

    return result


def check_uniswap_v3_pools(
    wallet: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True, reward: bool = False
):
    if blockchain is not Chain.ETHEREUM:
        raise ValueError("Stakewise Uniswap V3 pools are only deployed on Ethereum.")

    if web3 is None:
        web3 = get_node(blockchain)

    nft_ids = uniswapv3.allnfts(wallet, block, blockchain, web3=web3)
    result = {}

    for nft_id in nft_ids:
        nft = uniswapv3.NFTPosition(nft_id, blockchain, block, web3, decimals)
        tokens = [nft.token0, nft.token1]
        for item in Pools["ethereum"]["uniswap v3"]:
            if set(tokens) == set(item["tokens"]) and nft.fee == item["fee"]:
                result[item["name"]] = {"NFT ID": nft_id, "balances": []}
                balances = uniswapv3.underlying(wallet, nft_id, block, blockchain, web3=web3, decimals=decimals)
                for element in balances:
                    result[item["name"]]["balances"].append(
                        {
                            "token": element[0],
                            "balance": element[1],
                        }
                    )
                if reward:
                    result[item["name"]]["fees"] = []
                    fees = uniswapv3.get_fee(nft_id, block, blockchain, web3=web3, decimals=decimals)
                    for element in fees:
                        result[item["name"]]["fees"].append(
                            {
                                "token": element[0],
                                "balance": element[1],
                            }
                        )
        return result


def get_all_rewards(
    wallet: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True, pools: bool = False
) -> dict:
    # FIXME: the current code uses an API to fetch the latest unclaimed rewards. We need to find a way to be able to get historical unclaimed rewards
    if not isinstance(block, str):
        raise ValueError(
            "Historical unclaimed rewards not supported. Use block=latest to get current unclaimed rewards."
        )

    if web3 is None:
        web3 = get_node(blockchain)

    chain = "mainnet" if blockchain is Chain.ETHEREUM else Chain.GNOSIS
    response = requests.get(f"https://api.stakewise.io/distributor-claims/{wallet}/?network={chain}")
    data = json.loads(response.text, parse_float=Decimal)

    result = {"protocol": "Stakewise", "blockchain": blockchain, "block": block, "rewards": []}
    # If there are no unclaimed rewards the API call returns {"detail": "Not found."}
    if "detail" not in data:
        for element in data["rewards"]:
            if element["reward_token"] in reward_addresses[blockchain]:
                if element["reward_token"] in [entry["token"] for entry in result["rewards"]]:
                    for entry in result["rewards"]:
                        if element["reward_token"] == entry["token"]:
                            entry["balance"] += to_token_amount(
                                element["reward_token"], int(element["value"]), blockchain, web3=web3, decimals=decimals
                            )
                else:
                    result["rewards"].append(
                        {
                            "token": element["reward_token"],
                            "balance": to_token_amount(
                                element["reward_token"], int(element["value"]), blockchain, web3=web3, decimals=decimals
                            ),
                        }
                    )

    for element in reward_addresses[blockchain]:
        if element not in [entry["token"] for entry in result["rewards"]] or result["rewards"] == []:
            result["rewards"].append({"token": element, "balance": Decimal(0)})

    return result


def underlying(
    wallet: str,
    block: int | str,
    blockchain: str,
    decimals: bool = True,
    web3: object = None,
    reward: bool = False,
    pools: bool = False,
) -> dict:
    """
    Returns the balances of the staking and reward tokens as a dictionary.

    Parameters
    ----------
    wallet : str
        address of the wallet holding the position
    block : int or 'latest'
        block number at which the data is queried
    web3: obj
        optional, already instantiated web3 object
    decimals: bool
        specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True
    reward: bool
        if True adds the balances of unclaimed rewards to the result

    Returns
    ----------
    dict
        {
            'blockchain': 'ethereum',
            'block': 17693094,
            'protocol': 'Stakewise',
            'positions_key': None,
            'decimals': False,
            'version': 0,
            'wallet': '0x05E61adDCef87ad8548236eb5Cbf2f699C834935',
            'positions': {
                'staking_ETH': {
                    'holdings': [{
                            'token': '0xFe2e637202056d30016725477c5da089Ab0A043A',
                            'balance': Decimal('0.849414886512576674')
                        }
                    ],
                    'underlying': [{
                            'token': '0x0000000000000000000000000000000000000000',
                            'balance': Decimal('0.849414886512576674')
                        }
                    ]
                }
            },
            'unclaimed_rewards': [{
                    'token': '0x20BC832ca081b91433ff6c17f85701B6e92486c5',
                    'balance': Decimal('854744963544512')
                }, {
                    'token': '0x48C3399719B582dD63eB5AADf12A40B4C3f52FA2',
                    'balance': Decimal('203099406601438885')
                }
            ]
        }
    """
    # FIXME: the current code uses an API to fetch the latest unclaimed rewards. We need to find a way to be able to get historical unclaimed rewards
    if reward:
        if not isinstance(block, str):
            raise ValueError(
                "Historical unclaimed rewards not supported. Use block=latest to get current unclaimed rewards."
            )

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    staking_balance = balance_of(wallet, tokens[blockchain]["staking"], block, blockchain, web3=web3)
    # We are removing the balance of rewards held by the wallet
    # rewards_balance = balance_of(wallet, tokens[blockchain]["rewards"], block, blockchain, web3=web3)

    if block == "latest":
        block_result = last_block(blockchain)
    else:
        block_result = block

    result = {
        "blockchain": blockchain,
        "block": block_result,
        "protocol": "Stakewise",
        "positions_key": None,
        "decimals": decimals,
        "version": 0,
        "wallet": wallet,
        "positions": {
            "staking_ETH": {
                "holdings": [{"token": tokens[blockchain]["staking"], "balance": staking_balance}],
                "underlying": [{"token": tokens[blockchain]["underlying"], "balance": staking_balance}],
            }
        },
    }

    if reward:
        rewards_data = get_all_rewards(wallet, block, blockchain, decimals=decimals, web3=web3)
        result["unclaimed_rewards"] = rewards_data["rewards"]

    if pools:
        if blockchain == Chain.GNOSIS:
            result["Curve_pools"] = check_curve_pools(
                wallet, block, blockchain, web3=web3, decimals=decimals, reward=reward
            )
        if blockchain == Chain.ETHEREUM:
            result["Uniswap_V3_pools"] = check_uniswap_v3_pools(
                wallet, block, blockchain, web3=web3, decimals=decimals, reward=reward
            )

    return result
