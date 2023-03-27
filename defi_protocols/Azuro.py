from defi_protocols.functions import get_node, get_contract, get_decimals, get_logs_web3, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS
from typing import Union
from defi_protocols.util.topic import TopicCreator, AddressHexor

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# RealT Token Address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AZURO Token Address
AZURO_POOL_V1: str = '0xac004b512c33d029cf23abf04513f1f380b3fd0a'

# AZURO POOL V2
AZURO_POOL_V2: str = '0x204e7371ade792c5c006fb52711c50a7efc843ed'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# AZURO token contract ABI - balanceOf, nodeWithdrawView, ownerOf, tokenOfOwnerByIndex, token, withdrawals, withdrawPayout, withdrawLiquidity
AZURO_POOL_ABI: str = '[{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint48","name":"leaf","type":"uint48"}],"name":"nodeWithdrawView","outputs":[{"internalType":"uint128","name":"withdrawAmount","type":"uint128"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint48","name":"","type":"uint48"}],"name":"withdrawals","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint48","name":"depNum","type":"uint48"},{"internalType":"uint40","name":"percent","type":"uint40"}],"name":"withdrawLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},\
                        {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"withdrawPayout","outputs":[],"stateMutability":"nonpayable","type":"function"}]'

EVENT_LIQUIDITY_ADDED_V1 = 'LiquidityAdded (index_topic_1 address account, uint256 amount, uint48 leaf)'
EVENT_LIQUIDITY_ADDED_V2 = 'LiquidityAdded (index_topic_1 address account, index_topic_2 uint48 leaf, uint256 amount)'
EVENT_LIQUIDITY_REMOVED_V1 = 'LiquidityRemoved (index_topic_1 address account, index_topic_2 uint48 leaf, uint256 amount)'
EVENT_LIQUIDITY_REMOVED_V2 = 'LiquidityRemoved (index_topic_1 address account, index_topic_2 uint48 leaf, uint256 amount)'


def get_deposit(wallet: str, nftid: str, contract_address: str, block: Union[int, str], blockchain: str, web3=None,
                execution: int = 1, index: int = 0) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        azuro = web3.to_checksum_address(contract_address)
        wallethex = str(AddressHexor(wallet))
        nfthex = '0x00000000000000000000000000000000000000000000000000000' + hex(nftid)[2:]
        amount = 0
        if contract_address == AZURO_POOL_V1:
            topic0 = str(TopicCreator(EVENT_LIQUIDITY_ADDED_V1))
            logs = get_logs_web3(address=azuro, blockchain=blockchain, start_block=0, topics=[topic0, wallethex],
                                 block=block, web3=web3, index=index)
            for log in logs:
                if log['data'][-11:] == nfthex[-11:]:
                    amount = amount + int(log['data'][:66], 16)
            topic0 = str(TopicCreator(EVENT_LIQUIDITY_REMOVED_V1))
            logs = get_logs_web3(address=azuro, blockchain=blockchain, start_block=0,
                                 topics=[topic0, wallethex, nfthex], block=block, web3=web3, index=index)
            for log in logs:
                amount = amount - int(log['data'], 16)

        else:
            topic0 = str(TopicCreator(EVENT_LIQUIDITY_ADDED_V2))
            logs = get_logs_web3(address=azuro, blockchain=blockchain, start_block=0,
                                 topics=[topic0, wallethex, nfthex], block=block, web3=web3, index=index)
            for log in logs:
                amount = amount + int(log['data'], 16)
            topic0 = str(TopicCreator(EVENT_LIQUIDITY_REMOVED_V2))
            logs = get_logs_web3(address=azuro, blockchain=blockchain, start_block=0,
                                 topics=[topic0, wallethex, nfthex], block=block, web3=web3, index=index)
            for log in logs:
                amount = amount - int(log['data'], 16)
        return amount

    except GetNodeIndexError:
        return get_deposit(wallet, nftid, block, blockchain, index=0, execution=execution + 1)

    except:
        return get_deposit(wallet, nftid, block, blockchain, index=index + 1, execution=execution)


