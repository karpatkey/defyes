import logging
from decimal import Decimal

from defabipedia import Chain
from karpatkit.node import get_node
from web3 import Web3

from defyes.eth_derivs import EthDerivative

logger = logging.getLogger(__name__)

ANKR_ADDR = "0xE95A203B1a91a908F9B9CE46459d101078c2c3cb"

# FIXME: We have to find a way to take into consideration the different ankrETH proxy implementations, may be with a database keeping track of the changes and the blocks


Ankr = EthDerivative(
    protocol="Ankr",
    description="Ankr Staked ETH",
    blockchain=Chain.ETHEREUM,
    addr=ANKR_ADDR,
    underlying_token="0x0000000000000000000000000000000000000000",
    # The 'sharesToBonds' function is only present in the proxy implementation contract from block 16476340 onwards
    # Some proxy implementations:
    # AETH_R16: 0x1E5e5CF3652989A57736901D95749A326F5Cb60F
    # AETH_R17: 0x89632e27427109d64fFe1CdD98027139477E020F
    # AETH_R18: 0x3eD1DFBCCF893b7d2D730EAd3e5eDBF1f8f95a48
    eth_value_function="sharesToBonds",
    eth_value_abi='[{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sharesToBonds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]',
)


def underlying(
    wallet: str, block: int | str, blockchain: str, decimals: bool = True, web3: Web3 = None, unwrapped: bool = True
) -> list:
    # The blockchain argument is not used but it could be in the future if Ankr deploys on other ETHEREUM
    if web3 is None:
        web3 = get_node(blockchain)
    value = Ankr.underlying(wallet=wallet, block=block, decimals=decimals, web3=web3, unwrapped=unwrapped)
    if unwrapped:
        return [[Ankr.underlying_token, value]]
    else:
        return [[Ankr.addr, value]]


def unwrap(amount: int | float | Decimal, block: int | str, blockchain: str, web3: object = None) -> list:
    """
    Returns the balance of the underlying ETH corresponding to the inputted amount of ankrETH.
    Parameters
    ----------
    amount : int or float or Decimal
        amount of ankrETH;
    block : int or 'latest'
        block number at which the data is queried
    web3: obj
        optional, already instantiated web3 object

    Returns
    ----------
    list
        a list where the first element is the underlying token address and the second one is the balance
    """
    # The blockchain argument is not used but it could be in the future if Ankr deploys on other ETHEREUM
    if web3 is None:
        web3 = get_node(blockchain)
    value = Ankr.unwrap(amount=amount, block=block, web3=web3)
    return [[Ankr.underlying_token, value]]
