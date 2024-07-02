import json
import logging
import math
import re
from contextlib import suppress
from datetime import datetime
from decimal import Decimal
from typing import List, Tuple

import requests
from defabipedia import Blockchain, Chain
from hexbytes import HexBytes
from karpatkit.api_services import APIKey
from karpatkit.cache import cache_call, const_call
from karpatkit.constants import ABI_TOKEN_SIMPLIFIED, Address
from karpatkit.explorer import ChainExplorer
from karpatkit.helpers import suppress_error_codes
from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import ABIFunctionNotFound, BadFunctionCallOutput, ContractLogicError
from web3.types import LogReceipt

from defyes.lazytime import Time

logger = logging.getLogger(__name__)


# CUSTOM EXCEPTIONS
class BlockchainError(Exception):
    pass


def tz_aware(dt):
    return dt.tzinfo is not None and dt.tzinfo.utcoffset(dt) is not None


def to_token_amount(
    token_address: str, amount: int | Decimal, blockchain: str, web3: Web3 = None, decimals: bool = True
) -> Decimal:
    """
    Converts the given amount to the corresponding token amount based on the token's decimals.

    Args:
        token_address (str): The address of the token.
        amount (int | Decimal): The amount to be converted.
        blockchain (str): The blockchain on which the token exists.
        web3 (Web3, optional): The Web3 instance to use for blockchain interactions. Defaults to None.
        decimals (bool, optional): Whether to fetch the token's decimals from the blockchain. Defaults to True.
            In case False, decimals are assumed to be 0.

    Returns:
        Decimal: The converted token amount.
    """
    decimals = get_decimals(token_address, blockchain=blockchain, web3=web3) if decimals else 0
    return amount / Decimal(10**decimals)


def last_block(blockchain, web3=None):
    """
    Returns the number of the last block in the blockchain.
    """
    if web3 is None:
        web3 = get_node(blockchain)

    return web3.eth.block_number


def ensure_a_block_number(block: int | str, blockchain: Blockchain):
    """Ensures that the provided block number is valid.

    Args:
        block (int | str): The block number or the string 'latest'.
        blockchain (Blockchain): The blockchain object.

    Returns:
        int: The validated block number.

    Raises:
        ValueError: If the block is not an integer or the string 'latest'.
    """
    if isinstance(block, int):
        return block
    elif block == "latest":
        return last_block(blockchain)
    else:
        raise ValueError("block should be an integer or just the string 'latest'")


def date_to_block(datestring, blockchain) -> int:
    """
    Returns the block number of a specified date.

    The date can be a string (in the format '%Y-%m-%d %H:%M:%S') or a datetime object. UTC is asumed as timezone.
    An example datestring: '2023-02-20 18:30:00'.
    """
    if isinstance(datestring, datetime):
        if not tz_aware(datestring):
            raise ValueError("Naive datetimes are unsupported.")
        timestamp = datestring.timestamp()
    else:
        timestamp = Time.from_string(datestring)
    return timestamp_to_block(timestamp, blockchain)


def timestamp_to_block(timestamp: int, blockchain) -> int:
    """Converts a timestamp (Unix epoch) to a block number. (int)"""
    return ChainExplorer(blockchain).block_from_time(timestamp)


def block_to_date(block, blockchain):
    """Converts a block number to a date string."""
    return str(Time(ChainExplorer(blockchain).time_from_block(block)))


def get_blocks_per_year(blockchain):
    """Calculates the number of blocks per year in the blockchain."""
    current_block = last_block(blockchain)
    ts = math.floor(datetime.now().timestamp()) - (3600 * 24 * 365)
    block = ChainExplorer(blockchain).block_from_time(ts)

    block_delta = current_block - block

    return block_delta


# ERC20 TOKENS
# token_info
@cache_call()
def token_info(token_address, blockchain):
    ETHPLORER_URL = "https://api.ethplorer.io/getTokenInfo/%s?apiKey=%s"
    BLOCKSCOUT_URL = "https://blockscout.com/xdai/mainnet/api?module=token&action=getToken&contractaddress=%s"

    if blockchain.lower() == Chain.ETHEREUM:
        data = requests.get(ETHPLORER_URL % (token_address, APIKey.ETHPLORER)).json()

    elif blockchain.lower() == Chain.GNOSIS:
        data = requests.get(BLOCKSCOUT_URL % token_address).json()["result"]

    return data


