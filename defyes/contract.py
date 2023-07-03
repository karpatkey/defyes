import json

from web3 import Web3
from web3.contract import Contract

from defyes.cache import const_call
from defyes.functions import get_node


class ContractFunction:
    def __init__(self, attr, args, kwargs, get_contract_func):
        self.attr = attr
        self.args = args
        self.kwargs = kwargs
        self.get_contract = get_contract_func

    def _get_contract_func(self, attr, *args, **kwargs):
        block = kwargs.get("block_identifier", "latest")
        contract = self.get_contract(block)
        contract_func = getattr(contract.functions, attr)
        return contract_func

    def call(self, *args, **kwargs):
        contract_func = self._get_contract_func(self.attr, *args, **kwargs)
        return contract_func(*self.args, **self.kwargs).call(*args, **kwargs)

    def const_call(self, *args, **kwargs):
        contract_func = self._get_contract_func(self.attr, *args, **kwargs)
        return const_call(contract_func(*self.args, **self.kwargs))


class DefiContract:
    ABI: str = "MUST_BE_DEFINED"

    def __init__(self, blockchain: str, address: str) -> None:
        self.blockchain = blockchain
        self.address = Web3.to_checksum_address(address)
        self.node = None
        self.contract = None

        for method_name in [func["name"] for func in json.loads(self.ABI)]:
            setattr(self, method_name, self.create_method(method_name))

    def create_method(self, method_name):
        def method(*args, **kwargs):
            return ContractFunction(method_name, args, kwargs, get_contract_func=self.get_contract)

        return method

    def must_update(self, block) -> None:
        return self.node is None or block != self.node._called_with_block

    def get_node(self, block) -> Web3:
        if self.must_update(block):
            self.node = get_node(self.blockchain, block)
        return self.node

    def get_contract(self, block) -> Contract:
        if self.must_update(block) or self.contract is None:
            self.node = get_node(self.blockchain, block)
            self.contract = self.node.eth.contract(address=self.address, abi=self.ABI)
        return self.contract
