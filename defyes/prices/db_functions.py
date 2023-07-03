import json
import os
from pathlib import Path

from web3 import Web3

from defyes.constants import ETHEREUM, POLYGON, XDAI
from defyes.functions import get_symbol


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# update_token_mapping
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def update_token_mapping(
    token_address_eth,
    token_address_pol,
    token_address_xdai,
    price_feed_source=None,
    price_feed_blockchain=None,
    price_feed_connector=None,
):
    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/token_mapping.json", "r") as db_file:
        db_data = json.load(db_file)

    if token_address_xdai is not None and len(str(token_address_xdai)) > 0:
        token_address_xdai = Web3.to_checksum_address(token_address_xdai)

    if token_address_eth is not None and len(str(token_address_eth)) > 0:
        token_address_eth = Web3.to_checksum_address(token_address_eth)

    if token_address_pol is not None and len(str(token_address_pol)) > 0:
        token_address_pol = Web3.to_checksum_address(token_address_pol)

    # XDAI Node
    if token_address_xdai is not None and len(str(token_address_xdai)) > 0:
        token_symbol = get_symbol(token_address_xdai, XDAI)

        try:
            token_data = db_data[XDAI][token_address_xdai]

            if token_address_eth is not None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth

            if token_address_pol is not None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol

            token_data["symbol"] = token_symbol

            try:
                price_feed_data = db_data[XDAI][token_address_xdai]["price_feed"]

                if price_feed_source is not None and len(str(price_feed_source)) > 0:
                    price_feed_data["source"] = price_feed_source

                if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data["blockchain"] = price_feed_blockchain

                if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                    price_feed_data["connector"] = price_feed_connector

            except:
                price_feed_data = {}

                if price_feed_source is not None and len(str(price_feed_source)) > 0:
                    price_feed_data["source"] = price_feed_source

                if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data["blockchain"] = price_feed_blockchain

                if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                    price_feed_data["connector"] = price_feed_connector

                if price_feed_data != {}:
                    db_data[XDAI][token_address_xdai]["price_feed"] = price_feed_data

        except:
            token_data = {}
            price_feed_data = {}

            if token_address_eth is not None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth

            if token_address_pol is not None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol

            token_data["symbol"] = token_symbol

            if price_feed_source is not None and len(str(price_feed_source)) > 0:
                price_feed_data["source"] = price_feed_source

            if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                price_feed_data["blockchain"] = price_feed_blockchain

            if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                price_feed_data["connector"] = price_feed_connector

            if price_feed_data != {}:
                token_data["price_feed"] = price_feed_data

            db_data[XDAI][token_address_xdai] = token_data

    # ETHEREUM Node
    if token_address_eth is not None and len(str(token_address_eth)) > 0:
        token_symbol = get_symbol(token_address_eth, ETHEREUM)

        try:
            token_data = db_data[ETHEREUM][token_address_eth]

            if token_address_xdai is not None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai

            if token_address_pol is not None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol

            token_data["symbol"] = token_symbol

            try:
                price_feed_data = db_data[ETHEREUM][token_address_eth]["price_feed"]

                if price_feed_source is not None and len(str(price_feed_source)) > 0:
                    price_feed_data["source"] = price_feed_source

                if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data["blockchain"] = price_feed_blockchain

                if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                    price_feed_data["connector"] = price_feed_connector

            except:
                price_feed_data = {}

                if price_feed_source is not None and len(str(price_feed_source)) > 0:
                    price_feed_data["source"] = price_feed_source

                if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data["blockchain"] = price_feed_blockchain

                if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                    price_feed_data["connector"] = price_feed_connector

                if price_feed_data != {}:
                    db_data[ETHEREUM][token_address_eth]["price_feed"] = price_feed_data

        except:
            token_data = {}
            price_feed_data = {}

            if token_address_xdai is not None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai

            if token_address_pol is not None and len(str(token_address_pol)) > 0:
                token_data[POLYGON] = token_address_pol

            token_data["symbol"] = token_symbol

            if price_feed_source is not None and len(str(price_feed_source)) > 0:
                price_feed_data["source"] = price_feed_source

            if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                price_feed_data["blockchain"] = price_feed_blockchain

            if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                price_feed_data["connector"] = price_feed_connector

            if price_feed_data != {}:
                token_data["price_feed"] = price_feed_data

            db_data[ETHEREUM][token_address_eth] = token_data

    # POLYGON Node
    if token_address_pol is not None and len(str(token_address_pol)) > 0:
        token_symbol = get_symbol(token_address_pol, POLYGON)

        try:
            token_data = db_data[POLYGON][token_address_pol]

            if token_address_eth is not None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth

            if token_address_xdai is not None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai

            token_data["symbol"] = token_symbol

            try:
                price_feed_data = db_data[POLYGON][token_address_pol]["price_feed"]

                if price_feed_source is not None and len(str(price_feed_source)) > 0:
                    price_feed_data["source"] = price_feed_source

                if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data["blockchain"] = price_feed_blockchain

                if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                    price_feed_data["connector"] = price_feed_connector

            except:
                price_feed_data = {}

                if price_feed_source is not None and len(str(price_feed_source)) > 0:
                    price_feed_data["source"] = price_feed_source

                if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                    price_feed_data["blockchain"] = price_feed_blockchain

                if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                    price_feed_data["connector"] = price_feed_connector

                if price_feed_data != {}:
                    db_data[POLYGON][token_address_pol]["price_feed"] = price_feed_data

        except:
            token_data = {}
            price_feed_data = {}

            if token_address_eth is not None and len(str(token_address_eth)) > 0:
                token_data[ETHEREUM] = token_address_eth

            if token_address_xdai is not None and len(str(token_address_xdai)) > 0:
                token_data[XDAI] = token_address_xdai

            token_data["symbol"] = token_symbol

            if price_feed_source is not None and len(str(price_feed_source)) > 0:
                price_feed_data["source"] = price_feed_source

            if price_feed_blockchain is not None and len(str(price_feed_blockchain)) > 0:
                price_feed_data["blockchain"] = price_feed_blockchain

            if price_feed_connector is not None and len(str(price_feed_connector)) > 0:
                price_feed_data["connector"] = price_feed_connector

            if price_feed_data != {}:
                token_data["price_feed"] = price_feed_data

            db_data[POLYGON][token_address_pol] = token_data

    with open(str(Path(os.path.abspath(__file__)).resolve().parents[0]) + "/token_mapping.json", "w") as db_file:
        json.dump(db_data, db_file)
