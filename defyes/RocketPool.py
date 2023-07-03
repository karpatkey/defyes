import logging
from decimal import Decimal

from web3 import Web3

from defyes.constants import ETHEREUM
from defyes.eth_derivs import EthDerivative
from defyes.functions import get_node

logger = logging.getLogger(__name__)

ROCKET_ADDR = "0xae78736Cd615f374D3085123A210448E74Fc6393"

RocketPool = EthDerivative(
    protocol="Rocket Pool",
    description="Rocket Pool ETH",
    blockchain=ETHEREUM,
    addr=ROCKET_ADDR,
    underlying_token="0x0000000000000000000000000000000000000000",
    eth_value_function="getEthValue",
    eth_value_abi='[{"inputs":[{"internalType":"uint256","name":"_rethAmount","type":"uint256"}],"name":"getEthValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]',
)


def underlying(
    wallet: str, block: int | str, blockchain: str, decimals: bool = True, web3: Web3 = None, unwrapped: bool = True
) -> list:
    # The blockchain argument is not used but it could be in the future if Rocket Pool deploys on other chain
    if web3 is None:
        web3 = get_node(blockchain, block=block)
    value = RocketPool.underlying(wallet=wallet, block=block, decimals=decimals, web3=web3, unwrapped=unwrapped)
    if unwrapped:
        return [[RocketPool.underlying_token, value]]
    else:
        return [[RocketPool.addr, value]]


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
    # The blockchain argument is not used but it could be in the future if Rocket Pool deploys on other chain
    if web3 is None:
        web3 = get_node(blockchain, block=block)
    value = RocketPool.unwrap(amount=amount, block=block, web3=web3)
    return [[RocketPool.underlying_token, value]]
