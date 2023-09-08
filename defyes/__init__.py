import logging

from .protocols import aave  # noqa
from .protocols import aavev3  # noqa
from .protocols import agave  # noqa
from .protocols import angle  # noqa
from .protocols import ankr  # noqa
from .protocols import aura  # noqa
from .protocols import azuro  # noqa
from .protocols import balancer  # noqa
from .protocols import bancor  # noqa
from .protocols import compound  # noqa
from .protocols import compoundv3  # noqa
from .protocols import connext  # noqa
from .protocols import convex  # noqa
from .protocols import curve  # noqa
from .protocols import element  # noqa
from .protocols import elk  # noqa
from .protocols import hiddenhand  # noqa
from .protocols import honeyswap  # noqa
from .protocols import idle  # noqa
from .protocols import ironbank  # noqa
from .protocols import lido  # noqa
from .protocols import maker  # noqa
from .protocols import mstable  # noqa
from .protocols import notional  # noqa
from .protocols import qidao  # noqa
from .protocols import realt  # noqa
from .protocols import reflexer  # noqa
from .protocols import rocketpool  # noqa
from .protocols import stakewise  # noqa
from .protocols import sushiswap  # noqa
from .protocols import swapr  # noqa
from .protocols import symmetric  # noqa
from .protocols import uniswapv3  # noqa
from .protocols import unit  # noqa
from .protocols import votium  # noqa

Aave = aave
Aave_v3 = aavev3
Agave = agave
Angle = angle
Ankr = ankr
Aura = aura
Azuro = azuro
Balancer = balancer
Bancor = bancor
Compound = compound
Compoundv3 = compoundv3
Connext = connext
Convex = convex
Curve = curve
Element = element
Elk = elk
HiddenHand = hiddenhand
Honeyswap = honeyswap
Idle = idle
IronBank = ironbank
Lido = lido
Maker = maker
mStable = mstable
Notional = notional
QiDao = qidao
RealT = realt
Reflexer = reflexer
RocketPool = rocketpool
Stakewise = stakewise
SushiSwap = sushiswap
Swapr = swapr
Symmetric = symmetric
UniswapV3 = uniswapv3
Unit = unit
Votium = votium

logging.getLogger(__name__).addHandler(logging.NullHandler())


def add_stderr_logger(level: int = logging.DEBUG) -> logging.StreamHandler:
    """
    Helper for quickly adding a StreamHandler to the logger. Useful for
    debugging.
    Returns the handler after adding it.
    """
    # This method needs to be in this __init__.py to get the __name__ correct
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.debug("Added a stderr logging handler to logger: %s", __name__)
    return handler
