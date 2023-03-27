import requests
import json
import functools
import calendar
import lru
import math
import logging
from datetime import datetime
from decimal import Decimal
from typing import Union, Optional

import eth_abi
from web3 import Web3
from web3.middleware import construct_simple_cache_middleware
from defi_protocols.constants import (API_KEY_ETHERSCAN, API_GOERLI_GETLOGS, GOERLI, API_KOVAN_GETLOGS, KOVAN, API_ROPSTEN_GETLOGS, ROPSTEN,
                                     API_KEY_OPTIMISM, API_OPTIMISM_GETLOGS, OPTIMISM, API_KEY_FANTOM, API_FANTOM_GETLOGS, FANTOM,
                                     API_KEY_BINANCE, API_BINANCE_GETLOGS, BINANCE, API_KEY_AVALANCHE, API_AVALANCHE_GETLOGS,
                                     AVALANCHE, API_KEY_GNOSISSCAN, API_GNOSISSCAN_GETLOGS, XDAI, API_KEY_POLSCAN, API_POLYGONSCAN_GETLOGS,
                                     POLYGON, API_ETHERSCAN_GETLOGS, ETHEREUM, API_GOERLI_TXLIST, API_KOVAN_TXLIST, API_ROPSTEN_TXLIST,
                                     API_OPTIMISM_TXLIST, API_FANTOM_TXLIST, API_AVALANCHE_TXLIST, API_BINANCE_TXLIST, API_GNOSISSCAN_TXLIST,
                                      API_KEY_POLSCAN, API_POLYGONSCAN_TXLIST, API_ETHERSCAN_TXLIST, API_GOERLI_TOKENTX, API_KOVAN_TOKENTX,
                                      API_ROPSTEN_TOKENTX, API_OPTIMISM_TOKENTX, API_FANTOM_TOKENTX, API_AVALANCHE_TOKENTX, API_BINANCE_TOKENTX,
                                      API_GNOSISSCAN_TOKENTX, API_POLYGONSCAN_TOKENTX, API_ETHERSCAN_TOKENTX, ZERO_ADDRESS, TESTNET_HEADER,
                                      API_GOERLI_GETABI, API_KOVAN_GETABI, API_ROPSTEN_GETABI, API_OPTIMISM_GETABI, API_FANTOM_GETABI, API_AVALANCHE_GETABI,
                                      API_BINANCE_GETABI, API_BLOCKSCOUT_GETABI, API_GNOSISSCAN_GETABI, API_POLYGONSCAN_GETABI, API_ETHERSCAN_GETABI,
                                      ABI_TOKEN_SIMPLIFIED, E_ADDRESS, MAX_EXECUTIONS, API_BLOCKSCOUT_GETTOKENCONTRACT, API_KEY_ETHPLORER, API_ETHPLORER_GETTOKENINFO,
                                      API_GOERLI_GETBLOCKREWARD, API_KOVAN_GETBLOCKREWARD, API_ROPSTEN_GETBLOCKREWARD, API_OPTIMISM_GETBLOCKREWARD, API_FANTOM_GETBLOCKREWARD,
                                      API_AVALANCHE_GETBLOCKREWARD, API_BINANCE_GETBLOCKREWARD, API_GNOSISSCAN_GETBLOCKREWARD, API_POLYGONSCAN_GETBLOCKREWARD,
                                      API_ETHERSCAN_GETBLOCKREWARD, API_GOERLI_GETBLOCKNOBYTIME, API_KOVAN_GETBLOCKNOBYTIME, API_ROPSTEN_GETBLOCKNOBYTIME,
                                      API_OPTIMISM_GETBLOCKNOBYTIME, API_FANTOM_GETBLOCKNOBYTIME, API_AVALANCHE_GETBLOCKNOBYTIME, API_BINANCE_GETBLOCKNOBYTIME,
                                      API_GNOSISSCAN_GETBLOCKNOBYTIME, API_POLYGONSCAN_GETBLOCKNOBYTIME, API_ETHERSCAN_GETBLOCKNOBYTIME,
                                      NODE_GOERLI, NODE_KOVAN, NODE_ROPSTEN, NODE_OPTIMISM, NODE_FANTOM, NODE_AVALANCHE, NODE_BINANCE, NODE_XDAI, NODE_POL, NODE_ETH)


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CUSTOM EXCEPTIONS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
class GetNodeIndexError(Exception):
    """

    """
    pass


