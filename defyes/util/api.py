from dataclasses import dataclass, field
from typing import Optional

import requests

from defyes.util.explorers import Explorer
from defyes.util.impl_contract import ImplContractData


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
