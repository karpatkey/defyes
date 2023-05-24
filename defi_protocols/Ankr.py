import logging

from defi_protocols.util.EthDerivs import EthDerivative

logger = logging.getLogger(__name__)

def underlying(wallet, deriv_address, block, blockchain, decimals=True, web3=None, deriv=False):
    deriva = EthDerivative(deriv_address, block, web3, decimals, blockchain)
    if deriva.protocol_name == "Ankr Staked ETH":
        return deriva.underlying(wallet, deriv)
    else:
        return 'not a RocketPool address'