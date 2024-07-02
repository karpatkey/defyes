from decimal import Decimal

from defabipedia import Chain
from karpatkit.cache import const_call
from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CHAINLINK PRICE FEEDS
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ETHEREUM
# Feed Registry
CHAINLINK_FEED_REGISTRY = "0x47Fb2585D2C56Fe188D0E6ec628a38b74fCeeeDf"
# Quotes - USD and ETH
CHAINLINK_ETH_QUOTES = ["0x0000000000000000000000000000000000000348", "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"]
# ETH/USD Price Feed
CHAINLINK_ETH_USD = "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419"

# POLYGON
# MATIC/USD Price Feed
CHAINLINK_MATIC_USD = "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0"

# GNOSIS
# XDAI/USD Price Feed - The price feed retrieves the price of DAI instead of XDAI. Chainlink does not provide a price feed for XDAI.
CHAINLINK_XDAI_USD = "0x678df3415fc31947dA4324eC63212874be5a82f8"

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ChainLink Feed Registry ABI - getFeed
ABI_CHAINLINK_FEED_REGISTRY = '[{"inputs":[{"internalType":"address","name":"base","type":"address"},{"internalType":"address","name":"quote","type":"address"}],"name":"getFeed","outputs":[{"internalType":"contract AggregatorV2V3Interface","name":"aggregator","type":"address"}],"stateMutability":"view","type":"function"}]'
# ChainLink Price Feed ABI - latestAnswer, decimals
ABI_CHAINLINK_PRICE_FEED = '[{"inputs":[],"name":"latestAnswer","outputs":[{"internalType":"int256","name":"","type":"int256"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"}]'


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_native_token_price
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_native_token_price(web3, block, blockchain, decimals=False):
    """

    :param web3:
    :param block:
    :param blockchain:
    :return:
    """
    if blockchain == Chain.ETHEREUM:
        price_feed_address = CHAINLINK_ETH_USD

    elif blockchain == Chain.POLYGON:
        price_feed_address = CHAINLINK_MATIC_USD

    elif blockchain == Chain.GNOSIS:
        price_feed_address = CHAINLINK_XDAI_USD

    price_feed_contract = get_contract(price_feed_address, blockchain, web3=web3, abi=ABI_CHAINLINK_PRICE_FEED)
    price_feed_decimals = const_call(price_feed_contract.functions.decimals())
    if decimals:
        price_feed_decimals = Decimal(price_feed_decimals)
    native_token_price = price_feed_contract.functions.latestAnswer().call(block_identifier=block) / (
        10**price_feed_decimals
    )

    return native_token_price


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_mainnet_price
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_mainnet_price(token_address, block, web3=None, index=0):
    """
    :param token_address:
    :param block:
    :param web3:
    :param index:
    :return:
    """
    if web3 is None:
        web3 = get_node(Chain.ETHEREUM)

    token_address = Web3.to_checksum_address(token_address)

    feed_registry_contract = get_contract(
        CHAINLINK_FEED_REGISTRY, Chain.ETHEREUM, web3=web3, abi=ABI_CHAINLINK_FEED_REGISTRY
    )

    for quote in CHAINLINK_ETH_QUOTES:
        try:
            price_feed_address = feed_registry_contract.functions.getFeed(token_address, quote).call(
                block_identifier=block
            )
            price_feed_contract = get_contract(
                price_feed_address, Chain.ETHEREUM, web3=web3, abi=ABI_CHAINLINK_PRICE_FEED
            )
            price_feed_decimals = const_call(price_feed_contract.functions.decimals())

            if quote == CHAINLINK_ETH_QUOTES[0]:
                return (
                    price_feed_contract.functions.latestAnswer().call(block_identifier=block)
                    / 10**price_feed_decimals
                )
            else:
                return (
                    price_feed_contract.functions.latestAnswer().call(block_identifier=block)
                    / 10**price_feed_decimals
                    * get_native_token_price(web3, block, Chain.ETHEREUM)
                )

        except Exception as ex:
            if "Feed not found" in ex.args[0]:
                continue
            else:
                raise Exception

    return None
