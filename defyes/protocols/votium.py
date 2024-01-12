import logging
from decimal import Decimal
from typing import Dict

import requests
from defabipedia import Blockchain, Chain
from web3 import Web3

from defyes.functions import get_contract

logger = logging.getLogger(__name__)

contract_address = "0x378Ba9B73309bE80BF4C2c027aAD799766a7ED5A"


def get_all_rewards(wallet: str, blockchain: Blockchain = Chain.ETHEREUM, block="latest") -> Dict:
    """Get the rewards of all tokens.

    Args:
        list_token_symbols (list): List of tokens.

    Returns:
        list[tuple]: List of token amount and claim status.
    """
    if blockchain != Chain.ETHEREUM:
        raise ValueError("Only ethereum blockchain is supported")
    if block != "latest":
        raise ValueError("only latest is supported")

    wallet = Web3.to_checksum_address(wallet)
    raw_json_url = "https://raw.githubusercontent.com/oo-00/Votium/main/merkle/activeTokens.json"
    response = requests.get(raw_json_url)

    response.raise_for_status()
    json_data = response.json()

    rewards_list = {"protocol": "Votium", "block": "latest", "positions": []}
    position = {"position ID": "rewards", "balances": []}

    for i in range(len(json_data)):
        reward = get_rewards_per_token(wallet, json_data[i]["symbol"], json_data[i]["decimals"])
        if reward is not None:
            balance = {"token": json_data[i]["value"], "balance": Decimal(reward)}
            position["balances"].append(balance)

    rewards_list["positions"].append(position)

    return rewards_list


def get_rewards_per_token(wallet: str, token_symbol: str, decimals: int, round_number: str = "latest") -> float:
    """Get the earned rewards for a specific token. Currently the round_number is always going to be latest.
    The uncompleted idea is to check for past round numbers. As we are based on json files this is brittle and needs
    to be changed.

    Args:
        token_symbol (str): Symbol of the token. eg LDO, FLX
        round_number (str, optional): The number of the round. Has to be a str in the format 'xxxx'
          eg 0001 or 0023  Defaults to 'latest'.

    Returns:
        tuple: (token amount, Claim status)
    """
    wallet = Web3.to_checksum_address(wallet)
    if round_number == "latest":
        round_number = token_symbol

    raw_json_url = f"https://raw.githubusercontent.com/oo-00/Votium/main/merkle/{token_symbol}/{round_number}.json"
    response = requests.get(raw_json_url)

    response.raise_for_status()
    json_data = response.json()

    index_number = json_data["claims"].get(wallet, None)
    if index_number is None:
        logger.warning(f"{token_symbol} was not retrievable. {wallet} has not been found.")
        return None

    hexstr = json_data["claims"][wallet]["amount"]  # get hex amount
    token_amount = Decimal(Web3.to_int(hexstr=hexstr)) / pow(10, decimals)

    if check_claimed_or_unclaimed(wallet, index_number["index"]):
        token_amount = 0

    return token_amount


def check_claimed_or_unclaimed(wallet, index_number):
    """Interact with the contract to see if the funds have been already claimed or not.

    Args:
        wallet (str): Wallet address to check.
        index_number (int): Index number to get the bool value.

    Returns:
        bool: if claimed or not.
    """
    wallet = Web3.to_checksum_address(wallet)

    contract = get_contract(contract_address, Chain.ETHEREUM)
    claimed = contract.functions.isClaimed(wallet, index_number).call()

    return claimed


if __name__ == "__main__":
    print(get_rewards_per_token("0x849d52316331967b6ff1198e5e32a0eb168d039d", "LDO", 18, "0013"))
    print(get_all_rewards(wallet="0x849d52316331967b6ff1198e5e32a0eb168d039d"))
