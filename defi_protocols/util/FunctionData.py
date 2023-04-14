from typing import Optional, Union
from dataclasses import dataclass
from time import sleep
import json

from web3 import Web3
from web3._utils.abi import get_abi_input_types, filter_by_name
from eth_abi import encode_abi

from defi_protocols.util.api import RequestFromScan
from defi_protocols.constants import SAFETRANSACTIONWITHROLE


@dataclass
class ContractFunction:
    blockchain: str
    function_args: list
    function_name: str
    contract_address: str
    contract_abi: Optional[list] = None
    web3: Optional[Web3] = Web3(Web3.HTTPProvider("https://rpc.gnosischain.com/"))
    contract_instance: Optional[Web3] = None
    function_instance: Optional[Web3] = None

    def __post_init__(self):
        if self.contract_abi == None:
            self.contract_abi = RequestFromScan(blockchain=self.blockchain, module='contract', action='getabi',
                                            kwargs={'address': self.contract_abi}).request()['result']
        self.contract_address = self.web3.to_checksum_address(self.contract_address)
        self.contract_instance = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
        self.function_instance = self.contract_instance.functions[self.function_name]

    def call_function(self) -> Union[list,str,int]:
        result = self.function_instance(*self.function_args).call()
        return result

    def data_input(self) -> str:
        name = filter_by_name(self.function_name,json.loads(self.contract_abi))[0]
        types = get_abi_input_types(name)
        signature = Web3.keccak(text=f"{self.function_name}({','.join(types)})").hex()[:10]
        result = f"{signature}{encode_abi(types, self.function_args).hex()}"
        return result



       
