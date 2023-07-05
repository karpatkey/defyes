import json
import os
from datetime import datetime
from pathlib import Path

import pandas as pd
import requests
from tqdm import tqdm
from web3 import Web3

from defyes.constants import API_ETHERSCAN_GETTOKENINFO, API_KEY_ETHERSCAN, ETHEREUM, MAX_EXECUTIONS, ZERO_ADDRESS
from defyes.functions import GetNodeIndexError, block_to_timestamp, get_node, timestamp_to_block
from defyes.prices import Chainlink, CoinGecko, Zapper, _1inch


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_price
# 'execution' = the current iteration, as the function goes through the different Full/Archival nodes of the blockchain attempting a successfull execution
# 'index' = specifies the index of the Archival or Full Node that will be retrieved by the getNode() function
# 'web3' = web3 (Node) -> Improves performance
# 'token_mapping_data' = /db/token_mapping.json data
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_price(token_address, block, blockchain, web3=None, execution=1, index=0, token_mapping_data=None):
    # If the number of executions is greater than the MAX_EXECUTIONS variable -> returns None and halts
    if execution > MAX_EXECUTIONS:
        return None

    token_price = None

    try:
        if web3 is None:
            web3 = get_node(blockchain, block=block)

        token_address = Web3.to_checksum_address(token_address)

        if token_address == ZERO_ADDRESS:
            # returns price, source and blockchain:
            return Chainlink.get_native_token_price(web3, block, blockchain), "Chainlink", blockchain

        try:
            if token_mapping_data is None:
                with open(
                    str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/token_mapping.json", "r"
                ) as token_mapping_file:
                    # Reading from json file
                    token_mapping_data = json.load(token_mapping_file)
                    token_mapping_file.close()

            try:
                price_feed_data = token_mapping_data[blockchain][token_address]["price_feed"]

                try:
                    price_feed_data["source"]
                    price_feed_data["blockchain"]
                except:
                    raise Exception

                if blockchain == price_feed_data["blockchain"]:
                    token_address_mapping = token_address
                    block_price_feed = block
                else:
                    try:
                        token_address_mapping = token_mapping_data[blockchain][token_address][
                            price_feed_data["blockchain"]
                        ]
                    except:
                        token_address_mapping = token_address

                    block_price_feed = timestamp_to_block(
                        block_to_timestamp(block, blockchain), price_feed_data["blockchain"]
                    )

                if price_feed_data["source"] == "1inch":
                    try:
                        connector = price_feed_data["connector"]

                    except:
                        connector = None

                    # returns price, source and blockchain:
                    return (
                        _1inch.get_price(
                            token_address_mapping, block_price_feed, price_feed_data["blockchain"], connector=connector
                        ),
                        "1inch",
                        price_feed_data["blockchain"],
                    )

                elif price_feed_data["source"] == "coingecko":
                    price_coingecko = CoinGecko.get_price(
                        token_address_mapping,
                        block_to_timestamp(block_price_feed, price_feed_data["blockchain"]),
                        price_feed_data["blockchain"],
                    )

                    while price_coingecko[0] == 429:
                        price_coingecko = CoinGecko.get_price(
                            token_address_mapping,
                            block_to_timestamp(block_price_feed, price_feed_data["blockchain"]),
                            price_feed_data["blockchain"],
                        )

                    # returns price, source and blockchain:
                    return price_coingecko[1][1], "coingecko", price_feed_data["blockchain"]

                elif price_feed_data["source"] == "zapper":
                    price_zapper = Zapper.get_price(
                        token_address_mapping,
                        block_to_timestamp(block_price_feed, price_feed_data["blockchain"]),
                        price_feed_data["blockchain"],
                    )

                    # returns price, source and blockchain:
                    return price_zapper[1][1], "zapper", price_feed_data["blockchain"]

            except:
                raise Exception

        except:
            if blockchain != ETHEREUM:
                block_eth = timestamp_to_block(block_to_timestamp(block, blockchain), ETHEREUM)

                try:
                    token_address_eth = token_mapping_data[blockchain][token_address][ETHEREUM]
                except:
                    token_address_eth = None

            else:
                token_address_eth = token_address
                block_eth = block

            if token_address_eth is not None:
                token_price = Chainlink.get_mainnet_price(token_address_eth, block_eth)
                source = "Chainlink"
                final_blockchain = "ETHEREUM"

                if token_price is None:
                    token_price = _1inch.get_price(token_address_eth, block_eth, ETHEREUM)
                    source = "1inch"
                    final_blockchain = "ETHEREUM"  # redundant but to stay clear

            else:
                token_price = _1inch.get_price(token_address, block, blockchain)
                source = "1inch"
                final_blockchain = blockchain

            return token_price, source, final_blockchain

    except GetNodeIndexError:
        return get_price(
            token_address, block, blockchain, token_mapping_data=token_mapping_data, index=0, execution=execution + 1
        )

    except:
        return get_price(
            token_address,
            block,
            blockchain,
            token_mapping_data=token_mapping_data,
            index=index + 1,
            execution=execution,
        )


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_etherscan_price
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_etherscan_price(token_address):
    """

    :param token_address:
    """
    price = requests.get(API_ETHERSCAN_GETTOKENINFO % (token_address, API_KEY_ETHERSCAN)).json()["result"][0][
        "tokenPriceUSD"
    ]

    return price, "etherscan", ETHEREUM


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_today_prices_data
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_today_prices_data(file_name, return_type="df", web3=None):
    file = open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/" + file_name, "r")
    token_file = json.load(file)

    price = []
    source = []
    time_stamp = []
    blockchain = []
    token_address_data = []
    date_stamp = []

    for j in tqdm((token_file.keys())):  # Recorro las blockchain
        for k in tqdm((token_file[j].keys())):
            token_address = k
            token_blokchain = j
            # token_symbol = token_file[j][token_address]["symbol"]
            # print(token_address,token_blokchain,token_symbol)

            now = datetime(
                datetime.now().year,
                datetime.now().month,
                datetime.now().day,
                datetime.now().hour,
                datetime.now().minute,
            )

            # Use reference_block just if latest not needed.
            # reference_block = (date_to_block(now.strftime('%Y-%m-%d %H:%M:%S'), token_blokchain))

            data = get_price(token_address, "latest", token_blokchain, web3=web3)
            # print('Price Of',token_symbol,data,)
            price.append(data[0])
            source.append(data[1])
            time_stamp.append(now.strftime("%Y-%m-%d %H:%M:00"))
            date_stamp.append(now.strftime("%Y-%m-%d"))
            blockchain.append(data[2])
            token_address_data.append(token_address)

    # token_address.append(token_address[0])

    data_raw = {
        "Price_Datetime": time_stamp,
        "Price_Date": date_stamp,  # .strftime("%Y-%m-%d")
        "Price": price,
        "Source": source,
        "Token_Address": token_address_data,
        "Blockchain": blockchain,
    }

    if return_type == "df":
        df = pd.DataFrame(data_raw)
        return df
    else:
        return data_raw
