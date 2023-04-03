from typing import Optional, Union
from dataclasses import dataclass
from time import sleep

from web3 import Web3, exceptions
from eth_account import Account
from ape import accounts
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from defi_protocols.util.api import RequestFromScan
from defi_protocols.constants import SAFETRANSACTIONWITHROLE

accountOne = accounts.load('revoker-1')

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
        result = self.function_instance(*self.function_args).build_transaction()['data']
        return result

    def transact_with_role_from_EOA(
        self,
        private_key: str = None,
        chain_id: Optional[int] = None,
        gas_limit: Optional[int] = None,
        max_fee_per_gas: Optional[int] = None,
        max_prio_fee_per_gas: Optional[int] = None,
        nonce: Optional[int] = None,
        ) -> str:
        from_address = Account.from_key(private_key)
        if not max_fee_per_gas:
            max_fee_per_gas = self.web3.to_wei('5', 'gwei')

        if not nonce:
            nonce = self.web3.eth.get_transaction_count(from_address.address)
        if not max_prio_fee_per_gas:
            max_prio_fee_per_gas = self.web3.eth.max_priority_fee


        chain_id = self.web3.eth.chain_id        
        tx = self.function_instance(*self.function_args).build_transaction({
            'chainId':chain_id,
            'gas': 500000,
            'maxFeePerGas': max_fee_per_gas,
            'maxPriorityFeePerGas': max_prio_fee_per_gas,
            'nonce': nonce,
        })
        # if not gas_limit:
        #     tx['gas'] = self.web3.eth.estimate_gas({'to': self.contract_address, 'data':self.function_instance(*self.function_args).build_transaction()['data']}) * 1.1
        # else:
        #     tx['gas'] = gas_limit
        # print(gas_limit)
        #print(tx)
        signed_txn = self.web3.eth.account.sign_transaction(tx, private_key)
        #print(tx['gas'])
        executed_txn = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return executed_txn.hex()
    
    def get_tx_receipt(self,tx_hash):
        try:
            transaction_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
            return  transaction_receipt
        except exceptions.TransactionNotFound:
            return 'Transaction not yet on blockchain'
    
    
    def send_transaction_receipt_to_slack(self,channel,message):
        slack_client = WebClient(token=SAFETRANSACTIONWITHROLE)
        try:
            response = slack_client.chat_postMessage(
                channel=channel,
                text=message
            )
            print(f"Message sent successfully: {response['ts']}")
        except SlackApiError as e:
            print(f"Error sending message: {e}")

        
