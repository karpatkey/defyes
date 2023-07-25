from dataclasses import dataclass, field
from typing import Optional

import requests
from web3 import Web3

from defyes.explorers import Explorer
from defyes.node import get_node


@dataclass
class ImplContractData:
    proxy_address: str
    blockchain: str

    def __post_init__(self):
        self.web3 = get_node(self.blockchain)
        self.bytecode_contract = self.web3.eth.get_code(self.proxy_address).hex()

    def get_impl_contract(self):
        bytecode = self.web3.eth.get_code(self.proxy_address).hex()
        # Check for EIP-1167 proxy implementation
        if bytecode[2:22] == "363d3d373d3d3d363d73" and bytecode[62:] == "5af43d82803e903d91602b57fd5bf3":
            return "0x" + bytecode[22:62]
        hash_value = Web3.keccak(text="eip1967.proxy.implementation")
        impl_slot = (int.from_bytes(hash_value, byteorder="big") - 1).to_bytes(32, byteorder="big")
        impl_contract = (
            "0x"
            + Web3.to_hex(
                self.web3.eth.get_storage_at(
                    self.proxy_address,
                    impl_slot.hex(),
                )
            )[-40:]
        )
        impl_function = Web3.keccak(text="implementation()")[:4].hex()[2:]
        # FIXME: this is not a correct way to identify EIP-1967 proxy contracts
        if len(self.bytecode_contract) >= 1000:
            return self.proxy_address
        elif len(self.bytecode_contract) < 150:
            return "0x" + self.bytecode_contract[32:72]
        elif impl_function in self.bytecode_contract:
            contract_abi = '[{"constant":true,"inputs":[],"name":"implementation","outputs":[{"name":"impl","type":"address"}],"payable":false,"stateMutability":"view","type":"function"}]'
            contract_instance = self.web3.eth.contract(self.proxy_address, abi=contract_abi)
            impl_call = contract_instance.functions.implementation().call()
            return impl_call
        elif impl_contract == "0x0000000000000000000000000000000000000000":
            safe_impl_contract = "0x" + Web3.to_hex(self.web3.eth.get_storage_at(self.proxy_address, 0))[-40:]
            return safe_impl_contract
        else:
            return impl_contract


@dataclass
class RequestFromScan:
    module: str
    action: str
    blockchain: Optional[str] = None
    apikey: Optional[str] = None
    kwargs: field(default_factory=dict) = None

    def __post_init__(self):
        self.apikey = Explorer(self.blockchain).get_private_key()
        self.get_impl_contract_if_account()
        self.blockchain = Explorer(self.blockchain).get_explorer()
        [setattr(self, k, v) for k, v in self.kwargs.items()]

    def get_impl_contract_if_account(self):
        if "address" in self.kwargs:
            address = self.kwargs["address"]
            impl_data = ImplContractData(proxy_address=address, blockchain=self.blockchain)
            impl_contract = impl_data.get_impl_contract()
            self.kwargs["address"] = impl_contract

    def make_request(self):
        params = {k: v for k, v in self.__dict__.items() if k != "kwargs"}
        return params

    def request(self):
        request = requests.get(
            "https://api.{}/api?".format(self.blockchain),
            params={k: v for k, v in self.__dict__.items() if k != "kwargs"},
        ).json()
        return request