from web3 import Web3

from defi_protocols.functions import get_node, get_contract, get_decimals, GetNodeIndexError
from defi_protocols.constants import ETHEREUM, POLYGON, XDAI, BINANCE, KOVAN, OPTIMISM, ARBITRUM, AVAX, MAX_EXECUTIONS, ZERO_ADDRESS
from defi_protocols.prices import Chainlink

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ORACLES
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Ethereum Oracle Address
ORACLE_ETHEREUM = '0x07D91f5fb9Bf7798734C3f606dB065549F6893bb'

# Polygon Oracle Address
ORACLE_POLYGON = '0x7F069df72b7A39bCE9806e3AfaF579E54D8CF2b9'

# Gnosis Chain(xDai) Oracle Address
ORACLE_XDAI = '0x142DB045195CEcaBe415161e1dF1CF0337A4d02E'

# Smart Chain (Binance) Oracle Address
ORACLE_BINANCE = '0xfbD61B037C325b959c0F6A7e69D8f37770C2c550'

# Kovan Oracle Address
ORACLE_KOVAN = '0x29BC86Ad68bB3BD3d54841a8522e0020C1882C22'

# Optimism Oracle Address
ORACLE_OPTIMISM = '0x11DEE30E710B8d4a8630392781Cc3c0046365d4c'

# Arbitrum Oracle Address
ORACLE_ARBITRUM = '0x735247fb0a604c0adC6cab38ACE16D0DbA31295F'

# Avax Oracle Address
ORACLE_AVAX = '0xBd0c7AaF0bF082712EbE919a9dD94b2d978f79A9'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ABIs
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Oracle ABI - connectors, oracles, getRate, getRateToEth
ABI_ORACLE = '[{"inputs":[],"name":"connectors","outputs":[{"internalType":"contract IERC20[]","name":"allConnectors","type":"address[]"}],"stateMutability":"view","type":"function"}, {"inputs":[],"name":"oracles","outputs":[{"internalType":"contract IOracle[]","name":"allOracles","type":"address[]"},{"internalType":"enum OffchainOracle.OracleType[]","name":"oracleTypes","type":"uint8[]"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"contract IERC20","name":"srcToken","type":"address"},{"internalType":"contract IERC20","name":"dstToken","type":"address"},{"internalType":"bool","name":"useWrappers","type":"bool"}],"name":"getRate","outputs":[{"internalType":"uint256","name":"weightedRate","type":"uint256"}],"stateMutability":"view","type":"function"}, {"inputs":[{"internalType":"contract IERC20","name":"srcToken","type":"address"},{"internalType":"bool","name":"useSrcWrappers","type":"bool"}],"name":"getRateToEth","outputs":[{"internalType":"uint256","name":"weightedRate","type":"uint256"}],"stateMutability":"view","type":"function"}]'


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_oracle_address
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_oracle_address(blockchain):
    if blockchain == ETHEREUM:
        return ORACLE_ETHEREUM

    elif blockchain == POLYGON:
        return ORACLE_POLYGON

    elif blockchain == XDAI:
        return ORACLE_XDAI

    elif blockchain == BINANCE:
        return ORACLE_BINANCE

    elif blockchain == KOVAN:
        return ORACLE_KOVAN

    elif blockchain == OPTIMISM:
        return ORACLE_OPTIMISM

    elif blockchain == ARBITRUM:
        return ORACLE_ARBITRUM

    elif blockchain == AVAX:
        return ORACLE_AVAX


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_rate
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'token_dst' = token_dst address -> if it's not passed onto the function, the native token of the blockchain is used to calculate the rate
# 'use_wrappers' = True / False -> To handle wrapped tokens, such as wETH, cDAI, aDAI etc., the 1inch spot price aggregator uses custom wrapper smart contracts that
#                                  wrap/unwrap tokens at the current wrapping exchange rate
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_rate(token_src, block, blockchain, web3=None, execution=1, index=0, use_wrappers=False, token_dst=None):
    """

    :param token_src:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param use_wrappers:
    :param token_dst:
    :return:
    """
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block)

        token_src = Web3.to_checksum_address(token_src)

        if token_dst is not None:
            token_dst = Web3.to_checksum_address(token_dst)

        oracle_address = get_oracle_address(blockchain)
        oracle_contract = get_contract(oracle_address, blockchain, web3=web3, abi=ABI_ORACLE, block=block)

        token_src_decimals = get_decimals(token_src, blockchain, web3=web3)

        if token_dst is not None:
            token_dst_decimals = get_decimals(token_dst, blockchain, web3=web3)
        else:
            token_dst_decimals = 18

        if token_dst is None:
            rate = oracle_contract.functions.getRateToEth(token_src, use_wrappers).call(block_identifier=block) / (
                        10 ** abs(18 + token_dst_decimals - token_src_decimals))
        else:
            rate = oracle_contract.functions.getRate(token_src, token_dst, use_wrappers).call(
                block_identifier=block) / (10 ** abs(18 + token_dst_decimals - token_src_decimals))

        return rate

    except GetNodeIndexError:
        return get_rate(token_src, block, blockchain, use_wrappers=use_wrappers, token_dst=token_dst, index=0,
                        execution=execution + 1)

    except:
        return get_rate(token_src, block, blockchain, use_wrappers=use_wrappers, token_dst=token_dst, index=index + 1,
                        execution=execution)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_price
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'connector' = connector address -> if it's not passed onto the function, the native token of the blockchain is used to calculate the token_src price /
#                                    if it's passed onto the function, the connector is used to calculate the token_src price
# 'use_wrappers' = True / False -> To handle wrapped tokens, such as wETH, cDAI, aDAI etc., the 1inch spot price aggregator uses custom wrapper smart contracts that
#                                  wrap/unwrap tokens at the current wrapping exchange rate
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_price(token_src, block, blockchain, web3=None, execution=1, index=0, use_wrappers=False, connector=None):
    """

    :param token_src:
    :param block:
    :param blockchain:
    :param web3:
    :param execution:
    :param index:
    :param use_wrappers:
    :param connector:
    :return:
    """

    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block)

        token_src = Web3.to_checksum_address(token_src)

        native_token_price = Chainlink.get_native_token_price(web3, block, blockchain)

        if token_src == ZERO_ADDRESS:
            return native_token_price

        else:
            if connector is None:
                rate = get_rate(token_src, block, blockchain, use_wrappers=use_wrappers)
                token_src_price = native_token_price * rate
            else:
                connector = Web3.to_checksum_address(connector)

                rate = get_rate(token_src, block, blockchain, token_dst=connector, use_wrappers=use_wrappers)
                connector_price = get_price(connector, block, blockchain, use_wrappers=use_wrappers)
                token_src_price = connector_price * rate

        return token_src_price

    except GetNodeIndexError:
        return get_price(token_src, block, blockchain, use_wrappers=use_wrappers, connector=connector, index=0,
                         execution=execution + 1)

    except:
        return get_price(token_src, block, blockchain, use_wrappers=use_wrappers, connector=connector, index=index + 1,
                         execution=execution)
