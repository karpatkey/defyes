import math
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

from defi_protocols.constants import BINANCE, API_ZAPPER_PRICE, API_KEY_ZAPPER


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

    if blockchain == BINANCE:
        blockchain_id = 'binance-smart-chain'
    else:
        blockchain_id = blockchain

    if timestamp >= (math.floor((datetime.now() - relativedelta(days=1)).timestamp())):
        time_frame = 'hour'
    elif timestamp < (math.floor((datetime.now() - relativedelta(days=1)).timestamp())) and timestamp >= (
    math.floor((datetime.now() - relativedelta(months=1)).timestamp())):
        time_frame = 'day'
    elif timestamp < (math.floor((datetime.now() - relativedelta(months=1)).timestamp())) and timestamp >= (
    math.floor((datetime.now() - relativedelta(years=1)).timestamp())):
        time_frame = 'year'
    else:
        [999, [timestamp, None]]

    data = requests.get(API_ZAPPER_PRICE % (token_address, blockchain_id, time_frame, API_KEY_ZAPPER))

    if data.status_code != 200:
        return [data.status_code, [timestamp, None]]
    else:
        data = data.json()['prices']

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
            return [200, [timestamp, (
                    (timestamp * 1000 - data[i - 1][0]) * data[i][1] + (data[i][0] - timestamp * 1000) *
                    data[i - 1][1]) / (data[i][0] - data[i - 1][0])]]
