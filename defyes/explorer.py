import time

import requests
from web3 import Web3

from defyes.cache import cache_call
from defyes.constants import TESTNET_CHAINS, Address, APIKey, APIUrl, Chain
from defyes.node import get_node

TESTNET_HEADER = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Mobile Safari/537.36"
}

EXPLORERS = {
    Chain.ETHEREUM: (APIUrl.ETHERSCAN, APIKey.ETHERSCAN),
    Chain.POLYGON: (APIUrl.POLSCAN, APIKey.POLSCAN),
    Chain.GNOSIS: (APIUrl.GNOSISSCAN, APIKey.GNOSISSCAN),
    Chain.BINANCE: (APIUrl.BINANCE, APIKey.BINANCE),
    Chain.AVALANCHE: (APIUrl.AVALANCHE, APIKey.AVALANCHE),
    Chain.FANTOM: (APIUrl.FANTOM, APIKey.FANTOM),
    Chain.ARBITRUM: (APIUrl.ARBITRUM, APIKey.ARBITRUM),
    Chain.OPTIMISM: (APIUrl.OPTIMISM, APIKey.OPTIMISM),
    Chain.ROPSTEN: (APIUrl.ROPSTEN, APIKey.ETHERSCAN),
    Chain.KOVAN: (APIUrl.KOVAN, APIKey.ETHERSCAN),
    Chain.GOERLI: (APIUrl.GOERLI, APIKey.ETHERSCAN),
}


def get_implemented_contract(blockchain, proxy_address):
    proxy_address = Web3.to_checksum_address(proxy_address)
    node = get_node(blockchain)
    bytecode = node.eth.get_code(proxy_address).hex()

    # Check for EIP-1167 proxy implementation
    if bytecode[2:22] == "363d3d373d3d3d363d73" and bytecode[62:] == "5af43d82803e903d91602b57fd5bf3":
        return "0x" + bytecode[22:62]
    hash_value = Web3.keccak(text="eip1967.proxy.implementation")
    impl_slot = (int.from_bytes(hash_value, byteorder="big") - 1).to_bytes(32, byteorder="big")
    impl_contract = (
        "0x"
        + Web3.to_hex(
            node.eth.get_storage_at(
                proxy_address,
                impl_slot.hex(),
            )
        )[-40:]
    )
    impl_function = Web3.keccak(text="implementation()")[:4].hex()[2:]

    # FIXME: this is not a correct way to identify EIP-1967 proxy contracts
    if len(bytecode) >= 1000:
        return proxy_address
    elif len(bytecode) < 150:
        return "0x" + bytecode[32:72]
    elif impl_function in bytecode:
        contract_abi = '[{"constant":true,"inputs":[],"name":"implementation","outputs":[{"name":"impl","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'
        contract_instance = node.eth.contract(proxy_address, abi=contract_abi)
        impl_call = contract_instance.functions.implementation().call()
        return impl_call
    elif impl_contract == "0x0000000000000000000000000000000000000000":
        safe_impl_contract = "0x" + Web3.to_hex(node.eth.get_storage_at(proxy_address, 0))[-40:]
        return safe_impl_contract
    else:
        return impl_contract


