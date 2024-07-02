from dataclasses import dataclass, field

from karpatkit.node import get_node
from web3 import Web3
from web3.exceptions import BadFunctionCallOutput, ContractLogicError

from defyes.functions import get_contract, get_logs_web3, to_token_amount
from defyes.topic import address_hexor, topic_creator

POOL_ADDR_V1 = "0xac004b512c33D029cf23ABf04513f1f380B3FD0a"
POOL_ADDR_V2 = "0x204e7371Ade792c5C006fb52711c50a7efC843ed"


@dataclass
class AzuroPools:
    addr: str
    liquidity_added_topic: str = field(init=False)
    liquidity_removed_topic: str = field(init=False)
    first_block: int = field(init=False)
    version: int = field(init=False)

    def __post_init__(self):
        assert self.addr in [POOL_ADDR_V1, POOL_ADDR_V2], "Wrong Azuro pool address provided"
        if self.addr == POOL_ADDR_V1:
            self.version = 1
            liquidity_added_event = "LiquidityAdded (index_topic_1 address account, uint256 amount, uint48 leaf)"
            liquidity_removed_event = (
                "LiquidityRemoved (index_topic_1 address account, index_topic_2 uint48 leaf, uint256 amount)"
            )
            self.first_block = 22535363
        else:
            self.version = 2
            liquidity_added_event = (
                "LiquidityAdded (index_topic_1 address account, index_topic_2 uint48 leaf, uint256 amount)"
            )
            liquidity_removed_event = (
                "LiquidityRemoved (index_topic_1 address account, index_topic_2 uint48 leaf, uint256 amount)"
            )
            self.first_block = 26026907

        self.liquidity_added_topic = topic_creator(liquidity_added_event)
        self.liquidity_removed_topic = topic_creator(liquidity_removed_event)


# AZURO token contract ABI
# balanceOf, nodeWithdrawView, ownerOf, tokenOfOwnerByIndex, token, withdrawals, withdrawPayout, withdrawLiquidity
AZURO_POOL_ABI: str = (
    '[{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint48","name":"leaf","type":"uint48"}],"name":"nodeWithdrawView","outputs":[{"internalType":"uint128","name":"withdrawAmount","type":"uint128"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint48","name":"","type":"uint48"}],"name":"withdrawals","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},\
                        {"inputs":[{"internalType":"uint48","name":"depNum","type":"uint48"},{"internalType":"uint40","name":"percent","type":"uint40"}],"name":"withdrawLiquidity","outputs":[],"stateMutability":"nonpayable","type":"function"},\
                        {"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"withdrawPayout","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
)


def get_deposit(
    wallet: str, nftid: int, contract_address: str, block: int | str, blockchain: str, web3: Web3 = None
) -> list:
    if web3 is None:
        web3 = get_node(blockchain)

    azuro_pool = AzuroPools(contract_address)
    wallet = Web3.to_checksum_address(wallet)

    wallethex = address_hexor(wallet)
    nfthex = "0x00000000000000000000000000000000000000000000000000000" + hex(nftid)[2:]

    amount = 0
    add_logs = get_logs_web3(
        blockchain=blockchain,
        address=azuro_pool.addr,
        block_start=azuro_pool.first_block,
        block_end=block,
        topics=[azuro_pool.liquidity_added_topic, wallethex],
        web3=web3,
    )
    for log in add_logs:
        if azuro_pool.version == 1 and log["data"].hex()[-11:] == nfthex[-11:]:
            amount = amount + int(log["data"].hex()[:66], 16)
        elif azuro_pool.version == 2:
            amount = amount + int(log["data"].hex(), 16)
    remove_logs = get_logs_web3(
        blockchain=blockchain,
        address=azuro_pool.addr,
        block_start=azuro_pool.first_block,
        block_end=block,
        topics=[azuro_pool.liquidity_removed_topic, wallethex, nfthex],
        web3=web3,
    )
    for log in remove_logs:
        amount = amount - int(log["data"].hex(), 16)

    return amount


def underlying(
    wallet: str,
    nftid: int,
    block: int | str,
    blockchain: str,
    web3: Web3 = None,
    decimals: bool = True,
    rewards: bool = False,
) -> list:
    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)

    pool_v1_contract = get_contract(POOL_ADDR_V1, blockchain, web3=web3, abi=AZURO_POOL_ABI)
    pool_v2_contract = get_contract(POOL_ADDR_V2, blockchain, web3=web3, abi=AZURO_POOL_ABI)

    balance = 0
    reward = 0
    for contract in [pool_v1_contract, pool_v2_contract]:
        try:
            owner = contract.functions.ownerOf(nftid).call(block_identifier=block)
        except (ContractLogicError, BadFunctionCallOutput):
            owner = None
        if owner == wallet:
            node_withdraw = contract.functions.nodeWithdrawView(nftid).call(block_identifier=block)
            deposit = get_deposit(wallet, nftid, contract.address, block, blockchain, web3)
            balance += node_withdraw
            reward += node_withdraw - deposit

    token = pool_v1_contract.functions.token().call(block_identifier=block)
    balance = [token, to_token_amount(token, balance, blockchain, web3, decimals)]
    reward = [token, to_token_amount(token, reward, blockchain, web3, decimals)]

    balances = [balance]
    if rewards:
        balances = [balance, reward]

    return balances


def underlying_all(
    wallet: str,
    block: int | str,
    blockchain: str,
    web3: Web3 = None,
    decimals: bool = True,
    rewards: bool = False,
) -> list:
    if web3 is None:
        web3 = get_node(blockchain)

    wallet = Web3.to_checksum_address(wallet)
    pool_v1_contract = get_contract(POOL_ADDR_V1, blockchain, web3=web3, abi=AZURO_POOL_ABI)
    assets_pool1 = pool_v1_contract.functions.balanceOf(wallet).call(block_identifier=block)

    pool_v2_contract = get_contract(POOL_ADDR_V2, blockchain, web3=web3, abi=AZURO_POOL_ABI)
    assets_pool2 = pool_v2_contract.functions.balanceOf(wallet).call(block_identifier=block)

    results = []
    for assets_in_pool in [assets_pool1, assets_pool2]:
        for asset in range(assets_in_pool):
            nftid = pool_v1_contract.functions.tokenOfOwnerByIndex(wallet, asset).call(block_identifier=block)
            results.append([underlying(wallet, nftid, block, blockchain, web3, decimals=decimals, rewards=rewards)][0])

    return results
