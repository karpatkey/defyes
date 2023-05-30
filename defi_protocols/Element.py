from dataclasses import dataclass
from decimal import Decimal
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, to_token_amount
from defi_protocols.util.topic import decode_address_hexor
from defi_protocols.util.api import RequestFromScan
from defi_protocols.Curve import unwrap

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# LITERALS
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Contracts for calling liquidity pools and underlying tokens
ELEMENT_TRANCHE_ADDRESS = '0x17cb1f74119dfe718f786a05bea7d71bf438678c'
ELEMENT_LP_PYVCURVE = '0x07f589eA6B789249C83992dD1eD324c3b80FD06b'
ELEMENT_YVCURVE = '0xcD62f09681dCBB9fbc5bA8054B52F414Cb28960A'
BALANCER_POOL_ADDRESS = '0xBA12222222228d8Ba445958a75a0704d566BF2C8'
ELEMENT_DEPLOYER = '0xe88628700eae9213169d715148ac5a5f47b5dcd9'
ELEMENT_DEPLOYER2 = '0xb7561f547f3207edb42a6afa42170cd47add17bd'

DEPLOYER_FUNCNAMES = {
    ELEMENT_DEPLOYER: 'create(address _underlying, address _bond, uint256 _expiration, uint256 _unitSeconds, uint256 _percentFee, string _name, string _symbol, address _pauser)',
    ELEMENT_DEPLOYER2: 'create(address _underlying, address _bond, uint256 _expiration, uint256 _unitSeconds, uint256 _percentFee, string _name, string _symbol)'
}

