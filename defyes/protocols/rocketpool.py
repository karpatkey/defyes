import logging
from decimal import Decimal

from defabipedia import Chain
from karpatkit.node import get_node
from web3 import Web3

from defyes.eth_derivs import EthDerivative

logger = logging.getLogger(__name__)

ROCKET_ADDR = "0xae78736Cd615f374D3085123A210448E74Fc6393"

RocketPool = EthDerivative(
    protocol="Rocket Pool",
    description="Rocket Pool ETH",
    blockchain=Chain.ETHEREUM,
    addr=ROCKET_ADDR,
    underlying_token="0x0000000000000000000000000000000000000000",
    eth_value_function="getEthValue",
    eth_value_abi='[{"inputs":[{"internalType":"uint256","name":"_rethAmount","type":"uint256"}],"name":"getEthValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"}]',
)


def underlying(
    wallet: str, block: int | str, blockchain: str, decimals: bool = True, web3: Web3 = None, unwrapped: bool = True
) -> list:
    # The blockchain argument is not used but it could be in the future if Rocket Pool deploys on other ETHEREUM
    if web3 is None:
        web3 = get_node(blockchain)
    value = RocketPool.underlying(wallet=wallet, block=block, decimals=decimals, web3=web3, unwrapped=unwrapped)
    if unwrapped:
        return [[RocketPool.underlying_token, value]]
    else:
        return [[RocketPool.addr, value]]


def unwrap(amount: int | float | Decimal, block: int | str, blockchain: str, web3: object = None) -> list:
    """
    Returns the balance of the underlying ETH corresponding to the inputted amount of ankrETH.

    Args:
        amount (int or float or Decimal): Amount of ankrETH.
        block (int or str): Block number at which the data is queried.
        blockchain (str): The blockchain on which the data is queried.
        web3 (object, optional): Already instantiated web3 object.

    Returns:
        list: A list where the first element is the underlying token address and the second one is the balance.
    """
    # The blockchain argument is not used but it could be in the future if Rocket Pool deploys on other ETHEREUM
    if web3 is None:
        web3 = get_node(Chain.ETHEREUM)
    value = RocketPool.unwrap(amount=amount, block=block, web3=web3)

    if blockchain == "ethereum":
        underlying_token = RocketPool.underlying_token
    elif blockchain == "gnosis":
        underlying_token = "0xc791240D1F2dEf5938E2031364Ff4ed887133C3d"

    return [[underlying_token, value]]
