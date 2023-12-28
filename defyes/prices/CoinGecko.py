import math

import requests

from defyes.constants import Address, Chain

URL_COINID_PRICE_RANGE = "https://api.coingecko.com/api/v3/coins/%s/market_chart/range?vs_currency=usd&from=%d&to=%d"
URL_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE = (
    "https://api.coingecko.com/api/v3/coins/%s/contract/%s/market_chart/range?vs_currency=usd&from=%d&to=%d"
)
URL_BLOCKCHAINID_TOKENADDRESS_PRICE = "https://api.coingecko.com/api/v3/coins/%s/contract/%s"


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_price
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_price(token_address, timestamp, blockchain):
    """

    :param token_address:
    :param timestamp:
    :param blockchain:
    :return:
    """
    if blockchain not in [Chain.ETHEREUM, Chain.GNOSIS, Chain.POLYGON, Chain.AVALANCHE, Chain.OPTIMISM, Chain.ARBITRUM]:
        return [timestamp, None]

    if token_address == Address.ZERO:
        if blockchain == Chain.POLYGON:
            coin_id = "matic-network"
        else:
            coin_id = blockchain

        data = requests.get(URL_COINID_PRICE_RANGE % (coin_id, timestamp - 3600 * 23, timestamp + 3600 * 1))
        if data.status_code != 200:
            return [data.status_code, [timestamp, None]]
        else:
            data = data.json()["prices"]
            if data == []:
                data = requests.get(
                    URL_COINID_PRICE_RANGE % (coin_id, timestamp - 3600 * 24 * 40, timestamp + 3600 * 24 * 40)
                )
                if data.status_code != 200:
                    return [data.status_code, [timestamp, None]]
                else:
                    data = data.json()["prices"]
                    if data == []:
                        data = requests.get(
                            URL_COINID_PRICE_RANGE % (coin_id, timestamp - 3600 * 24 * 180, timestamp + 3600 * 24 * 180)
                        )
                        if data.status_code != 200:
                            return [data.status_code, [timestamp, None]]
                        else:
                            data = data.json()["prices"]

    else:
        blockchain_id = {
            Chain.POLYGON: "polygon-pos",
            Chain.OPTIMISM: "optimistic-ethereum",
            Chain.ARBITRUM: "arbitrum-one",
        }.get(blockchain, blockchain)

        data = requests.get(
            URL_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE
            % (blockchain_id, token_address, timestamp - 3600 * 23, timestamp + 3600 * 1)
        )
        if data.status_code != 200:
            return [data.status_code, [timestamp, None]]
        else:
            data = data.json()["prices"]
            if data == []:
                data = requests.get(
                    URL_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE
                    % (blockchain_id, token_address, timestamp - 3600 * 24 * 40, timestamp + 3600 * 24 * 40)
                )
                if data.status_code != 200:
                    return [data.status_code, [timestamp, None]]
                else:
                    data = data.json()["prices"]
                    if data == []:
                        data = requests.get(
                            URL_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE
                            % (blockchain_id, token_address, timestamp - 3600 * 24 * 180, timestamp + 3600 * 24 * 180)
                        )
                        if data.status_code != 200:
                            return [data.status_code, [timestamp, None]]
                        else:
                            data = data.json()["prices"]

    if data == [] or data is None:
        return [200, [timestamp, None]]
    else:
        if len(data) == 1:
            return [200, [math.floor(data[0][0] / 1000), data[0][1]]]
        i = 0
        while int(data[i][0]) < timestamp * 1000:
            i += 1
            if i == len(data):
                break

        if i == len(data):
            return [200, [math.floor(data[i - 1][0] / 1000), data[i - 1][1]]]
        else:
            return [
                200,
                [
                    timestamp,
                    (
                        (timestamp * 1000 - data[i - 1][0]) * data[i][1]
                        + (data[i][0] - timestamp * 1000) * data[i - 1][1]
                    )
                    / (data[i][0] - data[i - 1][0]),
                ],
            ]


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# get_price_range
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_price_range(token_address, start_timestamp, end_timestamp, blockchain):
    """

    :param token_address:
    :param start_timestamp:
    :param end_timestamp:
    :param blockchain:
    :return:
    """
    result = []

    if blockchain != Chain.ETHEREUM and blockchain != Chain.GNOSIS and blockchain != Chain.POLYGON:
        return None

    if token_address == Address.ZERO:
        if blockchain == Chain.POLYGON:
            coin_id = "matic-network"
        else:
            coin_id = blockchain

        data = requests.get(URL_COINID_PRICE_RANGE % (coin_id, start_timestamp, end_timestamp))
        if data.status_code != 200:
            return [data.status_code, None]
        else:
            data = data.json()["prices"]

    else:
        if blockchain == Chain.POLYGON:
            blockchain_id = "polygon-pos"
        else:
            blockchain_id = blockchain

        data = requests.get(
            URL_BLOCKCHAINID_TOKENADDRESS_PRICE_RANGE % (blockchain_id, token_address, start_timestamp, end_timestamp)
        )
        if data.status_code != 200:
            return [data.status_code, None]
        else:
            data = data.json()["prices"]

    if data == [] or data is None:
        return [200, None]
    else:
        for i in range(len(data)):
            result.append([math.floor(data[i][0] / 1000), data[i][1]])

    return [200, result]