class abiNotVerified(Exception):
    """

    """

    def __init__(self, message='Contract source code not verified') -> None:
        self.message = message
        super().__init__(self.message)


def get_web3_provider(endpoint):
    provider = Web3.HTTPProvider(endpoint)

    web3 = Web3(provider)

    # enable simple web3 cache, for example to cache eth_chainId calls
    # more methods can be cached after analysing whether they are safe to cache
    simple_cache = construct_simple_cache_middleware(
        cache_class=functools.partial(lru.LRU, 4096),
        rpc_whitelist={'eth_chainId'},
    )

    class CallCounterMiddleware:
        call_count = 0

        def __init__(self, make_request, w3):
            self.w3 = w3
            self.make_request = make_request

        @classmethod
        def increment(cls):
            cls.call_count += 1

        def __call__(self, method, params):
            self.increment()
            logger.debug('Web3 call count: %d', self.call_count)
            response = self.make_request(method, params)
            return response

    web3.middleware_onion.add(CallCounterMiddleware, 'call_counter')
    # adding the cache after to get only effective calls counted by the counter
    web3.middleware_onion.add(simple_cache, 'simple_cache')
    return web3

def get_web3_call_count(web3):
    """Obtain the total number of calls that have been made by a web3 instance."""
    return web3.middleware_onion['call_counter'].call_count


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_node
# 'block' = 'latest' -> retrieves a Full Node / 'block' = block or not passed onto the function -> retrieves an Archival Node
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_node(blockchain, block='latest', index=0):
    """

    :param blockchain:
    :param block:
    :param index:
    :return:
    """
    if blockchain == ETHEREUM:
        node = NODE_ETH

    elif blockchain == POLYGON:
        node = NODE_POL

    elif blockchain == XDAI:
        node = NODE_XDAI

    elif blockchain == BINANCE:
        node = NODE_BINANCE

    elif blockchain == AVALANCHE:
        node = NODE_AVALANCHE

    elif blockchain == FANTOM:
        node = NODE_FANTOM

    elif blockchain == OPTIMISM:
        node = NODE_OPTIMISM

    elif blockchain == ROPSTEN:
        node = NODE_ROPSTEN

    elif blockchain == KOVAN:
        node = NODE_KOVAN

    elif blockchain == GOERLI:
        node = NODE_GOERLI
    else:
        raise Exception

    if isinstance(block, str):
        if block == 'latest':
            if index > (len(node['latest']) - 1):
                if index > (len(node['latest']) + len(node['archival']) - 1):
                    raise GetNodeIndexError
                else:
                    web3 = get_web3_provider(node['archival'][index - len(node['latest'])])
            else:
                web3 = get_web3_provider(node['latest'][index])
        else:
            raise ValueError('Incorrect block.')

    else:
        if index > (len(node['archival']) - 1):
            raise GetNodeIndexError
        else:
            web3 = get_web3_provider(node['archival'][index])


    # enable simple web3 cache, for example to cache eth_chainId calls
    # more methods can be cached after analysing whether they are safe to cache
    simple_cache = construct_simple_cache_middleware(
        cache_class=functools.partial(lru.LRU, 4096),
        rpc_whitelist={'eth_chainId'},
    )
    web3.middleware_onion.add(simple_cache)
    return web3


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# last_block
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def last_block(blockchain, web3=None, block='latest', index=0):
    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    return web3.eth.blockNumber


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# timestamp_to_date
# 'utc' = timezone of the Output is UTC(+'utc')
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def timestamp_to_date(timestamp, utc=0):
    return datetime.utcfromtimestamp(timestamp + 3600 * utc).strftime('%Y-%m-%d %H:%M:%S')


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# timestamp_to_block
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def timestamp_to_block(timestamp, blockchain) -> int:
    data = None

    while data is None:
        if blockchain == ETHEREUM:
            data = requests.get(API_ETHERSCAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN)).json()['result']

        elif blockchain == POLYGON:
            data = requests.get(API_POLYGONSCAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_POLSCAN)).json()['result']

        elif blockchain == XDAI:
            data = requests.get(API_GNOSISSCAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_GNOSISSCAN)).json()['result']
            # For BLOCKSCOUT
            # if data is None:
            #     time.sleep(0.1)
            # else:
            #     data = data['blockNumber']

        elif blockchain == BINANCE:
            data = requests.get(API_BINANCE_GETBLOCKNOBYTIME % (timestamp, API_KEY_BINANCE)).json()['result']

        elif blockchain == AVALANCHE:
            data = requests.get(API_AVALANCHE_GETBLOCKNOBYTIME % (timestamp, API_KEY_AVALANCHE)).json()['result']

        elif blockchain == FANTOM:
            data = requests.get(API_FANTOM_GETBLOCKNOBYTIME % (timestamp, API_KEY_FANTOM)).json()['result']

        elif blockchain == OPTIMISM:
            data = requests.get(API_OPTIMISM_GETBLOCKNOBYTIME % (timestamp, API_KEY_OPTIMISM)).json()['result']

        elif blockchain == ROPSTEN:
            data = \
                requests.get(API_ROPSTEN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN),
                             headers=TESTNET_HEADER).json()[
                    'result']

        elif blockchain == KOVAN:
            data = \
                requests.get(API_KOVAN_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN),
                             headers=TESTNET_HEADER).json()[
                    'result']

        elif blockchain == GOERLI:
            data = \
                requests.get(API_GOERLI_GETBLOCKNOBYTIME % (timestamp, API_KEY_ETHERSCAN),
                             headers=TESTNET_HEADER).json()[
                    'result']

    return int(data)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# date_to_timestamp
