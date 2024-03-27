from dataclasses import dataclass, field
from decimal import Decimal

from defabipedia import Chain
from gql import Client, gql  # thegraph queries
from gql.transport.requests import RequestsHTTPTransport
from karpatkit.cache import const_call
from karpatkit.helpers import call_contract_method
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import balance_of, get_contract, get_decimals

# Subgraph API endpoints for Connext on different blockchains: https://docs.connext.network/resources/subgraphs
# For more info on how to query the subgraph: https://docs.connext.network/developers/guides/xcall-status
SUBGRAPH_ENDPOINTS = {
    Chain.ETHEREUM: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-mainnet",
    Chain.GNOSIS: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-gnosis",
    Chain.OPTIMISM: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-optimism",
    Chain.ARBITRUM: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-arbitrum-one",
    Chain.BINANCE: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-bnb",
    Chain.POLYGON: "https://api.thegraph.com/subgraphs/name/connext/amarok-runtime-v0-polygon",
}

# Connext Diamond Contract on different blockchains: https://docs.connext.network/resources/deployments
DIAMOND_ADDRESSES = {
    Chain.ETHEREUM: "0x8898B472C54c31894e3B9bb83cEA802a5d0e63C6",
    Chain.GNOSIS: "0x5bB83e95f63217CDa6aE3D181BA580Ef377D2109",
    Chain.OPTIMISM: "0x8f7492DE823025b4CfaAB1D34c58963F2af5DEDA",
    Chain.ARBITRUM: "0xEE9deC2712cCE65174B561151701Bf54b99C24C8",
    Chain.BINANCE: "0xCd401c10afa37d641d2F594852DA94C700e4F2CE",
    Chain.POLYGON: "0x11984dc4465481512eb5b777E44061C158CF2259",
}

# Connext Diamond ABI - getSwapLPToken, getSwapTokenIndex, getSwapToken, calculateRemoveSwapLiquidity
ABI_CONNEXT_DIAMOND = '[{"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"}],"name":"getSwapLPToken","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"address","name":"tokenAddress","type":"address"}],"name":"getSwapTokenIndex","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"uint8","name":"index","type":"uint8"}],"name":"getSwapToken","outputs":[{"internalType":"contractIERC20","name":"","type":"address"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"bytes32","name":"key","type":"bytes32"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"calculateRemoveSwapLiquidity","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"}]'

DECIMAL_FIX_TOKENS = {
    "0x55d398326f99059fF775485246999027B3197955": 18,
    "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d": 18,
}


def query_assets(subgraph_api_endpoint: str) -> list:
    """Return a list of dict:assets with it's id, key, adoptedAsset and decimals

    Args:
        subgraph_api_endpoint (str): Subgraph API endpoint

    Returns:
        list: list of dict:assets with it's id, key, adoptedAsset and decimals
    """
    assets = []
    skip = 0
    first = 1000
    status = "true"

    # Initialize subgraph
    connext_transport = RequestsHTTPTransport(url=subgraph_api_endpoint, verify=True, retries=3)
    client = Client(transport=connext_transport)

    response_length = 1001

    while not response_length < 1000:
        query_string = f"""
        query {{
        assets(first: {first}, skip: {skip}, where: {{status_:{{status: {status}}}}}) {{
            id
            key
            adoptedAsset
            decimal
            status {{status}}
        }}
        }}
        """

        # formatted_query_string = query_string.format(first=assets_to_query, skip=skip)
        response = client.execute(gql(query_string))
        assets.extend(response["assets"])
        response_length = len(response["assets"])
        skip += response_length

    for a in assets:
        a["id"] = Web3.to_checksum_address(a["id"])
        a["adoptedAsset"] = Web3.to_checksum_address(a["adoptedAsset"])
        a["decimal"] = int(a["decimal"]) if a.get("decimal", None) else 0

    return assets


