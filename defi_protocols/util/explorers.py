import os

from dataclasses import dataclass
from defi_protocols.util.enums import Chain, Explorer
from defi_protocols.constants import (API_KEY_ETHERSCAN, API_KEY_POLSCAN, API_KEY_GNOSISSCAN,
                                      API_KEY_BINANCE, API_KEY_AVALANCHE, API_KEY_FANTOM)

blockexplorers= {Chain.ETHEREUM.value:[Explorer.ETHERSCAN.value, API_KEY_ETHERSCAN],
                Chain.POLYGON.value:[Explorer.POLYSCAN.value, API_KEY_POLSCAN],
                Chain.GNOSIS.value:[Explorer.GNOSISSCAN.value, API_KEY_GNOSISSCAN],
                Chain.BINANCE.value:[Explorer.BSCSCAN.value, API_KEY_BINANCE],
                Chain.AVALANCHE.value:[Explorer.AVAXSCAN.value, API_KEY_AVALANCHE],
                Chain.FANTOM.value:[Explorer.FTMSCAN.value, API_KEY_FANTOM]}

#print(blockexplorers)

# FIXME: this collides with the imported Explorer
@dataclass
class Explorer:
    blockchain: str

    def get_explorer(self):
        for k,v in blockexplorers.items():
            if k == self.blockchain:
                return v[0]

    def get_private_key(self):
        for k,v in blockexplorers.items():
            if k == self.blockchain:
                return v[1]
