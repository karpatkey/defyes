import json
from decimal import Decimal
from pathlib import Path

from defabipedia import Chain

# thegraph queries
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from karpatkit.cache import const_call
from karpatkit.constants import ABI_TOKEN_SIMPLIFIED
from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput

from defyes.functions import get_contract, to_token_amount

DB_FILE = Path(__file__).parent / "db.json"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IDLE Deployer
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IDLE Deployer address
DEPLOYER: str = "0x1F98431c8aD98523631AE4a59f267346ea31F984"

GAUGE_CONTROLLER: str = "0xaC69078141f76A1e257Ee889920d02Cc547d632f"

# check for all_markets
IDLE_CONTROLLER: str = "0x275DA8e61ea8E02d51EDd8d0DC5c0E62b4CDB0BE"

CDO_PROXY: str = "0x3C9916BB9498f637e2Fa86C2028e26275Dc9A631"

IDLE_TOKEN: str = "0x875773784Af8135eA0ef43b5a374AaD105c5D39e"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IDLE CDO ABI - AAStaking, AATranche, BBStaking, BBTranche, getAPR, getIncentiveTokens, priceAA, priceBB, token, unclaimedFees, virtualPrice
ABI_CDO_IDLE: str = (
    '[{"inputs":[],"name":"AAStaking","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"AATranche","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"BBStaking","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"BBTranche","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"_tranche","type":"address"}],"name":"getApr","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"getIncentiveTokens","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"priceAA","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"priceBB","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"unclaimedFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"_tranche","type":"address"}],"name":"virtualPrice","outputs":[{"internalType":"uint256","name":"_virtualPrice","type":"uint256"}],"stateMutability":"view","type":"function"}]'
)

# IDLE GAUGE CONTROLLER - n_gauges, gauges
ABI_GAUGE_CONTROLLER: str = (
    '[{"stateMutability":"view","type":"function","name":"n_gauges","inputs":[],"outputs":[{"name":"","type":"int128"}],"gas":2988},\
                        {"stateMutability":"view","type":"function","name":"gauges","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3093}]'
)

# IDLE GAUGE ABI - decimals, claimed_reward, claimable_reward_write, claimabe_tokens, lp_token, balanceOf, reward_tokens
ABI_GAUGE: str = (
    '[{"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":288},\
            {"stateMutability":"view","type":"function","name":"claimed_reward","inputs":[{"name":"_addr","type":"address"},{"name":"_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3066},\
            {"stateMutability":"view","type":"function","name":"claimable_reward_write","inputs":[{"name":"_addr","type":"address"},{"name":"_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":1209922},\
            {"stateMutability":"view","type":"function","name":"claimable_tokens","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3046449},\
            {"stateMutability":"view","type":"function","name":"lp_token","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":3138},\
            {"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3473},\
            {"stateMutability":"view","type":"function","name":"reward_tokens","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3723}]'
)

ABI_CDO_PROXY: str = (
    '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"proxy","type":"address"}],"name":"CDODeployed","type":"event"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"},{"internalType":"address","name":"admin","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"deployCDO","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
)


def get_addresses_subgraph(block: int | str, blockchain: str, web3=None) -> dict:
    cdos = []
    skip = 0
    while True:
        # Initialize subgraph
        subgraph_url = "https://api.thegraph.com/subgraphs/name/samster91/idle-tranches"
        idle_transport = RequestsHTTPTransport(url=subgraph_url, verify=True, retries=3)
        client = Client(transport=idle_transport)

        query_string = """
        query {{
        cdos(first: {first}, skip: {skip}) {{
            id
            AATrancheToken {{
                id
            }}
            BBTrancheToken {{
                id
            }}
            underlyingToken
        }}
        }}
        """
        num_pools_to_query = 1000
        formatted_query_string = query_string.format(first=num_pools_to_query, skip=skip)
        response = client.execute(gql(formatted_query_string))
        cdos.extend(response["cdos"])

        if len(response["cdos"]) < 1000:
            break
        else:
            skip = 1000

    result = {"cdos": []}

    if web3 is None:
        web3 = get_node(blockchain)

    gauges = get_gauges(block, blockchain, web3=web3)

    for cdo in cdos:
        cdo_address = Web3.to_checksum_address(cdo["id"])
        aa_token = Web3.to_checksum_address(cdo["AATrancheToken"]["id"])
        bb_token = Web3.to_checksum_address(cdo["BBTrancheToken"]["id"])

        aa_gauge_contract_address = None
        bb_gauge_contract_address = None
        for gauge in gauges:
            if gauge[1] == aa_token:
                aa_gauge_contract_address = gauge[0]
            elif gauge[1] == bb_token:
                bb_gauge_contract_address = gauge[0]

        underlying_token = Web3.to_checksum_address(cdo["underlyingToken"])

        result["cdos"].append(
            {
                "CDO": cdo_address,
                "underlyingToken": underlying_token,
                "AATranche": {"AATrancheToken": aa_token, "AAGauge": aa_gauge_contract_address},
                "BBTranche": {"BBTrancheToken": bb_token, "BBGauge": bb_gauge_contract_address},
            }
        )

    return result


