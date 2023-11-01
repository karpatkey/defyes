import json
import logging
import math
import re
from contextlib import suppress
from datetime import datetime
from decimal import Decimal

import requests
from web3 import Web3
from web3.exceptions import ABIFunctionNotFound, BadFunctionCallOutput, ContractLogicError

from defyes.cache import cache_call, const_call
from defyes.constants import ABI_TOKEN_SIMPLIFIED, Address, APIKey, Chain
from defyes.explorer import ChainExplorer
from defyes.helpers import suppress_error_codes
from defyes.lazytime import Time
from defyes.node import get_node

logger = logging.getLogger(__name__)


# CUSTOM EXCEPTIONS
class BlockchainError(Exception):
    pass


def to_token_amount(
    token_address: str, amount: int | Decimal, blockchain: str, web3: Web3, decimals: bool = True
) -> Decimal:
    # This function provides support for correctly rounded decimal floating point arithmetic.
    decimals = get_decimals(token_address, blockchain=blockchain, web3=web3) if decimals else 0
    return amount / Decimal(10**decimals)


def last_block(blockchain, web3=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    return web3.eth.block_number


def ensure_a_block_number(block: int | str, blockchain: Chain):
    if isinstance(block, int):
        return block
    elif block == "latest":
        return last_block(blockchain)
    else:
        raise ValueError("block should be an integer or just the string 'latest'")


def date_to_block(datestring, blockchain, utc=0) -> int:
    """
    Returns the block number of a specified date.

    The date can be a string (in the format '%Y-%m-%d %H:%M:%S') or a datetime object. UTC is asumed as timezone.
    An example datestring: '2023-02-20 18:30:00'.
    """
    if isinstance(datestring, datetime):
        timestamp = datestring.timestamp()
    else:
        timestamp = Time.from_string(datestring)

    return timestamp_to_block(timestamp, blockchain)


def timestamp_to_block(timestamp, blockchain) -> int:
    return ChainExplorer(blockchain).block_from_time(timestamp)


def block_to_date(block, blockchain, utc=0):
    return str(Time(ChainExplorer(blockchain).time_from_block(block)))


def get_blocks_per_year(blockchain):
    current_block = last_block(blockchain)
    ts = math.floor(datetime.now().timestamp()) - (3600 * 24 * 365)
    block = ChainExplorer(blockchain).block_from_time(ts)

    block_delta = current_block - block

    return block_delta


# ERC20 TOKENS
# token_info
@cache_call()
def token_info(token_address, blockchain):  # NO ESTÁ Chain.POLYGON
    ETHPLORER_URL = "https://api.ethplorer.io/getTokenInfo/%s?apiKey=%s"
    BLOCKSCOUT_URL = "https://blockscout.com/xdai/mainnet/api?module=token&action=getToken&contractaddress=%s"

    if blockchain.lower() == Chain.ETHEREUM:
        data = requests.get(ETHPLORER_URL % (token_address, APIKey.ETHPLORER)).json()

    elif blockchain.lower() == Chain.GNOSIS:
        data = requests.get(BLOCKSCOUT_URL % token_address).json()["result"]

    return data


def balance_of(address, contract_address, block, blockchain, web3=None, decimals=True) -> Decimal:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    address = Web3.to_checksum_address(address)
    contract_address = Web3.to_checksum_address(contract_address)

    balance = 0
    if contract_address == Address.ZERO:
        balance = web3.eth.get_balance(address, block)
    else:
        token_contract = web3.eth.contract(address=contract_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
        try:
            balance = token_contract.functions.balanceOf(address).call(block_identifier=block)
        except ContractLogicError:
            pass

    return to_token_amount(contract_address, balance, blockchain, web3, decimals)


def total_supply(
    token_address: str, block: int | str, blockchain: str, web3: Web3 = None, decimals: bool = True
) -> Decimal:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    token_address = Web3.to_checksum_address(token_address)

    token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
    total_supply_v = token_contract.functions.totalSupply().call(block_identifier=block)

    return to_token_amount(token_address, total_supply_v, blockchain, web3, decimals)


def get_decimals(token_address, blockchain, web3=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    token_address = Web3.to_checksum_address(token_address)

    if token_address == Address.ZERO or token_address == Address.E:
        decimals = 18
    else:
        token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
        decimals = const_call(token_contract.functions.decimals())

    return decimals


def get_symbol(token_address, blockchain, web3=None, block="latest") -> str:
    token_address = Web3.to_checksum_address(token_address)

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    special_addr_mapping = {
        Chain.ETHEREUM: "ETH",
        Chain.OPTIMISM: "ETH",
        Chain.ARBITRUM: "ETH",
        Chain.POLYGON: "MATIC",
        Chain.GNOSIS: "GNOSIS",
        Chain.FANTOM: "FTM",
        Chain.AVALANCHE: "AVAX",
        Chain.BINANCE: "BNB",
    }

    if token_address in [Address.ZERO, Address.E]:
        symbol = special_addr_mapping[blockchain]
    else:
        symbol = infer_symbol(web3, blockchain, token_address)

        if not isinstance(symbol, str):
            symbol = symbol.hex()
            symbol = bytes.fromhex(symbol).decode("utf-8").rstrip("\x00")

    return symbol


def infer_symbol(web3, blockchain, token_address):
    contract = web3.eth.contract(address=token_address, abi=ABI_TOKEN_SIMPLIFIED)
    for method_name in ("symbol", "SYMBOL"):
        with suppress(ContractLogicError, BadFunctionCallOutput, OverflowError), suppress_error_codes():
            return const_call(getattr(contract.functions, method_name)())

    abi = ChainExplorer(blockchain).abi_from_address(token_address)
    contract = web3.eth.contract(address=token_address, abi=abi)
    with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
        return const_call(contract.functions.symbol())

    raise ValueError(f"Token {token_address} has no symbol()")


# CONTRACTS AND ABIS
def get_contract(contract_address, blockchain, web3=None, abi=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    contract_address = Web3.to_checksum_address(contract_address)

    if abi is None:
        abi = ChainExplorer(blockchain).abi_from_address(contract_address)
        return web3.eth.contract(address=contract_address, abi=abi)
    else:
        return web3.eth.contract(address=contract_address, abi=abi)


def get_contract_proxy_abi(contract_address, abi_contract_address, blockchain, web3=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    address = Web3.to_checksum_address(contract_address)

    abi = ChainExplorer(blockchain).abi_from_address(abi_contract_address)
    return web3.eth.contract(address=address, abi=abi)


def search_proxy_impl_address(contract_address, blockchain, web3=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain)

    proxy_impl_address = Address.ZERO

    contract_address = Web3.to_checksum_address(contract_address)

    # OpenZeppelins' EIP-1967 - Example in mainnet: 0xE95A203B1a91a908F9B9CE46459d101078c2c3cb
    IMPLEMENTATION_SLOT_EIP_1967 = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
    proxy_impl_address = Web3.to_hex(
        web3.eth.get_storage_at(contract_address, IMPLEMENTATION_SLOT_EIP_1967, block_identifier=block)
    )
    proxy_impl_address = Web3.to_checksum_address("0x" + proxy_impl_address[-40:])

    # OpenZeppelins' EIP-1167 - Example in GC: 0x793fAF861a78B07c0C8c0ed1450D3919F3473226)
    if proxy_impl_address == Address.ZERO:
        bytecode = web3.eth.get_code(contract_address, block_identifier=block).hex()
        if bytecode[2:22] == "363d3d373d3d3d363d73" and bytecode[62:] == "5af43d82803e903d91602b57fd5bf3":
            proxy_impl_address = Web3.to_checksum_address("0x" + bytecode[22:62])

    # Custom proxy implementation (similar to EIP-1167) -
    # Examples: mainnet: 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14 / GC: 0x7B7DA887E0c18e631e175532C06221761Db30A24
    if proxy_impl_address == Address.ZERO:
        bytecode = web3.eth.get_code(contract_address, block_identifier=block).hex()
        if bytecode[2:32] == "366000600037611000600036600073" and bytecode[72:] == "5af41558576110006000f3":
            proxy_impl_address = Web3.to_checksum_address("0x" + bytecode[32:72])

    # OpenZeppelins' Unstructured Storage proxy pattern - Example: USDC in mainnet (0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48)
    IMPLEMENTATION_SLOT_UNSTRUCTURED = "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3"
    if proxy_impl_address == Address.ZERO:
        proxy_impl_address = Web3.to_hex(
            web3.eth.get_storage_at(contract_address, IMPLEMENTATION_SLOT_UNSTRUCTURED, block_identifier=block)
        )
        proxy_impl_address = Web3.to_checksum_address("0x" + proxy_impl_address[-40:])

    # OpenZeppelins' EIP-897 DelegateProxy - Examples: stETH in mainnet (0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84)
    # It also includes the custom proxy implementation of the Comptroller: 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B
    if proxy_impl_address == Address.ZERO:
        contract = get_contract(contract_address, blockchain, web3=web3)
        if contract is not None:
            for func in [obj for obj in contract.abi if obj["type"] == "function"]:
                name = str(func["name"].lower())
                if "implementation" in name:
                    output_types = [output["type"] for output in func["outputs"]]
                    if output_types == ["address"]:
                        try:
                            proxy_impl_address_func = getattr(contract.functions, func["name"])
                            proxy_impl_address = proxy_impl_address_func().call(block_identifier=block)
                            break
                        except Exception as e:
                            if type(e) == ContractLogicError or type(e) == BadFunctionCallOutput:
                                continue

    # Custom proxy implementation (used by Safes) - Example: mainnet: 0x4F2083f5fBede34C2714aFfb3105539775f7FE64
    if proxy_impl_address == Address.ZERO:
        contract_custom_abi = get_contract(
            contract_address,
            Chain.ETHEREUM,
            abi='[{"inputs":[{"internalType":"uint256","name":"offset","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"getStorageAt","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"}]',
        )
        try:
            proxy_impl_address = Web3.to_hex(contract_custom_abi.functions.getStorageAt(0, 1).call())
            proxy_impl_address = Web3.to_checksum_address("0x" + proxy_impl_address[-40:])
        except Exception as e:
            if type(e) == ContractLogicError or type(e) == BadFunctionCallOutput:
                pass

    # Query Scans to get the Implementation Address
    if proxy_impl_address == Address.ZERO:
        proxy_impl_address = ChainExplorer(blockchain).get_impl_address(contract_address)

    return proxy_impl_address


def get_abi_function_signatures(contract_address, blockchain, web3=None, abi_address=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain)

    contract_address = Web3.to_checksum_address(contract_address)

    if abi_address is None:
        proxy_impl_address = search_proxy_impl_address(contract_address, blockchain, web3=web3, block=block)
        contract = get_contract_proxy_abi(contract_address, proxy_impl_address, blockchain, web3=web3)
    else:
        contract = get_contract_proxy_abi(contract_address, abi_address, blockchain, web3=web3, block=block)

    if contract is not None:
        abi = contract.abi

        functions = []
        for func in [obj for obj in abi if obj["type"] == "function"]:
            name = func["name"]
            input_types = [input["type"] for input in func["inputs"]]

            function = {}
            function["name"] = name
            function["signature"] = "{}{}".format(name, "(")
            function["inline_signature"] = "{}{}".format(name, "(")
            function["components"] = []
            function["stateMutability"] = func["stateMutability"]

            i = 0
            for input_type in input_types:
                if input_type == "tuple":
                    function["components"] = [component["type"] for component in func["inputs"][i]["components"]]
                    function["inline_signature"] += "({})".format(",".join(function["components"]))
                else:
                    function["inline_signature"] += input_type
                    function["components"].append(input_type)

                function["signature"] += input_type

                if i < len(input_types) - 1:
                    function["signature"] += ","
                    function["inline_signature"] += ","

                i += 1

            function["signature"] += ")"
            function["inline_signature"] += ")"

            functions.append(function)

        return functions

    return None


def get_data(contract_address, function_name, parameters, blockchain, web3=None, abi_address=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain)

    contract_address = Web3.to_checksum_address(contract_address)

    contract = None

    if abi_address is None:
        contract = get_contract(contract_address, blockchain, web3=web3)

        if contract is not None:
            try:
                getattr(contract.functions, function_name)
            except ABIFunctionNotFound:
                # If the contract does not have the function, it checks if there is a proxy implementation
                proxy_impl_address = search_proxy_impl_address(contract_address, blockchain, web3=web3, block=block)

                if proxy_impl_address != Address.ZERO:
                    contract = get_contract_proxy_abi(contract_address, proxy_impl_address, blockchain, web3=web3)
    else:
        contract = get_contract_proxy_abi(contract_address, abi_address, blockchain, web3=web3)

    try:
        return contract.encodeABI(fn_name=function_name, args=parameters)
    except Exception:
        logger.exception("Exception in get_data")
        return None


# LOGS
def get_block_intervals(blockchain, block_start, block_end, block_interval):
    block_interval = block_end if block_interval is None else block_interval

    if block_end == "latest":
        web3 = get_node(blockchain)
        block_end = web3.eth.block_number

    n_blocks = list(range(block_start, block_end + 1, block_interval))
    n_blocks += [] if ((block_end - block_start) / block_interval) % 1 == 0 else [block_end]

    return list(zip(n_blocks[:-1], n_blocks[1:]))


# get_logs_web3
def get_logs_web3(
    blockchain: str,
    tx_hash: str = None,
    address: str = None,
    block_start: int | str = None,
    block_end: int | str = "latest",
    topics: list = None,
    block_hash: str = None,
    web3: Web3 = None,
) -> dict:
    # FIXME: Add documentation
    if web3 is None:
        web3 = get_node(blockchain, block=block_end)
    try:
        params = {}
        if address is not None:
            address = Web3.to_checksum_address(address)
            params.update({"address": address})
        if topics is not None:
            params.update({"topics": topics})
        if tx_hash is not None:
            params.update({"transactionHash": tx_hash})
        elif block_hash is not None:
            params.update({"blockHash": block_hash})
        elif block_start is not None:
            params.update({"fromBlock": block_start})
            if block_end != "latest":
                params.update({"toBlock": block_end})
        logs = web3.eth.get_logs(params)
        if not isinstance(block_end, str):
            for n in range(len(logs)):
                if logs[n]["blockNumber"] > block_end:
                    logs = logs[:n]
                    break
    except ValueError as error:
        error_info = error.args[0]
        if error_info["code"] == -32005:  # error code in infura
            block_interval = int(error_info["data"]["to"], 16) - int(error_info["data"]["from"], 16)
        elif "max_block_range" in error_info:  # error code in Quicknode, see ProviderManager class
            block_interval = error_info["max_block_range"]
        elif error_info["code"] == -32602:  # error code in alchemy
            blocks = [int(block, 16) for block in re.findall(r"0x[0-9a-fA-F]+", error_info["message"])]
            block_interval = blocks[1] - blocks[0]
        elif error_info["code"] == -32600:  # error code in anker: "block range is too wide"
            block_interval = 3000
        else:
            raise ValueError(error_info)
        logger.debug(
            f"Web3.eth.get_logs: query returned more than 10000 results. Trying with a {block_interval} block range."
        )
        logs = []
        params = {"address": address, "topics": topics}
        if block_hash is not None:
            params.update({"blockHash": block_hash})
        for from_block, to_block in get_block_intervals(blockchain, block_start, block_end, block_interval):
            params.update({"fromBlock": from_block, "toBlock": to_block})
            logs += web3.eth.get_logs(params)
    return logs


# get_4byte_signature
def get_4byte_signature(hex_signature: str) -> list:
    API_4BYTE_DIRECTORY_SIGNATURES = "https://www.4byte.directory/api/v1/signatures/?hex_signature=%s"
    results = []

    data = requests.get(API_4BYTE_DIRECTORY_SIGNATURES % (hex_signature)).json()["results"]

    if len(data) > 0:
        for result in data:
            results.append(result["text_signature"])

    return results


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def is_archival(endpoint) -> bool:
    """
    Checks whether a node is an archival node or a full node.

    :param str endpoint: The node's RPC endpoint to analyse
    :return: True if the node is archival, False if it isn't
    """

    web3 = Web3(Web3.HTTPProvider(endpoint))

    try:
        web3.eth.get_balance("0x849D52316331967b6fF1198e5E32A0eB168D039d", block_identifier=1)
    except ValueError:
        return False
    return True