def get_amount(wallet: str, contract_1: str, contract_2: str, nftid: int, block: Union[int, str], blockchain: str,
               web3=None, execution: int = 1, index: int = 0, decimals: bool = True, rewards: bool = False) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)
        try:
            owner_1 = contract_1.functions.ownerOf(nftid).call()
        except:
            owner_1 = None
        try:
            owner_2 = contract_2.functions.ownerOf(nftid).call()
        except:
            owner_2 = None
        if owner_1 == wallet:
            node_withdraw1 = contract_1.functions.nodeWithdrawView(nftid).call()
            deposit = get_deposit(wallet, nftid, AZURO_POOL_V1, block, blockchain, web3)
        else:
            node_withdraw1 = 0
        if owner_2 == wallet:
            node_withdraw2 = contract_2.functions.nodeWithdrawView(nftid).call()
            deposit = get_deposit(wallet, nftid, AZURO_POOL_V2, block, blockchain, web3)
        else:
            node_withdraw2 = 0
        token = contract_1.functions.token().call()
        token_decimals = get_decimals(token, blockchain, block=block)
        balance = node_withdraw1 + node_withdraw2
        reward = balance - deposit
        if decimals == True and rewards == True:
            balances.append([token, balance / (10 ** token_decimals)])
            balances.append([token, reward / (10 ** token_decimals)])
        elif decimals == True and rewards == False:
            balances.append([token, balance / (10 ** token_decimals)])
        elif decimals == False and rewards == True:
            balances.append([token, balance])
            balances.append([token, reward])
        else:
            balances.append([token, balance])
        return balances



    except GetNodeIndexError:
        return get_amount(wallet, contract_1, contract_2, nftid, block, blockchain, decimals=decimals, index=0,
                          execution=execution + 1)

    except:
        return get_amount(wallet, contract_1, contract_2, nftid, block, blockchain, decimals=decimals, index=index + 1,
                          execution=execution)


def underlying(wallet: str, nftid: int, block: Union[int, str], blockchain: str, web3=None, execution: int = 1,
               index: int = 0, decimals: bool = True, rewards: bool = False) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        pool_address_v1 = get_contract(AZURO_POOL_V1, blockchain, web3=web3, abi=AZURO_POOL_ABI, block=block)
        pool_address_v2 = get_contract(AZURO_POOL_V2, blockchain, web3=web3, abi=AZURO_POOL_ABI, block=block)
        balances = get_amount(wallet, pool_address_v1, pool_address_v2, nftid, block, blockchain, web3,
                              decimals=decimals, rewards=rewards)
        return balances

    except GetNodeIndexError:
        return underlying(wallet, nftid, block, blockchain, decimals=decimals, index=0, execution=execution + 1,
                          rewards=rewards)

    except:
        return underlying(wallet, nftid, block, blockchain, decimals=decimals, index=index + 1, execution=execution,
                          rewards=rewards)


def underlying_all(wallet: str, block: Union[int, str], blockchain: str, web3=None, execution: int = 1, index: int = 0,
                   decimals: bool = True, rewards: bool = False) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    results = []

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        pool_address_v1 = get_contract(AZURO_POOL_V1, blockchain, web3=web3, abi=AZURO_POOL_ABI, block=block)
        pool_address_v2 = get_contract(AZURO_POOL_V2, blockchain, web3=web3, abi=AZURO_POOL_ABI, block=block)
        balance_of_pool1 = pool_address_v1.functions.balanceOf(wallet).call()
        balance_of_pool2 = pool_address_v2.functions.balanceOf(wallet).call()
        for i in range(0, balance_of_pool1):
            nftid = pool_address_v1.functions.tokenOfOwnerByIndex(wallet, i).call()
            results.append([get_amount(wallet, pool_address_v1, pool_address_v2, nftid, block, blockchain, web3,
                                       decimals=decimals, rewards=rewards)][0])
        for i in range(0, balance_of_pool2):
            nftid = pool_address_v2.functions.tokenOfOwnerByIndex(wallet, i).call()
            results.append([get_amount(wallet, pool_address_v1, pool_address_v2, nftid, block, blockchain, web3,
                                       decimals=decimals, rewards=rewards)][0])
        return results

    except GetNodeIndexError:
        return underlying_all(wallet, block, blockchain, decimals=decimals, index=0, execution=execution + 1)

    except:
        return underlying_all(wallet, block, blockchain, decimals=decimals, index=index + 1, execution=execution)

# from web3 import Web3, HTTPProvider
# # Initialize a Web3.py instance
# apiKey = "twj7sBzB1_Njwoejwj0EFM-_x-TKJkZb"
# nftid = 1099511627781
# web3 = Web3(Web3.HTTPProvider('https://rpc.gnosischain.com/'))
# wallet = web3.to_checksum_address('0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f')
# azuro = web3.to_checksum_address(AZURO_POOL_V2)
# wallethex = str(AddressHexor(wallet))
# print(wallethex)
# nfthex = '0x00000000000000000000000000000000000000000000000000000' + hex(nftid)[2:]
# topic0 = '0x04aea1979a2b879b0578efc9fb3e03cd6ae3bdc964f047e81f526ea2350967e5'
# events = web3.eth.get_logs({'address': azuro, 'fromBlock':0, 'toBlock':'latest', 'topics': [topic0,wallethex,nfthex]})
# print(events[0]['data'])
# amount = events[0]['data']
# print(int(amount, 16))


# wallet = '0x458cd345b4c05e8df39d0a07220feb4ec19f5e6f'
# nftid = 1099511627781
# yo = underlying_all(wallet,'latest',XDAI,rewards=True)
# print(yo)
# aabhar = get_deposit(wallet,nftid,'latest',XDAI)
# print(aabhar)
