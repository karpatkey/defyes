from dataclasses import dataclass

from web3 import Web3

from defyes.functions import get_node


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
