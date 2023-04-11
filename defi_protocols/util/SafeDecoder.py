from defi_protocols.functions import *
from defi_protocols.util.api import RequestFromScan

SAFE_CONTRACT_ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"}],"name":"AddedOwner","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"approvedHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"owner","type":"address"}],"name":"ApproveHash","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"handler","type":"address"}],"name":"ChangedFallbackHandler","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"guard","type":"address"}],"name":"ChangedGuard","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"threshold","type":"uint256"}],"name":"ChangedThreshold","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"DisabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"EnabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"txHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"payment","type":"uint256"}],"name":"ExecutionFailure","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"module","type":"address"}],"name":"ExecutionFromModuleFailure","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"module","type":"address"}],"name":"ExecutionFromModuleSuccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"bytes32","name":"txHash","type":"bytes32"},{"indexed":false,"internalType":"uint256","name":"payment","type":"uint256"}],"name":"ExecutionSuccess","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"owner","type":"address"}],"name":"RemovedOwner","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"SafeReceived","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"initiator","type":"address"},{"indexed":false,"internalType":"address[]","name":"owners","type":"address[]"},{"indexed":false,"internalType":"uint256","name":"threshold","type":"uint256"},{"indexed":false,"internalType":"address","name":"initializer","type":"address"},{"indexed":false,"internalType":"address","name":"fallbackHandler","type":"address"}],"name":"SafeSetup","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"msgHash","type":"bytes32"}],"name":"SignMsg","type":"event"},{"stateMutability":"nonpayable","type":"fallback"},{"inputs":[],"name":"VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"_threshold","type":"uint256"}],"name":"addOwnerWithThreshold","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"hashToApprove","type":"bytes32"}],"name":"approveHash","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"approvedHashes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_threshold","type":"uint256"}],"name":"changeThreshold","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"dataHash","type":"bytes32"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bytes","name":"signatures","type":"bytes"},{"internalType":"uint256","name":"requiredSignatures","type":"uint256"}],"name":"checkNSignatures","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bytes32","name":"dataHash","type":"bytes32"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"bytes","name":"signatures","type":"bytes"}],"name":"checkSignatures","outputs":[],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prevModule","type":"address"},{"internalType":"address","name":"module","type":"address"}],"name":"disableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"domainSeparator","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"}],"name":"enableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint256","name":"safeTxGas","type":"uint256"},{"internalType":"uint256","name":"baseGas","type":"uint256"},{"internalType":"uint256","name":"gasPrice","type":"uint256"},{"internalType":"address","name":"gasToken","type":"address"},{"internalType":"address","name":"refundReceiver","type":"address"},{"internalType":"uint256","name":"_nonce","type":"uint256"}],"name":"encodeTransactionData","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint256","name":"safeTxGas","type":"uint256"},{"internalType":"uint256","name":"baseGas","type":"uint256"},{"internalType":"uint256","name":"gasPrice","type":"uint256"},{"internalType":"address","name":"gasToken","type":"address"},{"internalType":"address payable","name":"refundReceiver","type":"address"},{"internalType":"bytes","name":"signatures","type":"bytes"}],"name":"execTransaction","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModule","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModuleReturnData","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"returnData","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getChainId","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"start","type":"address"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getModulesPaginated","outputs":[{"internalType":"address[]","name":"array","type":"address[]"},{"internalType":"address","name":"next","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwners","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"offset","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"name":"getStorageAt","outputs":[{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint256","name":"safeTxGas","type":"uint256"},{"internalType":"uint256","name":"baseGas","type":"uint256"},{"internalType":"uint256","name":"gasPrice","type":"uint256"},{"internalType":"address","name":"gasToken","type":"address"},{"internalType":"address","name":"refundReceiver","type":"address"},{"internalType":"uint256","name":"_nonce","type":"uint256"}],"name":"getTransactionHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"}],"name":"isModuleEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"nonce","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prevOwner","type":"address"},{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"_threshold","type":"uint256"}],"name":"removeOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"requiredTxGas","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"handler","type":"address"}],"name":"setFallbackHandler","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"guard","type":"address"}],"name":"setGuard","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address[]","name":"_owners","type":"address[]"},{"internalType":"uint256","name":"_threshold","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"address","name":"fallbackHandler","type":"address"},{"internalType":"address","name":"paymentToken","type":"address"},{"internalType":"uint256","name":"payment","type":"uint256"},{"internalType":"address payable","name":"paymentReceiver","type":"address"}],"name":"setup","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"signedMessages","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"targetContract","type":"address"},{"internalType":"bytes","name":"calldataPayload","type":"bytes"}],"name":"simulateAndRevert","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prevOwner","type":"address"},{"internalType":"address","name":"oldOwner","type":"address"},{"internalType":"address","name":"newOwner","type":"address"}],"name":"swapOwner","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
ROLES_CONTRACT_ABI = '[{"inputs":[{"internalType":"address","name":"_owner","type":"address"},{"internalType":"address","name":"_avatar","type":"address"},{"internalType":"address","name":"_target","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"ArraysDifferentLength","type":"error"},{"inputs":[],"name":"ModuleTransactionFailed","type":"error"},{"inputs":[],"name":"NoMembership","type":"error"},{"inputs":[],"name":"SetUpModulesAlreadyCalled","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"},{"indexed":false,"internalType":"uint16[]","name":"roles","type":"uint16[]"},{"indexed":false,"internalType":"bool[]","name":"memberOf","type":"bool[]"}],"name":"AssignRoles","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousAvatar","type":"address"},{"indexed":true,"internalType":"address","name":"newAvatar","type":"address"}],"name":"AvatarSet","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"guard","type":"address"}],"name":"ChangedGuard","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"DisabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"}],"name":"EnabledModule","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"initiator","type":"address"},{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"avatar","type":"address"},{"indexed":false,"internalType":"address","name":"target","type":"address"}],"name":"RolesModSetup","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"module","type":"address"},{"indexed":false,"internalType":"uint16","name":"defaultRole","type":"uint16"}],"name":"SetDefaultRole","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"multisendAddress","type":"address"}],"name":"SetMultisendAddress","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousTarget","type":"address"},{"indexed":true,"internalType":"address","name":"newTarget","type":"address"}],"name":"TargetSet","type":"event"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"allowTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"},{"internalType":"uint16[]","name":"_roles","type":"uint16[]"},{"internalType":"bool[]","name":"memberOf","type":"bool[]"}],"name":"assignRoles","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"avatar","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"defaultRoles","outputs":[{"internalType":"uint16","name":"","type":"uint16"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prevModule","type":"address"},{"internalType":"address","name":"module","type":"address"}],"name":"disableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"}],"name":"enableModule","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModule","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"}],"name":"execTransactionFromModuleReturnData","outputs":[{"internalType":"bool","name":"","type":"bool"},{"internalType":"bytes","name":"","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"bool","name":"shouldRevert","type":"bool"}],"name":"execTransactionWithRole","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"},{"internalType":"enum Enum.Operation","name":"operation","type":"uint8"},{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"bool","name":"shouldRevert","type":"bool"}],"name":"execTransactionWithRoleReturnData","outputs":[{"internalType":"bool","name":"success","type":"bool"},{"internalType":"bytes","name":"returnData","type":"bytes"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getGuard","outputs":[{"internalType":"address","name":"_guard","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"start","type":"address"},{"internalType":"uint256","name":"pageSize","type":"uint256"}],"name":"getModulesPaginated","outputs":[{"internalType":"address[]","name":"array","type":"address[]"},{"internalType":"address","name":"next","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"guard","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_module","type":"address"}],"name":"isModuleEnabled","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"multisend","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"}],"name":"revokeTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeAllowFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"bool[]","name":"isParamScoped","type":"bool[]"},{"internalType":"enum ParameterType[]","name":"paramType","type":"uint8[]"},{"internalType":"enum Comparison[]","name":"paramComp","type":"uint8[]"},{"internalType":"bytes[]","name":"compValue","type":"bytes[]"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"enum ExecutionOptions","name":"options","type":"uint8"}],"name":"scopeFunctionExecutionOptions","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint256","name":"paramIndex","type":"uint256"},{"internalType":"enum ParameterType","name":"paramType","type":"uint8"},{"internalType":"enum Comparison","name":"paramComp","type":"uint8"},{"internalType":"bytes","name":"compValue","type":"bytes"}],"name":"scopeParameter","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint256","name":"paramIndex","type":"uint256"},{"internalType":"enum ParameterType","name":"paramType","type":"uint8"},{"internalType":"bytes[]","name":"compValues","type":"bytes[]"}],"name":"scopeParameterAsOneOf","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"}],"name":"scopeRevokeFunction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"}],"name":"scopeTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_avatar","type":"address"}],"name":"setAvatar","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"module","type":"address"},{"internalType":"uint16","name":"role","type":"uint16"}],"name":"setDefaultRole","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_guard","type":"address"}],"name":"setGuard","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_multisend","type":"address"}],"name":"setMultisend","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_target","type":"address"}],"name":"setTarget","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"initParams","type":"bytes"}],"name":"setUp","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"target","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint16","name":"role","type":"uint16"},{"internalType":"address","name":"targetAddress","type":"address"},{"internalType":"bytes4","name":"functionSig","type":"bytes4"},{"internalType":"uint8","name":"paramIndex","type":"uint8"}],"name":"unscopeParameter","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

def get_safe_actions(tx_hash: str, blockchain: str, web3: object = None, execution: int = 1, index: int = 0) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=last_block(blockchain), index=index)# We force the use of an archival node with block=last_block(blockchain)

        tx_receipt = web3.eth.get_transaction(tx_hash)
        tx_to = tx_receipt['to']
        tx_input_data = tx_receipt['input']

        try:
            to_contract = web3.eth.contract(address=tx_to, abi=SAFE_CONTRACT_ABI)
            to_contract.functions.VERSION().call()
        except:
            try:
                to_contract = web3.eth.contract(address=tx_to, abi=ROLES_CONTRACT_ABI)
                to_contract.functions.avatar().call()
            except:
                print('To address is neither a safe nor a Roles mod contract')
                return None


        #FIXME: blockchain2 is used by RequestFromScan because it uses GNOSIS instead of XDAI, should be fixed when we remove XDAI
        if blockchain == XDAI:
            blockchain2 = 'gnosis'
        else:
            blockchain2 = blockchain

        input_data = to_contract.decode_function_input(tx_input_data)
        functions, params = input_data
        if 'execTransaction' in str(functions):
            input_data_contract_address = params['to']
            input_data_abi = RequestFromScan(blockchain=blockchain2, module='contract', action='getabi',
                                             kwargs={'address': input_data_contract_address}).request()['result']
            input_data_contract = web3.eth.contract(address=input_data_contract_address, abi=input_data_abi)
            input_data_bytes = input_data_contract.decode_function_input(params['data'].hex())
            functions2, params2 = input_data_bytes
            if 'multiSend' in str(functions2):
                transaction = params2['transactions'].hex()
                function_list = decode_multisend_transaction('0x' + transaction, web3)
                return function_list
            elif 'execTransactionWithRole' in str(functions2):
                functions3, params3 = decode_function_input(params2['to'], '0x'+params2['data'].hex(), web3)
                decode_dict = [{'to_address': params2['to'], 'value': params2['value'], 'signature': str(functions3)[10:-1], 'arguments': params3}]
                return decode_dict
            else:
                decode_dict = [{'to_address': params['to'], 'value': params['value'],
                               'signature': str(functions2)[10:-1], 'arguments': params2}]
                return decode_dict
        elif 'execTransactionWithRole' in str(functions):
            functions2, params2 = decode_function_input(params['to'], '0x'+params['data'].hex(), web3)
            decode_dict = [{'to_address': params2['to'], 'value': params2['value'], 'signature': str(functions2)[10:-1], 'arguments': params2}]
            return decode_dict
        else:
            print('Not a safe nor Roles transaction')

    except GetNodeIndexError:
        return get_safe_actions(tx_hash, blockchain, web3, index=0, execution=execution + 1)

    except:
        return get_safe_actions(tx_hash, blockchain, web3, index=index + 1, execution=execution)


