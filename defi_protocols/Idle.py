import re
import json
import os
from pathlib import Path
from decimal import Decimal
from typing import Union
from web3 import Web3

from defi_protocols.functions import get_node, get_contract, to_token_amount
from defi_protocols.constants import ABI_TOKEN_SIMPLIFIED, ETHEREUM
from defi_protocols.util.topic import decode_address_hexor
from defi_protocols.cache import const_call
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IDLE Deployer
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IDLE Deployer address
DEPLOYER: str = '0x1F98431c8aD98523631AE4a59f267346ea31F984'

GAUGE_CONTROLLER: str = '0xaC69078141f76A1e257Ee889920d02Cc547d632f'

# check for all_markets
IDLE_CONTROLLER: str = '0x275DA8e61ea8E02d51EDd8d0DC5c0E62b4CDB0BE'

CDO_PROXY: str = '0x3C9916BB9498f637e2Fa86C2028e26275Dc9A631'

IDLE_TOKEN: str = '0x875773784Af8135eA0ef43b5a374AaD105c5D39e'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# IDLE CDO ABI - AAStaking, AATranche, BBStaking, BBTranche, getAPR, getIncentiveTokens, priceAA, priceBB, token, unclaimedFees, virtualPrice
ABI_CDO_IDLE: str = '[{"inputs":[],"name":"AAStaking","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"AATranche","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"BBStaking","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"BBTranche","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"_tranche","type":"address"}],"name":"getApr","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"getIncentiveTokens","outputs":[{"internalType":"address[]","name":"","type":"address[]"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"priceAA","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"priceBB","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"token","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},\
            {"inputs":[],"name":"unclaimedFees","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},\
            {"inputs":[{"internalType":"address","name":"_tranche","type":"address"}],"name":"virtualPrice","outputs":[{"internalType":"uint256","name":"_virtualPrice","type":"uint256"}],"stateMutability":"view","type":"function"}]'

# IDLE GAUGE CONTROLLER - n_gauges, gauges
ABI_GAUGE_CONTROLLER: str = '[{"stateMutability":"view","type":"function","name":"n_gauges","inputs":[],"outputs":[{"name":"","type":"int128"}],"gas":2988},\
                        {"stateMutability":"view","type":"function","name":"gauges","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3093}]'

# IDLE GAUGE ABI - decimals, claimed_reward, claimable_reward_write, claimabe_tokens, lp_token, balanceOf, reward_tokens
ABI_GAUGE: str = '[{"stateMutability":"view","type":"function","name":"decimals","inputs":[],"outputs":[{"name":"","type":"uint256"}],"gas":288},\
            {"stateMutability":"view","type":"function","name":"claimed_reward","inputs":[{"name":"_addr","type":"address"},{"name":"_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3066},\
            {"stateMutability":"view","type":"function","name":"claimable_reward_write","inputs":[{"name":"_addr","type":"address"},{"name":"_token","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":1209922},\
            {"stateMutability":"view","type":"function","name":"claimable_tokens","inputs":[{"name":"addr","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3046449},\
            {"stateMutability":"view","type":"function","name":"lp_token","inputs":[],"outputs":[{"name":"","type":"address"}],"gas":3138},\
            {"stateMutability":"view","type":"function","name":"balanceOf","inputs":[{"name":"arg0","type":"address"}],"outputs":[{"name":"","type":"uint256"}],"gas":3473},\
            {"stateMutability":"view","type":"function","name":"reward_tokens","inputs":[{"name":"arg0","type":"uint256"}],"outputs":[{"name":"","type":"address"}],"gas":3723}]'

ABI_CDO_PROXY: str = '[{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"proxy","type":"address"}],"name":"CDODeployed","type":"event"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"},{"internalType":"address","name":"admin","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"deployCDO","outputs":[],"stateMutability":"nonpayable","type":"function"}]'


