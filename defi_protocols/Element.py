from defi_protocols.functions import get_node, get_contract, get_decimals, GetNodeIndexError
from defi_protocols.constants import MAX_EXECUTIONS

from defi_protocols.util.topic import DecodeAddressHexor
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

# create, owner
DEPLOYER_ABI = '[{"inputs":[{"internalType":"address","name":"_underlying","type":"address"},{"internalType":"address","name":"_bond","type":"address"},{"internalType":"uint256","name":"_expiration","type":"uint256"},{"internalType":"uint256","name":"_unitSeconds","type":"uint256"},{"internalType":"uint256","name":"_percentFee","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"},{"internalType":"address","name":"_pauser","type":"address"}],"name":"create","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},\
            {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

DEPLOYER_ABI_2 = '[{"inputs":[{"internalType":"address","name":"_underlying","type":"address"},{"internalType":"address","name":"_bond","type":"address"},{"internalType":"uint256","name":"_expiration","type":"uint256"},{"internalType":"uint256","name":"_unitSeconds","type":"uint256"},{"internalType":"uint256","name":"_percentFee","type":"uint256"},{"internalType":"string","name":"_name","type":"string"},{"internalType":"string","name":"_symbol","type":"string"}],"name":"create","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"nonpayable","type":"function"},\
                {"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'

YEAR_IN_SECONDS = 60 * 60 * 24 * 365


def get_tranches(input_data: str, hash: str, underlying_address: str, underlying_address_abi: str, blockchain: str,
                 web3: str, block: int) -> list:
    deploy_contract = get_contract(underlying_address, blockchain, web3=web3, abi=underlying_address_abi, block=block)
    function_output = deploy_contract.decode_function_input(input_data)
    tx = web3.eth.get_transaction_receipt(hash)
    yield_token = get_contract(function_output[1]['_bond'], blockchain, web3=web3, abi=PT_ABI,
                               block=block).functions.interestToken().call()
    pool_id = tx['logs'][0]['topics'][1].hex()
    pool_address = str(DecodeAddressHexor(tx['logs'][0]['topics'][2].hex()))
    addresses = [function_output[1]['_name'], function_output[1]['_bond'], yield_token,
                 function_output[1]['_underlying'], pool_id, pool_address, function_output[1]['_expiration']]
    return addresses


def get_amount(wallet: str, name: str, principal_address: str, yield_address: str, underlying_address: str,
               pool_address: str, pool_id: str, block: int, blockchain: str, web3=None, execution=1, index=0,
               decimals=True) -> list:
    if execution > MAX_EXECUTIONS:
        return None

    balances = []

    try:
        if web3 == None:
            web3 = get_node(blockchain, block=block, index=index)

        wallet = web3.to_checksum_address(wallet)
        pool_token_contract = get_contract(pool_address, blockchain=blockchain, web3=web3, abi=LP_PYV_ABI, block=block)
        pt_token = principal_address
        pt_token_contract = get_contract(pt_token, blockchain, web3=web3, abi=PT_ABI, block=block)
        # yt_token = yield_address
        underlying_token = underlying_address
        # underlying_token_contract = get_contract(underlying_token,blockchain,web3=web3,abi=ABI_TOKEN_SIMPLIFIED,block=block)
        # yt_token_contract = get_contract(yt_token,blockchain,web3=web3,abi=ABI_TOKEN_SIMPLIFIED,block=block)

        pt_token_balanceOf = pt_token_contract.functions.balanceOf(wallet).call(block_identifier=block)

        # yt_token_balanceOf = yt_token_contract.functions.balanceOf(wallet).call()
        # print(yt_token_balanceOf)

        # underlying_token_balanceOf = underlying_token_contract.functions.balanceOf(wallet).call(block_identifier=block)

        pool_total_supply = pool_token_contract.functions.totalSupply().call(block_identifier=block)
        pool_share_wallet = pool_token_contract.functions.balanceOf(wallet).call(
            block_identifier=block) / pool_total_supply

        pool_id = pool_id
        pool_token_vault_address = pool_token_contract.functions.getVault().call()
        pool_token_vault = get_contract(pool_token_vault_address, blockchain, web3=web3, abi=BALANCER_VAULT_ABI,
                                        block=block)
        pool_totals = pool_token_vault.functions.getPoolTokens(pool_id).call(block_identifier=block)
        amount = pt_token_balanceOf + pool_totals[1][0] * pool_share_wallet + pool_totals[1][1] * pool_share_wallet
        token_decimals = get_decimals(pool_address, blockchain, web3=web3)
        if amount != 0:
            if 'Curve' in name or 'crv' in name.lower():
                if decimals == True:
                    curve_amount = unwrap(amount / (10 ** token_decimals), underlying_token, block, blockchain, web3,
                                          decimals=decimals)
                    balances.append(curve_amount)
                else:
                    curve_amount = unwrap(amount, underlying_token, block, blockchain, web3, decimals=decimals)
                    balances.append(curve_amount)
            else:
                if decimals == True:
                    balances.append([underlying_token, amount / (10 ** token_decimals)])
                else:
                    balances.append([underlying_token, amount])

        return balances

    except GetNodeIndexError:
        return get_amount(wallet, name, principal_address, yield_address, underlying_address, pool_address, pool_id,
                          block, blockchain, web3=None, execution=execution + 1, index=0, decimals=decimals)

    except:
        return get_amount(wallet, name, principal_address, yield_address, underlying_address, pool_address, pool_id,
                          block, blockchain, web3=None, execution=execution, index=index + 1, decimals=decimals)