def balance_of(
    address: str, contract_address: str, block: int | str, blockchain: str, web3=None, decimals: bool = True
) -> Decimal:
    """
    Get the balance of an address for a given contract on a specific block in a blockchain.

    Args:
        address (str): The address (wallet) for which to retrieve the balance.
        contract_address (str): The address of the contract (Token or ERC20) for which to retrieve the balance.
        block (int | str): The block number or block identifier.
        blockchain (str): The name of the blockchain.
        web3 (Web3, optional): The Web3 instance to use. If not provided, a default instance will be used.
        decimals (bool, optional): Whether to convert the balance to token decimals. Defaults to True.

    Returns:
        Decimal: The balance of the address in the specified contract.
    """
    if web3 is None:
        web3 = get_node(blockchain)

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
    """Retrieves the total supply of a token at a specific block."""
    if web3 is None:
        web3 = get_node(blockchain)

    token_address = Web3.to_checksum_address(token_address)

    token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
    total_supply_v = token_contract.functions.totalSupply().call(block_identifier=block)

    return to_token_amount(token_address, total_supply_v, blockchain, web3, decimals)


def get_decimals(token_address: str, blockchain: str | Blockchain, web3=None) -> int:
    """Get the number of decimals for a given token address."""
    if web3 is None:
        web3 = get_node(blockchain)

    token_address = Web3.to_checksum_address(token_address)

    if token_address == Address.ZERO or token_address == Address.E:
        decimals = 18
    else:
        token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
        decimals = const_call(token_contract.functions.decimals())

    return decimals


def get_symbol(token_address: str, blockchain: str | Blockchain, web3=None) -> str:
    token_address = Web3.to_checksum_address(token_address)

    if web3 is None:
        web3 = get_node(blockchain)

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
def get_contract(contract_address, blockchain, web3=None, abi=None):
    """
    Retrieves a contract instance from the specified blockchain using the contract address and ABI.

    Args:
        contract_address (str): The address of the contract on the blockchain.
        blockchain (str): The name of the blockchain network.
        web3 (Web3, optional): An instance of the Web3 class. If not provided, a default instance will be used.
        abi (list, optional): The ABI (Application Binary Interface) of the contract.
            If not provided, it will be fetched from the blockchain explorer.

    Returns:
        Contract: An instance of the contract.

    """
    if web3 is None:
        web3 = get_node(blockchain)

    contract_address = Web3.to_checksum_address(contract_address)

    if abi is None:
        abi = ChainExplorer(blockchain).abi_from_address(contract_address)
        return web3.eth.contract(address=contract_address, abi=abi)
    else:
        return web3.eth.contract(address=contract_address, abi=abi)


def get_contract_proxy_abi(contract_address: str, abi_contract_address: str, blockchain: str | Blockchain, web3=None):
    """Retrieves the contract proxy ABI for a given contract address and ABI contract address.

    Args:
        contract_address (str): The address of the contract.
        abi_contract_address (str): The address of the ABI contract. (Implementation contract)
        blockchain (str): The name of the blockchain.
        web3 (Web3, optional): An instance of the Web3 class. If not provided, a default instance will be used.

    Returns:
        Contract: An instance of the contract proxy with the specified address and ABI.
    """
    if web3 is None:
        web3 = get_node(blockchain)

    address = Web3.to_checksum_address(contract_address)

    abi = ChainExplorer(blockchain).abi_from_address(abi_contract_address)
    return web3.eth.contract(address=address, abi=abi)


def format_address(address: str | bytes) -> str:
    """
    Formats the given Ethereum address. It converts the address to a checksum address.

    Example:
        address = "0x0000000000000000000000006bd780e7fdf01d77e4d475c821f1e7ae05409072"
        formatted_address = format_address(address)
        print(formatted_address)
        # Output: 0x5aAeb6053F3E94C9b9A09f33669435E7Ef1BeAed
    """
    if isinstance(address, str) and address.startswith("0x"):
        # If the address is already a hex string, skip the to_hex conversion
        hex_address = address
    else:
        hex_address = Web3.to_hex(address)

    return Web3.to_checksum_address("0x" + hex_address[-40:])