def decode_multisend_transaction(input_data: str, web3) -> list:
    """
    input_data is the bytes argument in the multiSend function
    """
    if web3.eth.chain_id == 1:
        blockchain = ETHEREUM
    else:
        blockchain = XDAI

    if input_data[:2] == '0x':
        input_data = input_data[2:]

    function_list = []
    while True:
        #operation = input_data[:2]
        to_address = '0x' + input_data[2:42]
        value = input_data[42:106]
        data_length = int('0x' + input_data[106:170].lstrip('0'), 16)
        data_rest = input_data[170:170 + (data_length * 2)]
        function, params = decode_function_input(to_address, '0x'+data_rest, web3)
        decode_dict = {'to_address': to_address, 'value': int(value,16), 'signature': str(function)[10:-1], 'arguments': params}
        function_list.append(decode_dict)
        input_data = input_data[170 + (data_length * 2):]
        if len(input_data) == 0:
            break
    return function_list


def decode_function_input(contract_address: str, input_hex: str, web3, abi=None) -> tuple:
    """

    """
    if contract_address[:2] == '0x':
        checksum_address = web3.to_checksum_address(contract_address)
    else:
        checksum_address = web3.to_checksum_address('0x' + contract_address)

    if web3.eth.chain_id == 1:
        blockchain = ETHEREUM
    else:
        blockchain = 'gnosis'

    if abi is None:
        abi = RequestFromScan(blockchain=blockchain, module='contract', action='getabi', kwargs={'address': checksum_address}).request()['result']
    function_contract = web3.eth.contract(address=checksum_address, abi=abi)
    if 'implementation' in str(abi):
        impl_address = function_contract.functions.implementation().call()
        abi = RequestFromScan(blockchain=blockchain, module='contract', action='getabi', kwargs={'address': impl_address}).request()['result']
        function_contract = web3.eth.contract(address=checksum_address, abi=abi)
    function_decode = function_contract.decode_function_input(input_hex)

    return function_decode