class ChainExplorer(requests.Session):
    def __init__(self, blockchain: str = None) -> None:
        super().__init__()
        self.chain = blockchain
        if blockchain in TESTNET_CHAINS:
            self.headers.update(TESTNET_HEADER)
        domain, apikey = EXPLORERS[blockchain]
        self.params["apikey"] = apikey
        self.url = f"https://{domain}/api"

    def _get(self, **params):
        response = self.request("GET", self.url, params=params)
        response.raise_for_status()
        return response

    cached = cache_call(
        exclude_args=["self"],
        filter=lambda args: "latest" not in args,
        include_attrs=[
            lambda self: self.__class__.__name__,
            lambda self: self.chain,
        ],
    )

    @cached
    def block_closest_to(self, timestamp: int, closest: str) -> int:
        response = self._get(module="block", action="getblocknobytime", closest=closest, timestamp=int(timestamp))
        block_id = response.json()["result"]
        try:
            return int(block_id)
        except (TypeError, ValueError):
            return block_id

    def block_after(self, timestamp):
        return self.block_closest_to(timestamp, closest="after")

    def block_before(self, timestamp):
        return self.block_closest_to(timestamp, closest="before")

    block_from_time = block_before

    @cached
    def time_from_block(self, block: int | str) -> int:
        if isinstance(block, str):
            if block == "latest":
                return int(time.time())

        response = self._get(module="block", action="getblockreward", blockno=block)
        timestamp = response.json()["result"]["timeStamp"]
        try:
            return int(timestamp)
        except (TypeError, ValueError):
            return timestamp

    @cached
    def abi_from_address(self, contract_address: str) -> str:
        contract_address = get_implemented_contract(self.chain, contract_address)
        response = self._get(module="contract", action="getabi", address=contract_address)
        abi = response.json()["result"]
        if abi == "Contract source code not verified":
            raise ValueError("ABI not verified.")
        return abi

    @cached
    def get_contract_creation(self, contract_address: str) -> dict:
        if self.chain != Chain.ETHEREUM:
            raise ValueError("Chain should be ethereum for this method")
        contract_address = get_implemented_contract(self.chain, contract_address)
        response = self._get(module="contract", action="getcontractcreation", contractaddresses=contract_address)
        contract = response.json()["result"]
        return contract

    @cached
    def get_logs(
        self, contract_address: str, from_block: int, to_block: int, topic: str, optional_params: dict = {}
    ) -> list:
        KEYS_WHITELIST = [
            "topic1",
            "topic2",
            "topic3",
            "topic0_1_opr",
            "topic0_2_opr",
            "topic0_3_opr",
            "topic1_2_opr",
            "topic1_3_opr" "topic2_3_opr",
        ]
        contract_address = get_implemented_contract(self.chain, contract_address)
        for key, value in optional_params.items():
            if key in KEYS_WHITELIST and value:
                self.params[key] = value
        response = self._get(
            module="logs",
            action="getLogs",
            fromBlock=from_block,
            toBlock=to_block,
            addresse=contract_address,
            topic0=topic,
        )
        logs = response.json()["result"]
        return logs

    @cached
    def get_transactions(self, contract_address: str, block_start: int, block_end: int) -> list:
        response = self._get(
            module="account",
            action="txlist",
            address=contract_address,
            startblock=block_start,
            endblock=block_end,
            sort="desc",
        )
        txs = response.json()["result"]
        return txs

    @cached
    def get_token_transactions(
        self, token_address: str, contract_address: str, block_start: str, block_end: str
    ) -> list:
        response = self._get(
            module="account",
            action="tokentx",
            contractaddress=token_address,
            address=contract_address,
            strarblock=block_start,
            endblock=block_end,
            sort="desc",
        )
        txs = response.json()["result"]
        return txs

    @cached
    def get_etherscan_price(self, token_address: str):
        if self.chain != Chain.ETHEREUM:
            raise ValueError("Chain should be ethereum for this method")
        response = self._get(module="token", action="tokeninfo", contractaddresses=token_address)
        price_usd = response.json()["result"][0]["tokenPriceUSD"]

        return price_usd

    @cached
    def get_impl_address(self, address: str):
        implementation_address = Address.ZERO
        response = self._get(module="contract", action="getsourcecode", address=address)
        data = response.json()
        if data["message"] == "OK" and data["result"][0]["Implementation"] != "":
            implementation_address = data["result"][0]["Implementation"]
            if Web3.is_address(implementation_address):
                implementation_address = Web3.to_checksum_address(implementation_address)

        return implementation_address

    @cached
    def get_contract_name(self, address: str):
        contract_name = ""
        response = self._get(module="contract", action="getsourcecode", address=address)
        data = response.json()
        if data["message"] == "OK" and data["result"][0]["ContractName"] != "":
            contract_name = data["result"][0]["ContractName"]

        return contract_name