# create, owner
DEPLOYER_ABIS = {
    ELEMENT_DEPLOYER: '[{"inputs":[{"internalType":"address","name":"_underlying","type":"address"},{"internalType":"address","name":"_bond","type":"address"},{"internalType":"uint256","name":"_expiration","type":"uint256"},{"internalType":"uint256","name":"_unitSeconds","type":"uint256"},{"internalType":"uint256","name":"_percentFee","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_pauser","type":"address"}],"name":"create","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},\
            {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]',
    ELEMENT_DEPLOYER2: '[{"inputs":[{"internalType":"address","name":"_underlying","type":"address"},{"internalType":"address","name":"_bond","type":"address"},{"internalType":"uint256","name":"_expiration","type":"uint256"},{"internalType":"uint256","name":"_unitSeconds","type":"uint256"},{"internalType":"uint256","name":"_percentFee","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"}],"name":"create","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},\
                {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
}
# balanceOf, interestToken, underlying
PT_ABI = '[{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"interestToken","outputs":[{"internalType":"contract IInterestToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"underlying","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unlockTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# TotalSupply, balanceOf, getPoolID, , getVault, expiration, unitseconds, bond
# expiration - block.timestamp, *1e18, divdown by unitseconds *1e18,
LP_PYV_ABI = '[{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"getPoolId","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"getVault","outputs":[{"internalType":"contract IVault","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"expiration","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
                {"inputs":[],"name":"unitSeconds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}, \
                {"inputs":[],"name":"bond","outputs":[{"internalType":"contract IERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bondDecimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'

# getPoolTokens
BALANCER_VAULT_ABI = '[{"inputs":[{"internalType":"bytes32","name":"poolId","type":"bytes32"}],"name":"getPoolTokens","outputs":[{"internalType":"contract IERC20[]","name":"tokens","type":"address[]"},{"internalType":"uint256[]","name":"balances","type":"uint256[]"},{"internalType":"uint256","name":"lastChangeBlock","type":"uint256"}],"stateMutability":"view","type":"function"}]'


YEAR_IN_SECONDS = 60 * 60 * 24 * 365


@dataclass
class Tranche:
    name: str
    principal_token: str
    yield_token: str
    underlying: str
    pool_id: str
    pool_addr: str
    expiration: int

    def to_list(self):
        return list(self.__dict__.values())


def get_tranche(input_data: str, hash: str, underlying_address: str, underlying_address_abi: str, blockchain: str,
                web3: str, block: int) -> Tranche:
    deploy_contract = get_contract(underlying_address, blockchain, web3=web3, abi=underlying_address_abi, block=block)
    function_output = deploy_contract.decode_function_input(input_data)

    yield_token_contract = get_contract(function_output[1]['_bond'],
                                        blockchain,
                                        web3=web3,
                                        abi=PT_ABI,
                                        block=block)

    yield_token = yield_token_contract.functions.interestToken().call()

    tx = web3.eth.get_transaction_receipt(hash)
    pool_id = tx['logs'][0]['topics'][1].hex()
    pool_address = decode_address_hexor(tx['logs'][0]['topics'][2])

    return Tranche(function_output[1]['_name'],
                   function_output[1]['_bond'],
                   yield_token,
                   function_output[1]['_underlying'],
                   pool_id,
                   pool_address,
                   function_output[1]['_expiration'])


def get_tranches(block: int, blockchain: str, web3) -> list:
    tranches = []
    for deployer in [ELEMENT_DEPLOYER, ELEMENT_DEPLOYER2]:
        underlying_address = Web3.to_checksum_address(deployer)
        tx_list = RequestFromScan(blockchain=blockchain, module='account', action='txlist',
                                 kwargs={'address': underlying_address,
                                         'startblock': 0,
                                         'endblock': block}).request()['result']

        for item in tx_list:
            if item['functionName'] == DEPLOYER_FUNCNAMES[deployer]:
                tranches.append(get_tranche(item['input'],
                                            item['hash'],
                                            underlying_address,
                                            DEPLOYER_ABIS[deployer],
                                            blockchain,
                                            web3,
                                            block)
                                )

    return tranches


def get_addresses(block: int, blockchain: str, web3=None) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    principal_tokens = get_tranches(block, blockchain, web3)

    return [pt.to_list() for pt in principal_tokens]


def get_amount(wallet: str, name: str, pt_token: str, underlying_token: str, pool_address: str, pool_id: str,
               block: int, blockchain: str, web3=None, decimals=True) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)

    pt_token_contract = get_contract(pt_token, blockchain, web3=web3, abi=PT_ABI, block=block)
    pt_token_balanceOf = pt_token_contract.functions.balanceOf(wallet).call(block_identifier=block)

    pool_token_contract = get_contract(pool_address, blockchain=blockchain, web3=web3, abi=LP_PYV_ABI, block=block)
    pool_total_supply = pool_token_contract.functions.totalSupply().call(block_identifier=block)
    pool_share_wallet = pool_token_contract.functions.balanceOf(wallet).call(block_identifier=block) / Decimal(pool_total_supply)

    pool_token_vault_address = pool_token_contract.functions.getVault().call()
    pool_token_vault = get_contract(pool_token_vault_address, blockchain, web3=web3, abi=BALANCER_VAULT_ABI, block=block)
    pool_totals = pool_token_vault.functions.getPoolTokens(pool_id).call(block_identifier=block)

    amount = pt_token_balanceOf + pool_totals[1][0] * pool_share_wallet + pool_totals[1][1] * pool_share_wallet
    balance = []
    if amount != 0:
        if 'Curve' in name or 'crv' in name.lower():
            balance = unwrap(to_token_amount(pool_address, amount, blockchain, web3, decimals),
                             underlying_token,
                             block,
                             blockchain,
                             web3,
                             decimals=decimals)
        else:
            balance = [underlying_token, to_token_amount(pool_address, amount, blockchain, web3, decimals)]

    return balance


def underlying(name: str, wallet: str, block: int, blockchain: str, web3=None, decimals=True) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    balances = []
    for tranche in get_tranches(block, blockchain, web3):
        if tranche.name == name:
            balances = get_amount(wallet,
                                  tranche.name,
                                  tranche.principal_token,
                                  tranche.underlying,
                                  tranche.pool_addr,
                                  tranche.pool_id,
                                  block,
                                  blockchain,
                                  web3=web3,
                                  decimals=decimals)
    return balances


def underlying_all(wallet: str, block: int, blockchain: str, web3=None, decimals=True) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block=block)

    balances = []
    for tranche in get_tranches(block, blockchain, web3):
        amounts = get_amount(wallet,
                             tranche.name,
                             tranche.principal_token,
                             tranche.underlying,
                             tranche.pool_addr,
                             tranche.pool_id,
                             block,
                             blockchain,
                             web3=web3,
                             decimals=decimals)
        if amounts:
            balances.append(
                {'protocol': 'Element',
                 'tranche': tranche.name,
                 'amounts': amounts,
                 'lptoken_address': tranche.underlying,
                 'wallet': wallet}
            )
    return balances