def get_gauges(block: int | str, blockchain: str, web3=None, decimals=True) -> list:
    gauges = []

    if web3 is None:
        web3 = get_node(blockchain)

    gauge_controller_contract = get_contract(GAUGE_CONTROLLER, blockchain, web3=web3, abi=ABI_GAUGE_CONTROLLER)
    n_gauges = gauge_controller_contract.functions.n_gauges().call(block_identifier=block)
    for i in range(0, n_gauges):
        # TODO: check if const_call can be used
        gauge_address = gauge_controller_contract.functions.gauges(i).call(block_identifier=block)
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE)
        lp_token_address = const_call(gauge_contract.functions.lp_token())
        gauges.append([gauge_address, lp_token_address])
    return gauges


def get_all_rewards(
    wallet: str, gauge_address: str, block: int | str, blockchain: str, web3=None, decimals: bool = True
) -> list:
    rewards = []

    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE)
    idle_rewards = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block)
    rewards.append([IDLE_TOKEN, to_token_amount(IDLE_TOKEN, idle_rewards, blockchain, web3, decimals)])

    for i in range(0, 10):
        reward_tokens = const_call(gauge_contract.functions.reward_tokens(i))
        if reward_tokens == "0x0000000000000000000000000000000000000000":
            break
        claimable_rewards = gauge_contract.functions.claimable_reward_write(wallet, reward_tokens).call(
            block_identifier=block
        )

        all_rewards = claimable_rewards
        rewards.append([reward_tokens, to_token_amount(reward_tokens, all_rewards, blockchain, web3, decimals)])

    return rewards


def get_balances(
    tranche: dict,
    cdo_address: str,
    underlying_token: str,
    wallet: str,
    block: int | str,
    blockchain: str,
    web3=None,
    decimals: bool = True,
) -> list:
    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    cdo_contract = get_contract(cdo_address, blockchain, web3=web3, abi=ABI_CDO_IDLE)

    if tranche.get("AATrancheToken"):
        tranche_token = tranche["AATrancheToken"]
        gauge_token = tranche["AAGauge"]
    elif tranche.get("BBTrancheToken"):
        tranche_token = tranche["BBTrancheToken"]
        gauge_token = tranche["BBGauge"]

    balances = {
        tranche_token: {
            "holdings": [],
            "underlying": [],
        }
    }

    tranche_contract = get_contract(tranche_token, blockchain, web3=web3, abi=ABI_TOKEN_SIMPLIFIED)
    # FIXME: added this try because if the tranch does not exist for the given block the balanceOf function reverts
    try:
        tranche_token_balance = tranche_contract.functions.balanceOf(wallet).call(block_identifier=block)
        underlying_token_balance_tranche = tranche_token_balance * (
            cdo_contract.functions.virtualPrice(tranche_token).call(block_identifier=block) / Decimal(10**18)
        )
    except Exception as e:
        if type(e) == BadFunctionCallOutput:
            tranche_token_balance = 0
            underlying_token_balance_tranche = 0

    balances[tranche_token]["holdings"].append(
        {
            "address": tranche_token,
            "balance": to_token_amount(tranche_token, tranche_token_balance, blockchain, web3, decimals),
        }
    )

    balances[tranche_token]["underlying"].append(
        {
            "address": underlying_token,
            "balance": to_token_amount(underlying_token, underlying_token_balance_tranche, blockchain, web3, decimals),
        }
    )

    if gauge_token:
        gauge_token_contract = get_contract(gauge_token, blockchain, web3=web3, abi=ABI_GAUGE)
        gauge_token_balance = gauge_token_contract.functions.balanceOf(wallet).call(block_identifier=block)
        underlying_token_balance_gauge = gauge_token_balance * (
            cdo_contract.functions.virtualPrice(tranche_token).call(block_identifier=block) / Decimal(10**18)
        )
        balances[tranche_token]["holdings"].append(
            {
                "address": gauge_token,
                "balance": to_token_amount(gauge_token, gauge_token_balance, blockchain, web3, decimals),
            }
        )

        balances[tranche_token]["underlying"][0]["balance"] += to_token_amount(
            underlying_token, underlying_token_balance_gauge, blockchain, web3, decimals
        )

    return balances