# function for getting all addresses you need to get underlying
def get_addresses(block: Union[int, str], blockchain: str, web3=None,
                  decimals: bool = True) -> dict:
    addresses = {"tranches": []}

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    cdo_events = web3.eth.get_logs({'fromBlock': 0, 'toBlock': block, 'address': CDO_PROXY})
    gauges = get_gauges(block, blockchain, web3=web3)
    for event in cdo_events:
        cdo_address = decode_address_hexor(event['data'])
        cdo_contract = get_contract(cdo_address, blockchain, web3=web3, abi=ABI_CDO_IDLE, block=block)
        aa_token = const_call(cdo_contract.functions.AATranche())
        bb_token = const_call(cdo_contract.functions.BBTranche())
        gauge_contract_address = [x[0] for x in gauges if re.match(aa_token, x[1])]
        if gauge_contract_address:
            gauge_contract_address = gauge_contract_address[0]
        else:
            gauge_contract_address = None
        underlying_token = const_call(cdo_contract.functions.token())
        addresses['tranches'].append({'underlying_token': underlying_token, 'CDO address': cdo_address,
                                      'AA tranche': {'aa_token': aa_token, 'aa_gauge': gauge_contract_address},
                                      'bb token': bb_token})
    return addresses


def get_gauges(block: Union[int, str], blockchain: str, web3=None, decimals=True) -> list:
    gauges = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    gauge_controller_contract = get_contract(GAUGE_CONTROLLER, blockchain, web3=web3, abi=ABI_GAUGE_CONTROLLER,
                                             block=block)
    n_gauges = gauge_controller_contract.functions.n_gauges().call()
    for i in range(0, n_gauges):
        gauge_address = gauge_controller_contract.functions.gauges(i).call()
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)
        lp_token_address = gauge_contract.functions.lp_token().call()
        gauges.append([gauge_address, lp_token_address])
    return gauges


def get_all_rewards(wallet: str, gauge_address: str, block: Union[int, str], blockchain: str, web3=None,
                    decimals: bool = True) -> list:
    rewards = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)
    idle_rewards = gauge_contract.functions.claimable_tokens(wallet).call(block_identifier=block)
    rewards.append([IDLE_TOKEN, to_token_amount(IDLE_TOKEN, idle_rewards, blockchain, web3, decimals)])

    for i in range(0, 10):
        reward_tokens = gauge_contract.functions.reward_tokens(i).call()
        if reward_tokens == '0x0000000000000000000000000000000000000000':
            break
        claimable_rewards = gauge_contract.functions.claimable_reward_write(wallet, reward_tokens).call(block_identifier=block)
        claimed_rewards = gauge_contract.functions.claimed_reward(wallet, reward_tokens).call(block_identifier=block)
        all_rewards = claimable_rewards + claimed_rewards
        rewards.append([reward_tokens, to_token_amount(reward_tokens, all_rewards, blockchain, web3, decimals)])

    return rewards


def get_amounts(underlying_address: str, cdo_address: str, aa_address: str, bb_address: str, gauge_address: str,
                wallet: str, block: Union[int, str], blockchain: str, web3=None, decimals: bool = True) -> list:
    balances = []

    if web3 is None:
        web3 = get_node(blockchain, block=block)

    wallet = Web3.to_checksum_address(wallet)
    cdo_contract = get_contract(cdo_address, blockchain, web3=web3, abi=ABI_CDO_IDLE, block=block)
    aa_contract = get_contract(aa_address, blockchain, web3=web3, abi=ABI_TOKEN_SIMPLIFIED, block=block)
    bb_contract = get_contract(bb_address, blockchain, web3=web3, abi=ABI_TOKEN_SIMPLIFIED, block=block)
    if gauge_address:
        gauge_contract = get_contract(gauge_address, blockchain, web3=web3, abi=ABI_GAUGE, block=block)
        gauge_balance = gauge_contract.functions.balanceOf(wallet).call(block_identifier=block) * (
                    cdo_contract.functions.virtualPrice(aa_address).call(block_identifier=block) / Decimal(10 ** 18))
    else:
        gauge_balance = 0
    aa_balance = aa_contract.functions.balanceOf(wallet).call(block_identifier=block) * (
                cdo_contract.functions.virtualPrice(aa_address).call(block_identifier=block) / Decimal(10 ** 18))
    bb_balance = bb_contract.functions.balanceOf(wallet).call(block_identifier=block) * (
                cdo_contract.functions.virtualPrice(bb_address).call(block_identifier=block) / Decimal(10 ** 18))

    for balance in [aa_balance, bb_balance, gauge_balance]:
        if balance != 0:
            balances.append([underlying_address, to_token_amount(aa_address, balance, blockchain, web3, decimals)])

    return balances