blockchain = 'ethereum'
tx1 = '0x2971c45416cbf234fe8939599dbb64d5c53210e76e4ff32d89188fa9bea30f87' # multisend
tx2 = '0x3c0fbad1350d84a159acef5c3e6fe350e10d44dc894bb3ee6f784b0c167e791f' # exec with role from manager safe
tx2_2 = '0x4170bc71b410f331e5d049be7bc4872380134827b69a4e39642c04b918434fa9'# exec with role from manager safe
tx3 = '0xd6ef0254c88760e5a2e58924bbaa28f8700341bfa91df469fc9c6f904b732e34' # single call
print('1',get_safe_actions(tx1, blockchain))
print('2',get_safe_actions(tx2, blockchain))
print('3',get_safe_actions(tx2_2, blockchain))
print('4',get_safe_actions(tx3, blockchain))

web3 = get_node(XDAI)
#print(decode_function_input())
print('yes')
print(decode_multisend_transaction('0x006a023ccd1ff6f2045c3309768ead9e68f978f6e100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044095ea7b3000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000000155bd9307f9fe80000009c58bacc331c9aa871afd802db6379a98e80cedb00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044095ea7b3000000000000000000000000ba12222222228d8ba445958a75a0704d566bf2c80000000000000000000000000000000000000000000001583bf3dc4212780000', web3))


