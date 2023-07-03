from dataclasses import dataclass

from defyes.constants import (
    API_KEY_ARBITRUM,
    API_KEY_AVALANCHE,
    API_KEY_BINANCE,
    API_KEY_ETHERSCAN,
    API_KEY_FANTOM,
    API_KEY_GNOSISSCAN,
    API_KEY_POLSCAN,
)
from defyes.util.enums import Chain, Explorer

blockexplorers = {
    Chain.ETHEREUM.value: [Explorer.ETHERSCAN.value, API_KEY_ETHERSCAN],
    Chain.POLYGON.value: [Explorer.POLYSCAN.value, API_KEY_POLSCAN],
    Chain.GNOSIS.value: [Explorer.GNOSISSCAN.value, API_KEY_GNOSISSCAN],
    # FIXME: XDAI should be eventually removed
    Chain.XDAI.value: [Explorer.GNOSISSCAN.value, API_KEY_GNOSISSCAN],
    Chain.BINANCE.value: [Explorer.BSCSCAN.value, API_KEY_BINANCE],
    Chain.AVALANCHE.value: [Explorer.AVAXSCAN.value, API_KEY_AVALANCHE],
    Chain.FANTOM.value: [Explorer.FTMSCAN.value, API_KEY_FANTOM],
    Chain.ARBITRUM.value: [Explorer.ARBISCAN.value, API_KEY_ARBITRUM],
}

# print(blockexplorers)


# FIXME: this collides with the imported Explorer
@dataclass
class Explorer:
    blockchain: str

    def get_explorer(self):
        for k, v in blockexplorers.items():
            if k == self.blockchain:
                return v[0]

    def get_private_key(self):
        for k, v in blockexplorers.items():
            if k == self.blockchain:
                return v[1]
