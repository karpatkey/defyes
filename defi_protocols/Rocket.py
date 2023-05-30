import logging

from defi_protocols.EthDerivs import EthDerivative

logger = logging.getLogger(__name__)

def underlying(wallet, deriv_address, block, blockchain, decimals=True, web3=None, deriv=False):
    deriva = EthDerivative("Rocket Pool ETH", deriv_address, block, web3, decimals, blockchain)
    return deriva.underlying(wallet, deriv)