@dataclass
class Connext:
    blockchain: str
    block: int | str
    web3: Web3 = None
    diamond_adrr: str = field(init=False)
    diamond_contract: object = field(init=False)
    subgraph_api_endpoint: str = field(init=False)
    assets: list = field(init=False)

    def __post_init__(self) -> None:
        try:
            self.diamond_adrr = DIAMOND_ADDRESSES[self.blockchain]
            self.subgraph_api_endpoint = SUBGRAPH_ENDPOINTS[self.blockchain]
        except KeyError:
            raise ValueError(f"{self.blockchain} not supported yet")

        if self.web3 is None:
            self.web3 = get_node(self.blockchain)
        else:
            assert isinstance(self.web3, Web3), "web3 is not a Web3 instance"

        self.diamond_contract = get_contract(
            self.diamond_adrr, self.blockchain, web3=self.web3, abi=ABI_CONNEXT_DIAMOND, block=self.block
        )
        self.assets = query_assets(self.subgraph_api_endpoint)

        for asset, decimal in DECIMAL_FIX_TOKENS.items():
            self.update_decimals(asset, decimal)

    def update_decimals(self, adopted_asset, new_decimal):
        """Unfortunately some decimals retrieved from the graph are not correct, so we need to update them manually"""
        for item in self.assets:
            if item["adoptedAsset"] == adopted_asset:
                item["decimal"] = (item["decimal"], new_decimal)

    def underlying(self, wallet: str, lptoken_address: str, decimals: bool = True) -> list:
        """Returns the underlying token balances for the given wallet, lp token address

        Returns:
            list: list of tuples containing [underlying_token_address, balance]
        """
        wallet = Web3.to_checksum_address(wallet)
        lptoken_address = Web3.to_checksum_address(lptoken_address)

        balances = []
        for asset in self.assets:
            if lptoken_address == const_call(self.diamond_contract.functions.getSwapLPToken(asset["key"])):
                lptoken_balance = int(balance_of(wallet, lptoken_address, self.block, self.blockchain, decimals=False))
                amounts = call_contract_method(
                    self.diamond_contract.functions.calculateRemoveSwapLiquidity(asset["key"], lptoken_balance),
                    self.block,
                )

                if amounts:
                    amounts = [Decimal(amounts[0]), Decimal(amounts[1])]
                    if decimals:
                        if isinstance(asset["decimal"], tuple):
                            amounts[0] = amounts[0] / Decimal(10 ** asset["decimal"][0])
                            amounts[1] = amounts[1] / Decimal(10 ** asset["decimal"][1])
                        else:
                            amounts = [amount / Decimal(10 ** asset["decimal"]) for amount in amounts]

                    balances = [[asset["id"], amounts[0]], [asset["adoptedAsset"], amounts[1]]]
                break

        return balances

    def underlying_all(self, wallet: str, decimals: bool = True) -> list:
        """Returns the underlying token balances for all the lp tokens in the protocol for the given wallet and blockchain

        Returns:
            list: list: list of tuples containing [underlying_token_address, balance]
        """
        wallet = Web3.to_checksum_address(wallet)

        balances = []
        for asset in self.assets:
            lptoken_address = const_call(self.diamond_contract.functions.getSwapLPToken(asset["key"]))
            lptoken_balance = int(balance_of(wallet, lptoken_address, self.block, self.blockchain, decimals=False))
            amounts = call_contract_method(
                self.diamond_contract.functions.calculateRemoveSwapLiquidity(asset["key"], lptoken_balance), self.block
            )

            if (not amounts) or amounts == [0, 0]:
                continue
            else:
                amounts = [Decimal(amounts[0]), Decimal(amounts[1])]
                if decimals:
                    if isinstance(asset["decimal"], tuple):
                        amounts[0] = amounts[0] / Decimal(10 ** asset["decimal"][0])
                        amounts[1] = amounts[1] / Decimal(10 ** asset["decimal"][1])
                    else:
                        amounts = [amount / Decimal(10 ** asset["decimal"]) for amount in amounts]

                balances.append([[asset["id"], amounts[0]], [asset["adoptedAsset"], amounts[1]]])

        return balances

    def unwrap(self, lptoken_amount: float, lptoken_address: str, decimals: bool = True) -> list:
        """Returns the unwrapped amount of underlying token given an lp token amount and address

        Returns:
            list: underlying_token, unwrapped_amount
        """
        lptoken_address = Web3.to_checksum_address(lptoken_address)

        balance = []
        for asset in self.assets:
            if lptoken_address == const_call(self.diamond_contract.functions.getSwapLPToken(asset["key"])):
                lptoken_decimals = get_decimals(lptoken_address, self.blockchain, web3=self.web3)
                token_amount = int(Decimal(lptoken_amount) * Decimal(10**lptoken_decimals))
                amounts = call_contract_method(
                    self.diamond_contract.functions.calculateRemoveSwapLiquidity(asset["key"], token_amount), self.block
                )

                if amounts:
                    amount = Decimal(amounts[0] + amounts[1])
                    if decimals:
                        amount = amount / Decimal(10 ** asset["decimal"])

                    balance = [asset["adoptedAsset"], amount]

        return balance


# Transitional wrapper of underlying method
def underlying(
    wallet: str, lptoken_address: str, block: int | str, blockchain: str, web3=None, decimals: bool = True
) -> list:
    connext = Connext(blockchain, block, web3)
    return connext.underlying(wallet, lptoken_address, decimals)


def underlying_all(wallet: str, block: int | str, blockchain: str, web3=None, decimals: bool = True) -> list:
    connext = Connext(blockchain, block, web3)
    return connext.underlying_all(wallet, decimals)


def unwrap(
    lptoken_amount: float, lptoken_address: str, block: int | str, blockchain: str, web3=None, decimals: bool = True
) -> list:
    connext = Connext(blockchain, block, web3)
    return connext.unwrap(lptoken_amount, lptoken_address, decimals)