def get_impl_latest(web3, contract_address, block):
    if isinstance(block, str) and block == "latest":
        return ChainExplorer(web3._network_name).get_impl_address(contract_address)
    return Address.ZERO


def get_impl_1967(web3, contract_address, block):
    impl_address = Address.ZERO
    IMPLEMENTATION_SLOT = "0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc"
    impl_address = web3.eth.get_storage_at(contract_address, IMPLEMENTATION_SLOT, block_identifier=block)
    return format_address(impl_address)


def get_impl_1167_0(web3, contract_address, block):
    # OpenZeppelins' EIP-1167 - Example in GC: 0x793fAF861a78B07c0C8c0ed1450D3919F3473226)
    impl_address = Address.ZERO
    bytecode = web3.eth.get_code(contract_address, block_identifier=block).hex()
    if bytecode[2:22] == "363d3d373d3d3d363d73" and bytecode[62:] == "5af43d82803e903d91602b57fd5bf3":
        impl_address = Web3.to_checksum_address("0x" + bytecode[22:62])
    return impl_address


def get_impl_1167_1(web3, contract_address, block):
    # Custom proxy implementation (similar to EIP-1167) -
    # Examples: mainnet: 0x09cabEC1eAd1c0Ba254B09efb3EE13841712bE14 / GC: 0x7B7DA887E0c18e631e175532C06221761Db30A24
    impl_address = Address.ZERO
    bytecode = web3.eth.get_code(contract_address, block_identifier=block).hex()
    if bytecode[2:32] == "366000600037611000600036600073" and bytecode[72:] == "5af41558576110006000f3":
        impl_address = Web3.to_checksum_address("0x" + bytecode[32:72])
    return impl_address


def get_impl_storage_proxy(web3, contract_address, block):
    # OpenZeppelins' Unstructured Storage proxy pattern - Example: USDC in mainnet (0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48)
    impl_address = Address.ZERO
    IMPLEMENTATION_SLOT_UNSTRUCTURED = "0x7050c9e0f4ca769c69bd3a8ef740bc37934f8e2c036e5a723fd8ee048ed3f8c3"
    impl_address = web3.eth.get_storage_at(contract_address, IMPLEMENTATION_SLOT_UNSTRUCTURED, block_identifier=block)
    return format_address(impl_address)


def get_impl_897(web3, contract_address, block):
    # OpenZeppelins' EIP-897 DelegateProxy - Examples: stETH in mainnet (0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84)
    # It also includes the custom proxy implementation of the Comptroller: 0x3d9819210A31b4961b30EF54bE2aeD79B9c9Cd3B
    impl_address = Address.ZERO
    contract = None
    with suppress(ContractLogicError, BadFunctionCallOutput), suppress_error_codes():
        contract = get_contract(contract_address, web3._network_name, web3=web3)

    if contract is not None:
        for func in [obj for obj in contract.abi if obj["type"] == "function"]:
            name = str(func["name"].lower())
            if "implementation" in name:
                output_types = [output["type"] for output in func["outputs"]]
                if output_types == ["address"]:
                    try:
                        impl_address_func = getattr(contract.functions, func["name"])
                        impl_address = impl_address_func().call(block_identifier=block)
                        break
                    except (ContractLogicError, BadFunctionCallOutput):
                        continue
    return impl_address


def get_impl_custom_proxy(web3, contract_address, block):
    # Custom proxy implementation (used by Safes) - Example: mainnet: 0x4F2083f5fBede34C2714aFfb3105539775f7FE64
    impl_address = Address.ZERO
    contract_custom_abi = get_contract(
        contract_address,
        web3._network_name,
        abi='[{"inputs":[{"internalType":"uint256","name":"offset","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"getStorageAt","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"}]',
    )
    try:
        impl_address = contract_custom_abi.functions.getStorageAt(0, 1).call(block_identifier=block)
        impl_address = format_address(impl_address)
    except (ContractLogicError, BadFunctionCallOutput):
        pass
    return impl_address