def underlying(
    tranche_address: str,
    wallet: str,
    block: int | str,
    blockchain: str,
    web3=None,
    decimals: bool = True,
    db: bool = True,
    reward: bool = False,
) -> list:
    result = {
        "blockchain": blockchain,
        "block": block,
        "protocol": "Idle",
        "positions_key": "tranche_token",
        "decimals": decimals,
        "version": 0,
        "wallet": wallet,
        "positions": {},
    }

    if web3 is None:
        web3 = get_node(blockchain)

    tranche_address = Web3.to_checksum_address(tranche_address)

    if db:
        with open(DB_FILE) as db_file:
            data = json.load(db_file)
        cdos = data["cdos"]
    else:
        cdo = get_addresses_subgraph(block, blockchain, web3=web3)

    tranche = None
    for cdo in cdos:
        if cdo["AATranche"]["AATrancheToken"] == tranche_address:
            tranche = cdo["AATranche"]
            gauge_address = cdo["AATranche"]["AAGauge"]
            cdo_address = cdo["CDO"]
            underlying_token = cdo["underlyingToken"]
            break
        elif cdo["BBTranche"]["BBTrancheToken"] == tranche_address:
            tranche = cdo["BBTranche"]
            gauge_address = cdo["BBTranche"]["BBGauge"]
            cdo_address = cdo["CDO"]
            underlying_token = cdo["underlyingToken"]
            break

    if tranche:
        result["positions"] = get_balances(
            tranche,
            cdo_address,
            underlying_token,
            wallet,
            block,
            blockchain,
            web3,
            decimals,
        )

        if reward and gauge_address is not None:
            all_rewards = get_all_rewards(wallet, gauge_address, block, blockchain, web3, decimals=decimals)

            result["positions"][tranche_address]["rewards"] = []
            for rewards in all_rewards:
                result["positions"][tranche_address]["rewards"].append(
                    {
                        "address": rewards[0],
                        "balance": rewards[1],
                    }
                )

    return result


# FIXME: this function must be refactored
# def underlying_all(
#     wallet: str,
#     block: Union[int, str],
#     blockchain: str,
#     web3=None,
#     decimals: bool = True,
#     db: bool = True,
#     rewards: bool = False,
# ) -> list:
#     balances_all = []
#     if db:
#         file = open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/db/Idle_db.json")
#         data = json.load(file)
#         addresses = data["tranches"]
#     else:
#         addresses = get_addresses(block, blockchain, web3=web3)

#     for address in addresses:
#         amounts = get_amounts(
#             address["underlying_token"],
#             address["CDO address"],
#             address["AA tranche"]["aa_token"],
#             address["bb token"],
#             address["AA tranche"]["aa_gauge"],
#             wallet,
#             block,
#             blockchain,
#             web3,
#             decimals,
#         )
#         if amounts:
#             if rewards and address["AA tranche"]["aa_gauge"] is not None:
#                 rewards = get_all_rewards(
#                     wallet, address["AA tranche"]["aa_gauge"], block, blockchain, web3, decimals=decimals
#                 )
#                 amounts.append(rewards)
#             balances_all.append(amounts)

#     return balances_all


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_db (function to update database with addresses from all tranches that have been deployed)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db(block="latest") -> dict:
    """

    :return:
    """
    with open(DB_FILE, "w") as db_file:
        cdos = get_addresses_subgraph(block, Chain.ETHEREUM)
        json.dump(cdos, db_file, indent=4)
