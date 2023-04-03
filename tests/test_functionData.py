from defi_protocols.util.FunctionData import ContractFunction
from ape import accounts

CONTRACT_ADDRESS = '0x4ECaBa5870353805a9F068101A40E0f32ed605C6'
CONTRACT_ABI = '[{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},\
                {"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"result","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},\
                {"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},\
                {"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},\
                {"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"}]'
TO = '0xBA12222222228d8Ba445958a75a0704d566BF2C8' 
VALUE = 0
ROLES_MOD_CONTRACT = '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503'
ROLES_MOD_ABI = '[{"type":"function","stateMutability":"nonpayable","outputs":[{"type":"bool","name":"success","internalType":"bool"}],"name":"execTransactionWithRole","inputs":[{"type":"address","name":"to","internalType":"address"},{"type":"uint256","name":"value","internalType":"uint256"},{"type":"bytes","name":"data","internalType":"bytes"},{"type":"uint8","name":"operation","internalType":"enum Enum.Operation"},{"type":"uint16","name":"role","internalType":"uint16"},{"type":"bool","name":"shouldRevert","internalType":"bool"}]}]'

PRIVATE_KEYS = 'INSERT_PRIVATE_KEY here'
VALUEROLE = 0
OPERATION = 0
ROLE = 2
SHOULDREVERT = False
FUNCTIONROLE = 'execTransactionWithRole'
DATA = '0x095ea7b3000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000000000000000000000000'
FUNCTIONROLEARGS = [CONTRACT_ADDRESS,VALUEROLE,DATA,OPERATION,ROLE,SHOULDREVERT]

ACCOUNT = accounts.load('revoker-1')

def test_call_function():
    cf = ContractFunction(blockchain= 'gnosisChain', function_args=[], function_name='decimals', contract_address=CONTRACT_ADDRESS, contract_abi=CONTRACT_ABI)
    data = cf.call_function()
    assert data == 6

def test_data_input():
    cf = ContractFunction(blockchain= 'gnosisChain', function_args=[TO,VALUE], function_name='approve', contract_address=CONTRACT_ADDRESS, contract_abi=CONTRACT_ABI)
    data = cf.data_input()
    assert data == DATA

def test_transact_with_role_from_EOA():
    cf = ContractFunction(blockchain= 'gnosisChain', function_args=FUNCTIONROLEARGS, function_name=FUNCTIONROLE, contract_address=ROLES_MOD_CONTRACT, contract_abi=ROLES_MOD_ABI)
    data = cf.transact_with_role_from_EOA(PRIVATE_KEYS)
    assert data == '0x9ce84387a4f6922693bbd4c92e0ab8f671ebee9c13c30531de37cdc20c03588c'

TRANSACTIONRECEIPT = """AttributeDict({'transactionHash': HexBytes('0x9ce84387a4f6922693bbd4c92e0ab8f671ebee9c13c30531de37cdc20c03588c'), 'transactionIndex': 1, 'blockHash': HexBytes('0x712262a4eaadcf12f751ab4ddb8acf4dc796004f373e1767a47fa45a796eea8c'), 'blockNumber': 27250856, 'cumulativeGasUsed': 736015, 'gasUsed': 90782, 'effectiveGasPrice': 1510000001, \
                    'from': '0x7e19DE37A31E40eec58977CEA36ef7fB70e2c5CD', 'to': '0xB6CeDb9603e7992A5d42ea2246B3ba0a21342503', 'contractAddress': None, 'logs': [AttributeDict({'removed': False, 'logIndex': 3, 'transactionIndex': 1, 'transactionHash': HexBytes('0x9ce84387a4f6922693bbd4c92e0ab8f671ebee9c13c30531de37cdc20c03588c'), \
                    'blockHash': HexBytes('0x712262a4eaadcf12f751ab4ddb8acf4dc796004f373e1767a47fa45a796eea8c'), 'blockNumber': 27250856, 'address': '0x9a18b276e86844A05587e1C822D2311D51d1c7F9', \
                    'data': HexBytes('0x000000000000000000000000b6cedb9603e7992a5d42ea2246b3ba0a213425030000000000000000000000004ecaba5870353805a9f068101a40e0f32ed605c6000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000a000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044095ea7b3000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'),\
                    'topics': [HexBytes('0xb648d3644f584ed1c2232d53c46d87e693586486ad0d1175f8656013110b714e')]}), AttributeDict({'removed': False, 'logIndex': 4, 'transactionIndex': 1, 'transactionHash': HexBytes('0x9ce84387a4f6922693bbd4c92e0ab8f671ebee9c13c30531de37cdc20c03588c'), 'blockHash': HexBytes('0x712262a4eaadcf12f751ab4ddb8acf4dc796004f373e1767a47fa45a796eea8c'), 'blockNumber': 27250856, 'address': '0x4ECaBa5870353805a9F068101A40E0f32ed605C6', 'data': HexBytes('0x0000000000000000000000000000000000000000000000000000000000000000'), 'topics': [HexBytes('0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925'), \
                    HexBytes('0x0000000000000000000000009a18b276e86844a05587e1c822d2311d51d1c7f9'), HexBytes('0x000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c8')]}), AttributeDict({'removed': False, 'logIndex': 5, 'transactionIndex': 1, 'transactionHash': HexBytes('0x9ce84387a4f6922693bbd4c92e0ab8f671ebee9c13c30531de37cdc20c03588c'), 'blockHash': HexBytes('0x712262a4eaadcf12f751ab4ddb8acf4dc796004f373e1767a47fa45a796eea8c'), 'blockNumber': 27250856, 'address': '0x9a18b276e86844A05587e1C822D2311D51d1c7F9', 'data': HexBytes('0x'), 'topics': [HexBytes('0x6895c13664aa4f67288b25d7a21d7aaa34916e355fb9b6fae0a139a9085becb8'), \
                    HexBytes('0x000000000000000000000000b6cedb9603e7992a5d42ea2246b3ba0a21342503')]})], 'logsBloom': HexBytes('0x00000000040010040000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000008000000000200000000000000000000000000010000000000000000000000000000000000000000000000000000000000000100000000000000000020000000000000000000000000200010020000000000000000000040000000000000100000080000000000000020000000000000000000000000000000200000000000000000000000000000000000000000000000008000000000000002000000020000000000000001000000010080000000000000000000000000200000000000001000000000000000000'), 'status': 1, 'type': 2})"""

def test_get_tx_receipt():
    cf = ContractFunction(blockchain= 'gnosisChain', function_args=FUNCTIONROLEARGS, function_name=FUNCTIONROLE, contract_address=ROLES_MOD_CONTRACT, contract_abi=ROLES_MOD_ABI)
    data = cf.get_tx_receipt('0x9ce84387a4f6922693bbd4c92e0ab8f671ebee9c13c30531de37cdc20c03588c')
    assert data == TRANSACTIONRECEIPT

def test_send_transaction_receipt_to_slack():
    cf = ContractFunction(blockchain= 'gnosisChain', function_args=FUNCTIONROLEARGS, function_name=FUNCTIONROLE, contract_address=ROLES_MOD_CONTRACT, contract_abi=ROLES_MOD_ABI)
    data = cf.send_transaction_receipt_to_slack('safetransactionwithrole',str(TRANSACTIONRECEIPT))
    assert data == 'Message sent successfully: 1680464770.857389'