def search_proxy_impl_address(contract_address, blockchain, web3=None, block="latest"):
    if web3 is None:
        web3 = get_node(blockchain)

    contract_address = Web3.to_checksum_address(contract_address)

    proxy_impl_funcs = [
        get_impl_latest,
        get_impl_1967,
        get_impl_1167_0,
        get_impl_1167_1,
        get_impl_storage_proxy,
        get_impl_897,
        get_impl_custom_proxy,
    ]
    for func in proxy_impl_funcs:
        proxy_impl_address = func(web3, contract_address, block)
        if proxy_impl_address != Address.ZERO:
            return proxy_impl_address

    return Address.ZERO


def get_abi_function_signatures(
    contract_address, blockchain, web3=None, abi_address=None, block="latest", func_names=None
):
    if web3 is None:
        web3 = get_node(blockchain)

    contract_address = Web3.to_checksum_address(contract_address)

    if abi_address is None:
        abi_address = search_proxy_impl_address(contract_address, blockchain, web3=web3, block=block)

    if abi_address == Address.ZERO:
        contract = get_contract(contract_address, blockchain, web3=web3)
    else:
        contract = get_contract_proxy_abi(contract_address, abi_address, blockchain, web3=web3)

    if contract is not None:
        abi = contract.abi

        functions = []
        for func in [obj for obj in abi if obj["type"] == "function"]:
            if func_names and func["name"] not in func_names:
                continue
            else:
                name = func["name"]
                input_types = [input["type"] for input in func["inputs"]]
                input_names = [input["name"] for input in func["inputs"]]

                function = {}
                function["name"] = name
                function["signature"] = "{}{}".format(name, "(")
                function["inline_signature"] = "{}{}".format(name, "(")
                function["components"] = []
                function["components_names"] = []
                function["stateMutability"] = func["stateMutability"]

                i = 0
                for input_type in input_types:
                    if input_type == "tuple" or input_type == "tuple[]":
                        function["components"] += [component["type"] for component in func["inputs"][i]["components"]]
                        function["components_names"] += [
                            component["name"] for component in func["inputs"][i]["components"]
                        ]
                        function["inline_signature"] += "({})".format(",".join(function["components"]))
                    else:
                        function["inline_signature"] += input_type
                        function["components"].append(input_type)
                        function["components_names"].append(input_names[i])

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


def get_block_intervals(
    blockchain: str, block_start: int, block_end: int, block_interval: int
) -> List[Tuple[int, int]]:
    """Function used by get_logs_web3 to get the block intervals.
    It returns a list of tuples with the start and end block numbers of each interval.
    """
    block_interval = block_end if block_interval is None else block_interval

    if block_end == "latest":
        web3 = get_node(blockchain)
        block_end = web3.eth.block_number

    n_blocks = list(range(block_start, block_end + 1, block_interval))
    n_blocks += [] if ((block_end - block_start) / block_interval) % 1 == 0 else [block_end]

    return list(zip(n_blocks[:-1], n_blocks[1:]))


def prepare_log_params(address, topics, tx_hash, block_hash, block_start, block_end):
    """Function used by get_logs_web3 to prepare the parameters for fetching logs."""
    params = {}
    if address:
        params["address"] = Web3.to_checksum_address(address)
    if topics:
        params["topics"] = topics
    if tx_hash:
        params["transactionHash"] = tx_hash
    elif block_hash:
        params["blockHash"] = block_hash
    elif block_start:
        params["fromBlock"] = block_start
        if block_end != "latest":
            params["toBlock"] = block_end
    return params


def get_logs_from_transaction(tx_receipt: dict, address: str = None, topics: list[str] = None) -> list[LogReceipt]:
    """
    Retrieves logs from a transaction receipt.

    Args:
        tx_receipt (dict): The transaction receipt containing logs.
        address (str, optional): The address to filter logs by. Defaults to None.
        topics (list[str], optional): The topics to filter logs by. Defaults to None.

    Returns:
        list[LogReceipt]: The filtered logs from the transaction receipt.
    """
    tx_logs = tx_receipt.get("logs", [])
    logs = []
    for log in tx_logs:
        if address is not None and log.get("address") != address:
            continue
        if topics is not None and not all(HexBytes(topic) in log.get("topics", []) for topic in topics):
            continue
        logs.append(log)
    return logs


