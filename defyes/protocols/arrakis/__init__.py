from typing import Dict, List

from defabipedia import Chain
from web3 import Web3

from defyes.functions import ensure_a_block_number, get_decimals
from defyes.protocols.arrakis.autogenerated import ArrakisHelperV2, ArrakisV2

ArrakisHelperV2.default_addresses = {
    Chain.GNOSIS: "0x89E4bE1F999E3a58D16096FBe405Fc2a1d7F07D6",
}


def calculate_balances_for_account(block: int, vault_address: str, wallet_address: str) -> List[Dict]:
    """Calculate the balances of an account in a vault.
    From the Arrakis V2 contract, get the total underlying with fees and leftover, calculate the actual liquidity
    and the account's share of the liquidity.

    Returns:
        tuple[float, float]: The account's liquidity for token0 and token1.
    """
    arrakis_v2_helper = ArrakisHelperV2(Chain.GNOSIS, block)
    vault_contract = ArrakisV2(Chain.GNOSIS, block, vault_address)

    result = arrakis_v2_helper.total_underlying_with_fees_and_left_over(vault_address)

    liquidity0 = result[0] - result[4] - result[2]
    liquidity1 = result[1] - result[5] - result[3]

    # Get total supply of shares
    total_shares = vault_contract.total_supply

    # Get account balance of shares
    account_shares = vault_contract.balance_of(wallet_address)

    # Calculate account's share of the liquidity
    account_liquidity0 = liquidity0 * account_shares / total_shares
    account_liquidity1 = liquidity1 * account_shares / total_shares

    token0_address = vault_contract.token0
    token1_address = vault_contract.token1

    return_list = [
        {"address": token0_address, "balance": account_liquidity0},
        {"address": token1_address, "balance": account_liquidity1},
    ]

    return return_list


def get_protocol_data_for(
    blockchain: str,
    wallet: str,
    position_identifier: str,
    block: str = "latest",
    decimals: bool = True,
) -> Dict:
    """Get the data for the Arrakis protocol.
    Args:
        position_identifier (str): The address of the vault you want to get data from.
    """
    block = ensure_a_block_number(block, blockchain)
    wallet = Web3.to_checksum_address(wallet)
    position_identifier = Web3.to_checksum_address(position_identifier)

    balances = calculate_balances_for_account(block, position_identifier, wallet)

    if decimals:
        for balance in balances:
            d = get_decimals(balance["address"], blockchain)
            balance["balance"] = balance["balance"] / 10**d

    data = {
        "blockchain": blockchain,
        "block": block,
        "protocol": "Arrakis",
        "positions_key": None,
        "version": 0,
        "wallet": wallet,
        "decimals": "",
        "positions": {position_identifier: {"underlying": balances}},
    }

    return data