# 'utc' = timezone of the Input is UTC(+'utc')
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def date_to_timestamp(datestring, utc=0):
    #   localTimestamp = math.floor(time.mktime(datetime.strptime(datestring,'%Y-%m-%d %H:%M:%S').timetuple()) + 3600 * utc)
    utc_timestamp = math.floor(
        calendar.timegm(datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S').timetuple()) - 3600 * utc)

    return utc_timestamp


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# date_to_block
# 'utc' = timezone of the Output is UTC(+'utc')
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def date_to_block(datestring, blockchain, utc=0) -> int:
    """

    :param str datestring:
    :param str blockchain:
    :param utc:
    :return:
    """
    return timestamp_to_block(date_to_timestamp(datestring, utc=utc), blockchain)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# block_to_timestamp
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_to_timestamp(block, blockchain):
    data = None

    if isinstance(block, str):
        if block == 'latest':
            return math.floor(datetime.now().timestamp())

    while data is None:
        if blockchain == ETHEREUM:
            data = requests.get(API_ETHERSCAN_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN)).json()['result']['timeStamp']

        elif blockchain == POLYGON:
            data = requests.get(API_POLYGONSCAN_GETBLOCKREWARD % (block, API_KEY_POLSCAN)).json()['result']['timeStamp']

        elif blockchain == XDAI:
            data = requests.get(API_GNOSISSCAN_GETBLOCKREWARD % (block, API_KEY_GNOSISSCAN)).json()['result'][
                'timeStamp']

        elif blockchain == BINANCE:
            data = requests.get(API_BINANCE_GETBLOCKREWARD % (block, API_KEY_BINANCE)).json()['result']['timeStamp']

        elif blockchain == AVALANCHE:
            data = requests.get(API_AVALANCHE_GETBLOCKREWARD % (block, API_KEY_AVALANCHE)).json()['result']['timeStamp']

        elif blockchain == FANTOM:
            data = requests.get(API_FANTOM_GETBLOCKREWARD % (block, API_KEY_FANTOM)).json()['result']['timeStamp']

        elif blockchain == OPTIMISM:
            data = requests.get(API_OPTIMISM_GETBLOCKREWARD % (block, API_KEY_OPTIMISM)).json()['result']['timeStamp']

        elif blockchain == ROPSTEN:
            data = requests.get(API_ROPSTEN_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()[
                'result']['timeStamp']

        elif blockchain == KOVAN:
            data = requests.get(API_KOVAN_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()[
                'result']['timeStamp']

        elif blockchain == GOERLI:
            data = requests.get(API_GOERLI_GETBLOCKREWARD % (block, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()[
                'result']['timeStamp']

    return int(data)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# block_to_date
# 'utc' = timezone of the Output is UTC(+'utc')
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_to_date(block, blockchain, utc=0):
    return timestamp_to_date(block_to_timestamp(block, blockchain), utc=utc)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_blocks_per_year
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_blocks_per_year(blockchain):
    current_block = last_block(blockchain)
    ts = math.floor(datetime.now().timestamp()) - (3600 * 24 * 365)
    block = timestamp_to_block(ts, blockchain)

    block_delta = current_block - block

    return block_delta


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ERC20 TOKENS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# token_info
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def token_info(token_address, blockchain):  # NO ESTÁ POLYGON

    if blockchain.lower() == ETHEREUM:
        data = requests.get(API_ETHPLORER_GETTOKENINFO % (token_address, API_KEY_ETHPLORER)).json()

    elif blockchain.lower() == XDAI:
        data = requests.get(API_BLOCKSCOUT_GETTOKENCONTRACT % token_address).json()['result']

    return data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# balance_of
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def balance_of(address, contract_address, block, blockchain, execution=1, web3=None, index=0, decimals=True) -> Union[
    int, float]:
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        address = web3.to_checksum_address(address)

        contract_address = web3.to_checksum_address(contract_address)

        if contract_address == ZERO_ADDRESS:
            if decimals is True:
                return web3.eth.get_balance(address, block) / (10 ** 18)
            else:
                return web3.eth.get_balance(address, block)

        else:
            token_contract = web3.eth.contract(address=contract_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))

            try:
                balance = token_contract.functions.balanceOf(address).call(block_identifier=block)
            except:
                balance = 0

            if decimals is True:
                token_decimals = token_contract.functions.decimals().call()
                return float(Decimal(balance) / Decimal(10 ** token_decimals))
            else:
                return balance



    except GetNodeIndexError:
        return balance_of(address, contract_address, block, blockchain, decimals=decimals, index=0,
                          execution=execution + 1)

    except:
        return balance_of(address, contract_address, block, blockchain, decimals=decimals, index=index + 1,
                          execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# total_supply
# 'web3' = web3 (Node) -> Improves performance
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'decimals' = True -> retrieves the results considering the decimals / 'decimals' = False or not passed onto the function -> decimals are not considered
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def total_supply(token_address, block, blockchain, execution=1, web3=None, index=0, decimals=True):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        if not web3.isChecksumAddress(token_address):
            token_address = web3.to_checksum_address(token_address)

        token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
        total_supply_v = token_contract.functions.totalSupply().call(block_identifier=block)

        if decimals is True:
            token_decimals = token_contract.functions.decimals().call(block_identifier=block)
        else:
            token_decimals = 0

        return float(Decimal(total_supply_v) / Decimal(10 ** token_decimals))

    except GetNodeIndexError:
        return total_supply(token_address, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return total_supply(token_address, block, blockchain, decimals=decimals, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_decimals
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_decimals(token_address, blockchain, execution=1, web3=None, block='latest', index=0):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        token_address = web3.to_checksum_address(token_address)

        if token_address == ZERO_ADDRESS or token_address == E_ADDRESS:
            decimals = 18
        else:
            token_contract = web3.eth.contract(address=token_address, abi=json.loads(ABI_TOKEN_SIMPLIFIED))
            decimals = token_contract.functions.decimals().call()

        return decimals

    except GetNodeIndexError:
        return get_decimals(token_address, blockchain, block=block, index=0, execution=execution + 1)

    except:
        return get_decimals(token_address, blockchain, block=block, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_symbol
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_symbol(token_address, blockchain, execution=1, web3=None, block='latest', index=0) -> str:
    """

    :param str token_address:
    :param str blockchain:
    :param web3:
    :param block:
    :param int index:
    :return:
    """

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:

        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        if not web3.isConnected():
            raise Exception

        token_address = web3.to_checksum_address(token_address)

        if token_address == ZERO_ADDRESS or token_address == E_ADDRESS:
            if blockchain == ETHEREUM:
                symbol = 'ETH'
            elif blockchain == POLYGON:
                symbol = 'MATIC'
            elif blockchain == XDAI:
                symbol = 'XDAI'
        else:
            token_contract = web3.eth.contract(address=token_address, abi=ABI_TOKEN_SIMPLIFIED)

            try:
                symbol = token_contract.functions.symbol().call()
            except:
                try:
                    symbol = token_contract.functions.SYMBOL().call()
                except:
                    try:
                        token_contract = web3.eth.contract(address=token_address,
                                                           abi=get_contract_abi(token_address, blockchain))
                        symbol = token_contract.functions.symbol().call()
                    except:
                        logger.debug('Token %s has no symbol()' % token_address)
                        symbol = ''

            if not isinstance(symbol, str):
                symbol = symbol.hex()
                symbol = bytes.fromhex(symbol).decode('utf-8').rstrip('\x00')

        return symbol

    except GetNodeIndexError:
        return get_symbol(token_address, blockchain, block=block, index=0, execution=execution + 1)

    except:
        return get_symbol(token_address, blockchain, block=block, index=index + 1, execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CONTRACTS AND ABIS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract_abi
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract_abi(contract_address, blockchain):
    data = None

    while data is None:
        if blockchain == ETHEREUM:
            data = requests.get(API_ETHERSCAN_GETABI % (contract_address, API_KEY_ETHERSCAN)).json()['result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == POLYGON:
            data = requests.get(API_POLYGONSCAN_GETABI % (contract_address, API_KEY_POLSCAN)).json()['result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == XDAI:
            data = requests.get(API_GNOSISSCAN_GETABI % (contract_address, API_KEY_GNOSISSCAN)).json()['result']
            if data == 'Contract source code not verified':
                data = requests.get(API_BLOCKSCOUT_GETABI % contract_address).json()['result']
                if data == 'Contract source code not verified':
                    raise abiNotVerified

        elif blockchain == BINANCE:
            data = requests.get(API_BINANCE_GETABI % (contract_address, API_KEY_BINANCE)).json()['result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == AVALANCHE:
            data = requests.get(API_AVALANCHE_GETABI % (contract_address, API_KEY_AVALANCHE)).json()['result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == FANTOM:
            data = requests.get(API_FANTOM_GETABI % (contract_address, API_KEY_FANTOM)).json()['result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == OPTIMISM:
            data = requests.get(API_OPTIMISM_GETABI % (contract_address, API_KEY_OPTIMISM)).json()['result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == ROPSTEN:
            data = \
            requests.get(API_ROPSTEN_GETABI % (contract_address, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()[
                'result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == KOVAN:
            data = \
            requests.get(API_KOVAN_GETABI % (contract_address, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()[
                'result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

        elif blockchain == GOERLI:
            data = \
            requests.get(API_GOERLI_GETABI % (contract_address, API_KEY_ETHERSCAN), headers=TESTNET_HEADER).json()[
                'result']
            if data == 'Contract source code not verified':
                raise abiNotVerified

    return data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract
# 'web3' = web3 (Node) -> Improves performance
# 'abi' = specifies the exact ABI (used when contracts are not verified)
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract(contract_address, blockchain, web3=None, abi=None, block='latest', index=0):
    if web3 == None:
        web3 = get_node(blockchain, block=block, index=index)

    contract_address = web3.to_checksum_address(contract_address)

    if abi == None:
        try:
            abi = get_contract_abi(contract_address, blockchain)
            return web3.eth.contract(address=contract_address, abi=abi)
        except abiNotVerified:
            logger.exception("ABI not verified")
            return None
    else:
        return web3.eth.contract(address=contract_address, abi=abi)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_contract_proxy_abi
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_contract_proxy_abi(contract_address, abi_contract_address, blockchain, web3=None, block='latest', index=0):
    if web3 is None:
        web3 = get_node(blockchain, block=block, index=index)

    address = web3.to_checksum_address(contract_address)

    try:
        abi = get_contract_abi(abi_contract_address, blockchain)
        return web3.eth.contract(address=address, abi=abi)
    except abiNotVerified as Ex:
        logger.exception(Ex)
        return None


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# search_proxy_contract
# 'web3' = web3 (Node) -> Improves performance
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def search_proxy_contract(contract_address, blockchain, web3=None):
    if web3 == None:
        web3 = get_node(blockchain)

    contract_address = web3.to_checksum_address(contract_address)

    contract = get_contract(contract_address, blockchain, web3=web3)

    if contract is not None:
        for func in [obj for obj in contract.abi if obj['type'] == 'function']:
            name = str(func['name'].lower())
            if 'implementation' in name:
                output_types = [output['type'] for output in func['outputs']]
                if output_types == ['address']:
                    try:
                        proxy_address_func = getattr(contract.functions, func['name'])
                        proxy_address = proxy_address_func().call()
                        if web3.isAddress(proxy_address) and proxy_address != ZERO_ADDRESS:
                            return get_contract_proxy_abi(contract_address, proxy_address, blockchain, web3=web3)
                    except:
                        continue

    return contract


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_abi_function_signatures
# 'web3' = web3 (Node) -> Improves performance
# 'abi_address' = Proxy contract to get the ABI
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_abi_function_signatures(contract_address, blockchain, web3=None, abi_address=None):
    if web3 == None:
        web3 = get_node(blockchain)

    contract_address = web3.to_checksum_address(contract_address)

    if abi_address is None:
        contract = search_proxy_contract(contract_address, blockchain, web3=web3)
    else:
        contract = get_contract_proxy_abi(contract_address, abi_address, blockchain, web3=web3)

    if contract is not None:

        abi = contract.abi

        functions = []
        for func in [obj for obj in abi if obj['type'] == 'function']:
            function = {}
            name = func['name']
            input_types = [input['type'] for input in func['inputs']]

            function = {}
            function['name'] = name
            function['signature'] = '{}{}'.format(name, '(')
            function['inline_signature'] = '{}{}'.format(name, '(')
            function['components'] = []
            function['stateMutability'] = func['stateMutability']

            i = 0
            for input_type in input_types:
                if input_type == 'tuple':
                    function['components'] = [component['type'] for component in func['inputs'][i]['components']]
                    function['inline_signature'] += '({})'.format(','.join(function['components']))
                else:
                    function['inline_signature'] += input_type
                    function['components'].append(input_type)

                function['signature'] += input_type

                if i < len(input_types) - 1:
                    function['signature'] += ','
                    function['inline_signature'] += ','

                i += 1

            function['signature'] += ')'
            function['inline_signature'] += ')'

            functions.append(function)

        return functions

    return None


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_data
# 'web3' = web3 (Node) -> Improves performance
# 'abi_address' = Proxy contract to get the ABI
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_data(contract_address, function_name, parameters, blockchain, web3=None, abi_address=None):
    if web3 == None:
        web3 = get_node(blockchain)

    contract_address = web3.to_checksum_address(contract_address)

    if abi_address is None:
        contract = get_contract(contract_address, blockchain, web3=web3)

        if contract is None:
            return None
        else:
            try:
                getattr(contract.functions, function_name)
            except:
                # If the contract does not have the function, it checks if there is a proxy implementation
                proxy_contract = search_proxy_contract(contract_address, blockchain, web3=web3)

                if proxy_contract is not None:
                    contract = proxy_contract
                else:
                    return None
    else:
        contract = get_contract_proxy_abi(contract_address, abi_address, blockchain, web3=web3)

        if contract is None:
            return None

    try:
        return contract.encodeABI(fn_name=function_name, args=parameters)
    except Exception:
        logger.exception('Exception in get_data')
        return None


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ACCOUNTS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_token_tx
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_token_tx(token_address, contract_address, block_start, block_end, blockchain):
    data = None

    if blockchain == ETHEREUM:
        data = requests.get(API_ETHERSCAN_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()['result']

    elif blockchain == POLYGON:
        data = requests.get(API_POLYGONSCAN_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_POLSCAN)).json()['result']

    elif blockchain == XDAI:
        data = requests.get(API_GNOSISSCAN_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_GNOSISSCAN)).json()['result']

    elif blockchain == BINANCE:
        data = requests.get(API_BINANCE_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_BINANCE)).json()['result']

    elif blockchain == AVALANCHE:
        data = requests.get(API_AVALANCHE_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_AVALANCHE)).json()['result']

    elif blockchain == FANTOM:
        data = requests.get(API_FANTOM_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_FANTOM)).json()['result']

    elif blockchain == OPTIMISM:
        data = requests.get(API_OPTIMISM_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_OPTIMISM)).json()['result']

    elif blockchain == ROPSTEN:
        data = requests.get(API_ROPSTEN_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()['result']

    elif blockchain == KOVAN:
        data = requests.get(API_KOVAN_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()['result']

    elif blockchain == GOERLI:
        data = requests.get(API_GOERLI_TOKENTX % (
            token_address, contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()['result']

    return data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_tx_list
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_tx_list(contract_address, block_start, block_end, blockchain):
    data = None

    if blockchain == ETHEREUM:
        data = \
            requests.get(API_ETHERSCAN_TXLIST % (contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()[
                'result']

    elif blockchain == POLYGON:
        data = \
            requests.get(API_POLYGONSCAN_TXLIST % (contract_address, block_start, block_end, API_KEY_POLSCAN)).json()[
                'result']

    elif blockchain == XDAI:
        data = \
            requests.get(API_GNOSISSCAN_TXLIST % (contract_address, block_start, block_end, API_KEY_GNOSISSCAN)).json()[
                'result']

    elif blockchain == BINANCE:
        data = \
            requests.get(API_BINANCE_TXLIST % (contract_address, block_start, block_end, API_KEY_BINANCE)).json()[
                'result']

    elif blockchain == AVALANCHE:
        data = \
            requests.get(API_AVALANCHE_TXLIST % (contract_address, block_start, block_end, API_KEY_AVALANCHE)).json()[
                'result']

    elif blockchain == FANTOM:
        data = \
            requests.get(API_FANTOM_TXLIST % (contract_address, block_start, block_end, API_KEY_FANTOM)).json()[
                'result']

    elif blockchain == OPTIMISM:
        data = \
            requests.get(API_OPTIMISM_TXLIST % (contract_address, block_start, block_end, API_KEY_OPTIMISM)).json()[
                'result']

    elif blockchain == ROPSTEN:
        data = \
            requests.get(API_ROPSTEN_TXLIST % (contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()[
                'result']

    elif blockchain == KOVAN:
        data = \
            requests.get(API_KOVAN_TXLIST % (contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()[
                'result']

    elif blockchain == GOERLI:
        data = \
            requests.get(API_GOERLI_TXLIST % (contract_address, block_start, block_end, API_KEY_ETHERSCAN)).json()[
                'result']

    return data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LOGS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_logs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_logs(block_start, block_end, address, topic0, blockchain, **kwargs):
    data = None
    optional_parameters = ''

    for key, value in kwargs.items():

        if key == 'topic1':
            if value:
                optional_parameters += '&topic1=%s' % (value)
                continue

        if key == 'topic2':
            if value:
                optional_parameters += '&topic2=%s' % (value)
                continue

        if key == 'topic3':
            if value:
                optional_parameters += '&topic3=%s' % (value)
                continue

        if key == 'topic0_1_opr':
            if value:
                optional_parameters += '&topic0_1_opr=%s' % (value)
                continue

        if key == 'topic0_2_opr':
            if value:
                optional_parameters += '&topic0_2_opr=%s' % (value)
                continue

        if key == 'topic0_3_opr':
            if value:
                optional_parameters += '&topic0_3_opr=%s' % (value)
                continue

        if key == 'topic1_2_opr':
            if value:
                optional_parameters += '&topic1_2_opr=%s' % (value)
                continue

        if key == 'topic1_3_opr':
            if value:
                optional_parameters += '&topic1_3_opr=%s' % (value)
                continue

        if key == 'topic2_3_opr':
            if value:
                optional_parameters += '&topic2_3_opr=%s' % (value)
                continue

    if blockchain == ETHEREUM:
        data = requests.get(API_ETHERSCAN_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_ETHERSCAN) + optional_parameters).json()['result']

    elif blockchain == POLYGON:
        data = requests.get(API_POLYGONSCAN_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_POLSCAN) + optional_parameters).json()['result']

    elif blockchain == XDAI:
        data = requests.get(API_GNOSISSCAN_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_GNOSISSCAN) + optional_parameters).json()['result']

    elif blockchain == AVALANCHE:
        data = requests.get(API_AVALANCHE_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_AVALANCHE) + optional_parameters).json()['result']

    elif blockchain == BINANCE:
        data = requests.get(API_BINANCE_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_BINANCE) + optional_parameters).json()['result']

    elif blockchain == FANTOM:
        data = requests.get(API_FANTOM_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_FANTOM) + optional_parameters).json()['result']

    elif blockchain == OPTIMISM:
        data = requests.get(API_OPTIMISM_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_OPTIMISM) + optional_parameters).json()['result']

    elif blockchain == ROPSTEN:
        data = requests.get(API_ROPSTEN_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_ETHERSCAN) + optional_parameters).json()['result']

    elif blockchain == KOVAN:
        data = requests.get(API_KOVAN_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_ETHERSCAN) + optional_parameters).json()['result']

    elif blockchain == GOERLI:
        data = requests.get(API_GOERLI_GETLOGS % (
            block_start, block_end, address, topic0, API_KEY_ETHERSCAN) + optional_parameters).json()['result']

    return data


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_block_samples(start_date, samples, blockchain, end_date='latest', utc=0, dates=False):
    start_timestamp = date_to_timestamp(start_date, utc=utc)
    if end_date == 'latest':
        end_timestamp = math.floor(datetime.now().timestamp())
    else:
        end_timestamp = date_to_timestamp(end_date, utc=utc)

    period = int((end_timestamp - start_timestamp) / (samples - 1))

    timestamps = [start_timestamp + i * period for i in range(samples)]

    dates_strings = [datetime.utcfromtimestamp(timestamp + 3600 * utc).strftime('%Y-%m-%d %H:%M:%S') for timestamp in
                     timestamps]

    blocks = [timestamp_to_block(timestamps[i], blockchain) for i in range(samples)]

    if dates is True:
        return [blocks, dates_strings]
    else:
        return blocks


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def is_archival(endpoint) -> bool:
    """
    Checks whether a node is an archival node or a full node.

    :param str endpoint: The node's RPC endpoint to analyse
    :return: True if the node is archival, False if it isn't
    """

    web3 = Web3(Web3.HTTPProvider(endpoint))

    try:
        web3.eth.get_balance('0x849D52316331967b6fF1198e5E32A0eB168D039d', block_identifier=1)
    except ValueError:
        return False
    return True


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_logs_web3
# 'web3' = web3 (Node) -> Improves performance
# 'block' = block identifier used to call the getNode() function
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_logs_web3(address: str, blockchain: str, start_block: Optional[Union[int, str]] = None,
                  topics: Optional[list] = None, block: Optional[Union[int, str]] = None,
                  block_hash: Optional[str] = None, web3=None, index: int = 0) -> dict:
    if web3 == None:
        web3 = get_node(blockchain, block=block, index=index)

    address = web3.to_checksum_address(address)
    return web3.eth.get_logs(
        {'address': address, 'fromBlock': start_block, 'toBlock': block, 'topics': topics, 'blockHash': block_hash})


def get_transaction(tx_hash: str, blockchain: str, block: str = 'latest', index: int = 0) -> dict:
    if web3 == None:
        web3 = get_node(blockchain, block=block, index=index)

    return web3.eth.get_transaction(tx_hash)  