web3 = get_node(ETHEREUM)
print(decode_function_input('0x074306bc6a6fc1bd02b425dd41d742adf36ca9c6','0x63453ae1000000000000000000000000675ec042325535f6e176638dd2d4994f645502b9', web3))
print(decode_multisend_transaction('0x00074306bc6a6fc1bd02b425dd41d742adf36ca9c60000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002463453ae1000000000000000000000000675ec042325535f6e176638dd2d4994f645502b900675ec042325535f6e176638dd2d4994f645502b900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004e6f1daf200675ec042325535f6e176638dd2d4994f645502b9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000242e1a7d4d000000000000000000000000000000000000000000000030a2b81aa7faf0c8b4', web3))


print('mierda')

blockchain = XDAI
tx1 = '0x29ab61b70723cfafa6a8d4c52c3d98aaf99a68108e3a2c5eaee8db4d0b519c75' # single call
tx2 = '0xf86a4de912225c46047e6fb2fa4d86f14f5f677a813ef267cca7a48d2886055f' # multisend
tx3 = '0xffd333e9cdfcd5818921a944914bf5a4e1e326cadef897ba3ddea239b0a4d3c9' # execTransactionWithRole from EOA
print('1',get_safe_actions(tx1, blockchain))
print('2',get_safe_actions(tx2, blockchain))

print('mierda2')








web3 = get_node(ETHEREUM)

print('')

blockchain = 'ethereum'
tx1 = '0x2971c45416cbf234fe8939599dbb64d5c53210e76e4ff32d89188fa9bea30f87' # multisend
tx2 = '0x3c0fbad1350d84a159acef5c3e6fe350e10d44dc894bb3ee6f784b0c167e791f' # exec with role from manager safe
tx2_2 = '0x4170bc71b410f331e5d049be7bc4872380134827b69a4e39642c04b918434fa9'# exec with role from manager safe
tx3 = '0xd6ef0254c88760e5a2e58924bbaa28f8700341bfa91df469fc9c6f904b732e34' # single call
print('1',get_safe_actions(tx1, blockchain))
print('2',get_safe_actions(tx2, blockchain))
print('3',get_safe_actions(tx2_2, blockchain))
print('4',get_safe_actions(tx3, blockchain))



web3 = get_node(ETHEREUM)
print(decode_function_input('0x074306bc6a6fc1bd02b425dd41d742adf36ca9c6','0x63453ae1000000000000000000000000675ec042325535f6e176638dd2d4994f645502b9', web3))
print(decode_multisend_transaction('0x00074306bc6a6fc1bd02b425dd41d742adf36ca9c60000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002463453ae1000000000000000000000000675ec042325535f6e176638dd2d4994f645502b900675ec042325535f6e176638dd2d4994f645502b900000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000004e6f1daf200675ec042325535f6e176638dd2d4994f645502b9000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000242e1a7d4d000000000000000000000000000000000000000000000030a2b81aa7faf0c8b4', web3))









