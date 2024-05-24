from decimal import Decimal

from web3 import Web3

from defyes.functions import get_decimals
from defyes.protocols.uniswapv2.autogenerated import LpToken


class Pool(LpToken):
    """Class to get the data of a Uniswap V2 pool.
    It inherits from the LpToken class that is autogenerated from the UniswapV2 LP token contract.
    There's no default address for the contract, so it needs to be passed as an argument.
    """

    def get_lp_token_data(self) -> dict:
        """Collects the data of the LP token from the contract."""
        lp_token_data = {}

        lp_token_data["decimals"] = self.decimals
        lp_token_data["total_supply"] = self.total_supply
        lp_token_data["token0"] = self.token0
        lp_token_data["token1"] = self.token1
        lp_token_data["reserves"] = self.get_reserves

        return lp_token_data


def get_balances(wallet, lptoken_address, block, blockchain, decimals=True):
    """
    Retrieves the balance information for a given wallet and liquidity pool token (LP token).

    It then retrieves the LP token data. The function calculates the fraction of the total pool balance.
    It then iterates over each reserve in the LP token data.
    For each reserve, it tries to get the corresponding token.

    Returns:
        list: A list of dictionaries. Each dictionary contains the address and balance.

    Raises:
        AttributeError: If a token does not have a corresponding attribute in the LP token contract.
    """
    underlying_balances = []

    wallet = Web3.to_checksum_address(wallet)
    lptoken_address = Web3.to_checksum_address(lptoken_address)

    pool = Pool(blockchain, block, lptoken_address)
    lptoken_data = pool.get_lp_token_data()

    lptoken_data["balanceOf"] = pool.balance_of(wallet)
    holding_balance = {
        "address": lptoken_address,
        "balance": lptoken_data["balanceOf"] / 10**18 if decimals else lptoken_data["balanceOf"],
    }

    pool_balance_fraction = lptoken_data["balanceOf"] / lptoken_data["total_supply"]

    for i in range(len(lptoken_data["reserves"])):
        token_address = lptoken_data.get("token" + str(i))
        if token_address is None:
            continue

        token_decimals = Decimal(10 ** get_decimals(token_address, blockchain) if decimals else 0)

        token_balance = Decimal(lptoken_data["reserves"][i]) / token_decimals * Decimal(pool_balance_fraction)

        underlying_balances.append({"address": token_address, "balance": token_balance})

    return underlying_balances, holding_balance


def get_data_protocol_for(wallet, lptoken_address, block, blockchain, decimals=True):
    """Retrieves and formats balance information for a given wallet and liquidity pool token (LP token)."""
    balances, holding = get_balances(wallet, lptoken_address, block, blockchain, decimals=decimals)

    data = {
        "blockchain": blockchain,
        "block": block,
        "protocol": "Uniswap V2",
        "positions_key": "lptoken_address",
        "version": 0,
        "wallet": wallet,
        "decimals": 18,
        "positions": {
            lptoken_address: {
                "holdings": holding,
                "underlyings": balances,
            }
        },
    }
    return data