def get_addresses(block: int, blockchain: str, web3=None, execution=1, index=0) -> list:
    if execution > MAX_EXECUTIONS:
        return None
    principal_tokens = []

    try:
        if web3 == None:
            web3 = get_node(blockchain, block=block, index=index)

        underlying_address = web3.to_checksum_address(ELEMENT_DEPLOYER)
        underlying_address2 = web3.to_checksum_address(ELEMENT_DEPLOYER2)
        tranches_list1 = []
        tranches_list2 = []
        tx_list = RequestFromScan(blockchain=blockchain, module='account', action='txlist',
                                  kwargs={'address': underlying_address, 'startblock': 0, 'endblock': block}).request()[
            'result']
        tx_list = [tranches_list1.append(i) for i in tx_list if i[
            'functionName'] == 'create(address _underlying, address _bond, uint256 _expiration, uint256 _unitSeconds, uint256 _percentFee, string _name, string _symbol, address _pauser)']
        tx_list2 = RequestFromScan(blockchain=blockchain, module='account', action='txlist',
                                   kwargs={'address': underlying_address2, 'startblock': 0,
                                           'endblock': block}).request()['result']
        tx_list2 = [tranches_list2.append(i) for i in tx_list2 if i[
            'functionName'] == 'create(address _underlying, address _bond, uint256 _expiration, uint256 _unitSeconds, uint256 _percentFee, string _name, string _symbol)']
        for create in tranches_list1:
            principal_tokens.append(
                get_tranches(create['input'], create['hash'], underlying_address, DEPLOYER_ABI, blockchain, web3,
                             block))
        for create in tranches_list2:
            principal_tokens.append(
                get_tranches(create['input'], create['hash'], underlying_address2, DEPLOYER_ABI_2, blockchain, web3,
                             block))
        return principal_tokens


    except GetNodeIndexError:
        return get_addresses(block, blockchain, index=0, execution=execution + 1)

    except:
        return get_addresses(block, blockchain, index=index + 1, execution=execution)


def underlying(name: str, lptoken_address: str, wallet: str, block: int, blockchain: str, web3=None, execution=1,
               index=0, decimals=True, reward=False) -> list:
    token_addresses = \
    [x for x in get_addresses(block, blockchain, web3=web3, execution=execution, index=index) if x[0] == name][0]
    balances = get_amount(wallet, token_addresses[0], token_addresses[1], token_addresses[2], token_addresses[3],
                          token_addresses[5], token_addresses[4], block, blockchain, web3=web3, execution=execution,
                          index=index, decimals=decimals)
    return balances[0]


def underlying_all(wallet: str, block: int, blockchain: str, web3=None, execution=1, index=0, decimals=True,
                   reward=False) -> list:
    token_addresses = get_addresses(block, blockchain, web3=web3, execution=execution, index=index)
    balances = []
    for x in token_addresses:
        amounts = get_amount(wallet, x[0], x[1], x[2], x[3], x[5], x[4], block, blockchain, web3=web3,
                             execution=execution, index=index, decimals=decimals)
        if amounts:
            balances.append(
                {'protocol': 'Element', 'tranche': x[0], 'amounts': amounts, 'lptoken_address': x[3], 'wallet': wallet})
    return balances

# to test
# name = 'LP Element Principal Token yvCurve-stETH-24FEB23'
# wallet='0x849D52316331967b6fF1198e5E32A0eB168D039d'
# lp = '0x06325440D014e39736583c165C2963BA99fAf14E'
# element = underlying(name,lp,wallet,'latest',blockchain=ETHEREUM)
# # #element3 = underlying_all(wallet,'latest',blockchain=ETHEREUM)
# # #element2 = get_addresses('latest',ETHEREUM)
# print(element)

# calculate spot price:
# t = (expiration - unitseconds time now) / seconds in one year
# with getPoolTokens get supply of stETH and supply of Pt
# calculate stETH(Pt+TotalSupply) * t

# calculate fixed APY
# ((1 - spotprice)/spotprice/timeremaining)*100

# input_data = create['input']
# deploy_contract = get_contract(underlying_address,blockchain,web3=web3,abi=DEPLOYER_ABI, block=block)
# function_output = deploy_contract.decode_function_input(input_data)
# tx = web3.eth.get_transaction_receipt(create['hash'])
# yield_token = get_contract(function_output[1]['_bond'],blockchain,web3=web3,abi=PT_ABI, block=block).functions.interestToken().call()
# pool_id = tx['logs'][0]['topics'][1].hex()
# pool_address = str(DecodeAddressHexor(tx['logs'][0]['topics'][2].hex()))
# principal_tokens.append([function_output[1]['_name'], function_output[1]['_bond'], yield_token , function_output[1]['_underlying'], pool_id, pool_address, function_output[1]['_expiration']])
