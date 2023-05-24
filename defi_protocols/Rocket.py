import logging

from defi_protocols.util.EthDerivs import EthDerivative

logger = logging.getLogger(__name__)

def underlying(wallet, deriv_address, block, blockchain, decimals=True, web3=None):
    deriv = EthDerivative(deriv_address, block, blockchain, decimals, web3)
    if deriv.protocol_name == "Rocket Pool ETH":
        return deriv.underlying(wallet)
    else:
        return 'not a RocketPool address'