def underlying(token_address: str, wallet: str, block: Union[int, str], blockchain: str, web3=None,
               decimals: bool = True, db: bool = True, rewards: bool = False) -> list:
    if web3 is None:
        web3 = get_node(blockchain, block)
    token_address = Web3.to_checksum_address(token_address)

    if db:
        file = open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Idle_db.json')
        data = json.load(file)
        tranches_list = data['tranches']
        addresses = [x for x in tranches_list if x['underlying_token'] == token_address][0]
    else:
        addresses = [x for x in get_addresses(block, blockchain, web3=web3) if x['underlying_token'] == token_address][
            0]
    amounts = get_amounts(addresses['underlying_token'], addresses['CDO address'], addresses['AA tranche']['aa_token'],
                          addresses['bb token'], addresses['AA tranche']['aa_gauge'],
                          wallet, block, blockchain, web3, decimals)
    if rewards:
        rewards = get_all_rewards(wallet, addresses['AA tranche']['aa_gauge'], block, blockchain, web3,
                                  decimals=decimals)
        amounts.append(rewards)
    return amounts


def underlying_all(wallet: str, block: Union[int, str], blockchain: str, web3=None,
                   decimals: bool = True, db: bool = True, rewards: bool = False) -> list:
    balances_all = []
    if db:
        file = open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Idle_db.json')
        data = json.load(file)
        addresses = data['tranches']
    else:
        addresses = get_addresses(block, blockchain, web3=web3)

    for address in addresses:
        amounts = get_amounts(address['underlying_token'], address['CDO address'], address['AA tranche']['aa_token'],
                              address['bb token'], address['AA tranche']['aa_gauge'],
                              wallet, block, blockchain, web3, decimals)
        if amounts:
            if rewards and address['AA tranche']['aa_gauge'] != None:
                rewards = get_all_rewards(wallet, address['AA tranche']['aa_gauge'], block, blockchain, web3,
                                          decimals=decimals)
                amounts.append(rewards)
            balances_all.append(amounts)
    return balances_all


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_db (function to update database with addresses from all tranches that have been deployed)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_db() -> dict:
    """

    :return:
    """
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + '/db/Idle_db.json', 'w') as db_file:
        addresses = get_addresses('latest', ETHEREUM)
        json.dump(addresses, db_file, indent=4)


# wallet = '0x849d52316331967b6ff1198e5e32a0eb168d039d'
# gauge = '0x675eC042325535F6e176638Dd2d4994F645502B9'
# rewors = get_all_rewards(wallet, gauge, 'latest', ETHEREUM)
# print(rewors)

# CDO_address = '0xae7ab96520de3a18e5e111b5eaab095312d7fe84'
# wallet = '0x849D52316331967b6fF1198e5E32A0eB168D039d'

# haha = underlying(token_address=CDO_address, wallet=wallet,block='latest',blockchain=ETHEREUM,rewards=True)
# print(haha)

# yo = get_gauges('latest',ETHEREUM)
# print(yo)

# aabhar = get_addresses('latest',ETHEREUM)
# print(aabhar)

# aabhar2 = update_db()
# print(aabhar2)