def get_logs_web3(
    blockchain: str,
    tx_hash: str = None,
    address: str = None,
    block_start: int | str = None,
    block_end: int | str = "latest",
    topics: list = None,
    block_hash: str = None,
    web3: Web3 = None,
) -> list[LogReceipt]:
    """
    Fetches logs from a specified blockchain using the Web3 library.
    You can fetch logs from a specific transaction, contract address, block range, or block hash.
    Some arguments are optional, but one of `tx_hash`, `address`, `block_start`, or `block_hash` must be provided.
    If `tx_hash` is provided, the function fetches the logs from the transaction receipt.
    If `address` is provided, the function fetches the logs from the specified contract.
    If `block_start` and `block_end` are provided, the function fetches logs from the specified block range.

    Args:
        blockchain (str): The name of the blockchain from which to fetch logs.
        tx_hash (str, optional): The transaction hash. Fetches the receipt of this transaction and extracts its logs.
        address (str, optional): The address of the contract for which to fetch logs.
        block_start (int | str, optional): The start block number or block hash.
        block_end (int | str, optional): The end block number. If not provided, fetches logs until the latest block.
        topics (list, optional): The topics of the logs to fetch. If not provided, fetches all logs.
        block_hash (str, optional): The hash of a specific block from which to fetch logs.
        web3 (Web3, optional): An instance of the Web3 class.

    Returns:
        list[LogReceipt]: The fetched logs.
    """
    # Check if tx_hash is used with block_start, block_end or block_hash
    if tx_hash and (block_start or block_end != "latest" or block_hash):
        raise ValueError("tx_hash cannot be used with block_start, block_end or block_hash")

    if web3 is None:
        web3 = get_node(blockchain)

    if tx_hash:
        # Get transaction receipt
        tx_receipt = web3.eth.get_transaction_receipt(tx_hash)
        if tx_receipt is None:
            return []
        # Get logs from the transaction receipt
        logs = get_logs_from_transaction(tx_receipt, address, topics)
    else:
        try:
            # Prepare the parameters for fetching logs
            params = prepare_log_params(address, topics, tx_hash, block_hash, block_start, block_end)
            # Fetch the logs
            logs = web3.eth.get_logs(params)
            # If block_end is not a string, trim the logs to the block range
            if not isinstance(block_end, str):
                for n in range(len(logs)):
                    if logs[n]["blockNumber"] > block_end:
                        logs = logs[:n]
                        break
        except ValueError as error:
            # Handle ValueError by adjusting the block range and retrying
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
            # Log the error and the new block range
            logger.debug(
                f"Web3.eth.get_logs: query returned more than 10000 results. Trying with a {block_interval} block range."
            )
            # Retry fetching the logs with the new block range
            logs = []
            params = {"address": address, "topics": topics}
            if block_hash is not None:
                params.update({"blockHash": block_hash})
            for from_block, to_block in get_block_intervals(blockchain, block_start, block_end, block_interval):
                params.update({"fromBlock": from_block, "toBlock": to_block})
                logs += web3.eth.get_logs(params)
    return logs


def get_4byte_signature(hex_signature: str) -> list:
    """
    Retrieves the text signatures associated with a given hexadecimal signature from the 4byte.directory API.
    More information: https://www.4byte.directory/

    Args:
        hex_signature (str): The hexadecimal signature to search for.

    Returns:
        list: A list of text signatures associated with the given hexadecimal signature.
    """
    API_4BYTE_DIRECTORY_SIGNATURES = "https://www.4byte.directory/api/v1/signatures/?hex_signature=%s"
    results = []

    data = requests.get(API_4BYTE_DIRECTORY_SIGNATURES % (hex_signature)).json()["results"]

    if len(data) > 0:
        for result in data:
            results.append(result["text_signature"])

    return results


def is_archival(endpoint) -> bool:
    """
    Checks whether a node is an archival node or a full node.

    Args:
        endpoint (str): The node's RPC endpoint to analyze.

    Returns:
        bool: True if the node is archival, False if it isn't.
    """
    web3 = Web3(Web3.HTTPProvider(endpoint))

    try:
        web3.eth.get_balance("0x849D52316331967b6fF1198e5E32A0eB168D039d", block_identifier=1)
    except ValueError:
        return False
    return True
