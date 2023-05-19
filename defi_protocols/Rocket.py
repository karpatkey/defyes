import logging

from defi_protocols.util.EthDerivs import EthDerivative

logger = logging.getLogger(__name__)

def underlying(wallet, deriv_address, block, web3=None):
    deriv = EthDerivative(deriv_address, block, web3)
    return deriv.underlying(wallet)
