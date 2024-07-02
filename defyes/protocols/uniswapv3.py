"""
Module to interact with Uniswap v3 positions and pools.
Most information were obtain through the Uniswap v3 whitepaper. https://uniswap.org/whitepaper-v3.pdf

some of the variables have a slight change in the name to make it more readable.

token0
token1
fee
Lower tick: lower_tick (il)
Upper tick upper_tick (iu)
Current tick: current_tick (ic)
feeGrowthInside0LastX128: fee_growth_inside_0 (fr0)
feeGrowthInside1LastX128: fee_growth_inside_1 (fr1)
feeGrowthGlobal0: fee_growth_0 (fg0)
feeGrowthGlobal1: fee_growth_1 (fg1)
feeGrowthOutside0X128low: fee_growth_outside_0_low (fo0low)
feeGrowthOutside1X128low: fee_growth_outside_1_low (fo1low)
feeGrowthOutside0X128up: fee_growth_outside_0_up (fo0up)
feeGrowthOutside1X128up: fee_growth_outside_1_up (fo1up)
seconds spent above: sa
seconds spent below: sb
fees earned per unit of liquidity in token 0: fees_per_unit_0
fees earned per unit of liquidity in token 1: fees_per_unit_1
"""

import logging
from dataclasses import dataclass, field
from decimal import Decimal
from enum import IntEnum
from typing import ClassVar

from karpatkit.node import get_node
from web3 import Web3

from defyes.functions import get_contract, get_decimals

logger = logging.getLogger(__name__)

FACTORY: str = "0x1F98431c8aD98523631AE4a59f267346ea31F984"

# Contract to get the position based on the NFT id
POSITIONS_NFT: str = "0xC36442b4a4522E871399CD717aBDD847Ab11FE88"

UNISWAPV3_ROUTER2: str = "0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45"

UNISWAPV3_QUOTER: str = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"


class FeeAmount(IntEnum):
    """Possible Fees for Uniwsap v3 Pools https://docs.uniswap.org/sdk/v3/reference/enums/FeeAmount"""

    LOWEST = 100
    LOW = 500
    MEDIUM = 3000
    HIGH = 10000


# Uniswap v3 Factory ABI - getPool
ABI_FACTORY: str = '[{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint24","name":"","type":"uint24"}],"name":"getPool","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutablower_tickity":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutablower_tickity":"view","type":"function"}]'

# Uniswap v3 Pools ABI - slot0, token0, token1
ABI_POOL: str = '[{"inputs":[],"name":"slot0","outputs":[{"internalType":"uint160","name":"sqrtPriceX96","type":"uint160"},{"internalType":"int24","name":"tick","type":"int24"},{"internalType":"uint16","name":"observationIndex","type":"uint16"},{"internalType":"uint16","name":"observationCardinality","type":"uint16"},{"internalType":"uint16","name":"observationCardinalityNext","type":"uint16"},{"internalType":"uint8","name":"feeProtocol","type":"uint8"},{"internalType":"bool","name":"unlocked","type":"bool"}],"stateMutablower_tickity":"view","type":"function"}, \
            {"inputs":[],"name":"token0","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutablower_tickity":"view","type":"function"},\
            {"inputs":[],"name":"token1","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutablower_tickity":"view","type":"function"}, \
            {"inputs":[],"name":"feeGrowthGlobal0X128","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutablower_tickity":"view","type":"function"},\
            {"inputs":[],"name":"feeGrowthGlobal1X128","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutablower_tickity":"view","type":"function"}, \
            {"inputs":[{"internalType":"int24","name":"","type":"int24"}],"name":"ticks","outputs":[{"internalType":"uint128","name":"liquidityGross","type":"uint128"},{"internalType":"int128","name":"liquidityNet","type":"int128"},{"internalType":"uint256","name":"feeGrowthOutside0X128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthOutside1X128","type":"uint256"},{"internalType":"int56","name":"tickCumulativeOutside","type":"int56"},{"internalType":"uint160","name":"secondsPerLiquidityOutsideX128","type":"uint160"},{"internalType":"uint32","name":"secondsOutside","type":"uint32"},{"internalType":"bool","name":"initialized","type":"bool"}],"stateMutablower_tickity":"view","type":"function"}]'

# Uniswap v3 NFT manager - balanceOf, tokenofownerbyindex, positions, ownerof
ABI_POSITIONS_NFT: str = '[{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutablower_tickity":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"tokenOfOwnerByIndex","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutablower_tickity":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"positions","outputs":[{"internalType":"uint96","name":"nonce","type":"uint96"},{"internalType":"address","name":"operator","type":"address"},{"internalType":"address","name":"token0","type":"address"},{"internalType":"address","name":"token1","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"int24","name":"tickLower","type":"int24"},{"internalType":"int24","name":"tickUpper","type":"int24"},{"internalType":"uint128","name":"liquidity","type":"uint128"},{"internalType":"uint256","name":"feeGrowthInside0LastX128","type":"uint256"},{"internalType":"uint256","name":"feeGrowthInside1LastX128","type":"uint256"},{"internalType":"uint128","name":"tokensOwed0","type":"uint128"},{"internalType":"uint128","name":"tokensOwed1","type":"uint128"}],"stateMutablower_tickity":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"tokenId","type":"uint256"}],"name":"ownerOf","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutablower_tickity":"view","type":"function"}]'

# Uniswap v3 Quoter ABI
ABI_QUOTER_V3: str = '[{"inputs":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"name":"quoteExactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutablower_tickity":"nonpayable","type":"function"}]'


@dataclass
class Pool:
    blockchain: str
    block: int | str
    web3: object
    tokenA: str
    tokenB: str
    fee: int
    pool_contract: object = field(init=False)
    addr: object = field(init=False)
    current_tick: int = field(init=False)
    sqrt_price_x96: int = field(init=False)
    sqrt_price: Decimal = field(init=False)
    price: Decimal = field(init=False)
    token0: str = field(init=False)
    token1: str = field(init=False)

    def __post_init__(self) -> None:
        # From the factory address we get the pool address
        factory_address = get_contract(FACTORY, self.blockchain, self.web3, ABI_FACTORY)
        self.addr = factory_address.functions.getPool(self.tokenA, self.tokenB, self.fee).call(
            block_identifier=self.block
        )
        # We then initialize the pool contract to get the info about the tick, price and tokens.
        self.pool_contract = get_contract(self.addr, self.blockchain, self.web3, ABI_POOL)
        self.sqrt_price_x96, self.current_tick = self.pool_contract.functions.slot0().call(block_identifier=self.block)[
            0:2
        ]
        self.sqrt_price = Decimal(self.sqrt_price_x96) / Decimal(2**96)
        self.price = self.sqrt_price**2
        self.token0 = self.pool_contract.functions.token0().call(block_identifier=self.block)
        self.token1 = self.pool_contract.functions.token1().call(block_identifier=self.block)

    def get_fee_growth_indexes(self, lower_tick: int, upper_tick: int) -> tuple:
        """Function to get the fee growth indexes for a given tick range. lower_tick and upper_tick."""
        fee_growth_0 = self.pool_contract.functions.feeGrowthGlobal0X128().call(block_identifier=self.block)
        fee_growth_1 = self.pool_contract.functions.feeGrowthGlobal1X128().call(block_identifier=self.block)
        fee_growth_outside_0_low, fee_growth_outside_1_low = self.pool_contract.functions.ticks(lower_tick).call(
            block_identifier=self.block
        )[2:4]
        fee_growth_outside_0_up, fee_growth_outside_1_up = self.pool_contract.functions.ticks(upper_tick).call(
            block_identifier=self.block
        )[2:4]

        return (
            fee_growth_0,
            fee_growth_1,
            fee_growth_outside_0_low,
            fee_growth_outside_1_low,
            fee_growth_outside_0_up,
            fee_growth_outside_1_up,
        )


@dataclass
class NFTPosition:
    BASETICK: ClassVar[int] = 1.0001

    nftid: int
    blockchain: str
    block: int | str
    web3: object
    decimals: bool
    token0: str = field(init=False)
    token1: str = field(init=False)
    fee: int = field(init=False)
    lower_tick: int = field(init=False)
    upper_tick: int = field(init=False)
    fee_growth_inside_0: int = field(init=False)
    fee_growth_inside_1: int = field(init=False)
    liquidity: Decimal = field(init=False)
    decimals0: int = field(init=False)
    decimals1: int = field(init=False)

    def __post_init__(self) -> None:
        self._nft_contract = get_contract(POSITIONS_NFT, self.blockchain, web3=self.web3, abi=ABI_POSITIONS_NFT)
        (
            self.token0,
            self.token1,
            self.fee,
            self.lower_tick,
            self.upper_tick,
            liquidity,
            self.fee_growth_inside_0,
            self.fee_growth_inside_1,
        ) = self._nft_contract.functions.positions(self.nftid).call(block_identifier=self.block)[2:10]
        self.liquidity = Decimal(liquidity)
        if self.decimals:
            self.decimals0 = get_decimals(self.token0, self.blockchain, self.web3)
            self.decimals1 = get_decimals(self.token1, self.blockchain, self.web3)

    def owned_by(self, wallet: str) -> bool:
        wallet = Web3.to_checksum_address(wallet)
        nft_owner = self._nft_contract.functions.ownerOf(self.nftid).call(block_identifier=self.block)
        return nft_owner == wallet

    def get_fees(
        self,
        current_tick: int,
        fee_growth_0: int,
        fee_growth_1: int,
        fee_growth_outside_0_low: int,
        fee_growth_outside_1_low: int,
        fee_growth_outside_0_up: int,
        fee_growth_outside_1_up: int,
    ) -> list:
        if current_tick >= self.lower_tick:
            fee_lower_token0 = fee_growth_outside_0_low
            fee_lower_token1 = fee_growth_outside_1_low
        else:
            fee_lower_token0 = fee_growth_0 - fee_growth_outside_0_low
            fee_lower_token1 = fee_growth_1 - fee_growth_outside_1_low
        if current_tick >= self.upper_tick:
            fee_upper_token0 = fee_growth_0 - fee_growth_outside_0_up
            fee_upper_token1 = fee_growth_1 - fee_growth_outside_1_up
        else:
            fee_upper_token0 = fee_growth_outside_0_up
            fee_upper_token1 = fee_growth_outside_1_up

        fees_per_unit_0 = Decimal(
            (fee_growth_0 - fee_lower_token0 - fee_upper_token0 - self.fee_growth_inside_0) * self.liquidity
        ) / Decimal(2**128)
        fees_per_unit_1 = Decimal(
            (fee_growth_1 - fee_lower_token1 - fee_upper_token1 - self.fee_growth_inside_1) * self.liquidity
        ) / Decimal(2**128)

        return [fees_per_unit_0, fees_per_unit_1]

    def get_balance(
        self, current_tick: int, current_square_price: Decimal, fees_per_unit_0: int = 0, fees_per_unit_1: int = 0
    ) -> list:
        # TODO: get_balance output sould not be variable
        balances = []
        if self.liquidity != 0:
            sa = Decimal(self.BASETICK) ** Decimal(int(self.lower_tick) / 2)
            sb = Decimal(self.BASETICK) ** Decimal(int(self.upper_tick) / 2)

            if self.upper_tick <= current_tick:
                amount0 = 0
                amount0fee = fees_per_unit_0 if fees_per_unit_0 > 0 else 0
                amount1 = self.liquidity * (sb - sa)
                amount1fee = fees_per_unit_1
            elif self.lower_tick < current_tick < self.upper_tick:
                amount0 = self.liquidity * (sb - current_square_price) / (current_square_price * sb)
                amount0fee = fees_per_unit_0
                amount1 = self.liquidity * (current_square_price - sa)
                amount1fee = fees_per_unit_1
            else:
                amount0 = self.liquidity * (sb - sa) / (sa * sb)
                amount0fee = fees_per_unit_0
                amount1 = 0
                amount1fee = fees_per_unit_1 if fees_per_unit_1 > 0 else 0

            amount0 = Decimal(amount0) + Decimal(amount0fee)
            amount1 = Decimal(amount1) + Decimal(amount1fee)

            if self.decimals:
                amount0 = amount0 / Decimal(10**self.decimals0)
                amount1 = amount1 / Decimal(10**self.decimals1)

            if amount0 > 0:
                balances.append([self.token0, amount0])

            if amount1 > 0:
                balances.append([self.token1, amount1])
        return balances


def underlying(
    wallet: str,
    nftid: int,
    block: int | str,
    blockchain: str,
    web3=None,
    decimals: bool = True,
    fee: bool = False,
) -> list:
    """Returns the balances of the underlying assets corresponding to a position held by a wallet.

    Args:
        wallet (str): Address of the wallet holding the position.
        nftid (int): Address of the token identifying the position in the protocol.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (str): Blockchain in which the position is held.
        web3 (obj, optional): Already instantiated web3 object.
        decimals (bool, optional): Specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True.
        fee (bool, optional): If set to True, the balances of the unclaimed fees corresponding to the position are appended to the returned list.

    Returns:
        list: A list where each element is a list with two elements, the underlying token address and its corresponding amount.
    """
    balances = []
    if web3 is None:
        web3 = get_node(blockchain)

    nft_position = NFTPosition(nftid, blockchain, block, web3, decimals)
    if nft_position.owned_by(wallet):
        pool = Pool(blockchain, block, web3, nft_position.token0, nft_position.token1, nft_position.fee)

        if fee:
            growth_indexes = pool.get_fee_growth_indexes(nft_position.lower_tick, nft_position.upper_tick)
            fees_per_unit_0, fees_per_unit_1 = nft_position.get_fees(pool.current_tick, *growth_indexes)
            balances = nft_position.get_balance(pool.current_tick, pool.sqrt_price, fees_per_unit_0, fees_per_unit_1)
        else:
            balances = nft_position.get_balance(pool.current_tick, pool.sqrt_price)

    return balances


def get_fee(nftid: int, block: int | str, blockchain: str, web3=None, decimals: bool = True) -> list:
    """Returns the unclaimed fees corresponding to a nft id.

    Args:
        nftid (int): Number corresponding to a nftid.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (str): Blockchain in which the position is held.
        web3 (obj, optional): Already instantiated web3 object.
        decimals (bool, optional): Specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True.

    Returns:
        list: A list where each element is a list with two elements, the underlying token address and its corresponding unclaimed fee.
    """
    if web3 is None:
        web3 = get_node(blockchain)

    nft_position = NFTPosition(nftid, blockchain, block, web3, decimals)
    pool = Pool(blockchain, block, web3, nft_position.token0, nft_position.token1, nft_position.fee)

    growth_indexes = pool.get_fee_growth_indexes(nft_position.lower_tick, nft_position.upper_tick)
    fees_per_unit_0, fees_per_unit_1 = nft_position.get_fees(pool.current_tick, *growth_indexes)
    if decimals:
        fees_per_unit_0 = fees_per_unit_0 / Decimal(10**nft_position.decimals0)
        fees_per_unit_1 = fees_per_unit_1 / Decimal(10**nft_position.decimals1)
    return [[nft_position.token0, fees_per_unit_0], [nft_position.token1, fees_per_unit_1]]


def get_rate_uniswap_v3(
    token_src: str, token_dst: str, block: int | str, blockchain: str, web3=None, fee: int = FeeAmount.LOWEST
) -> Decimal:
    """Returns the price of a token.

    Args:
        token_src (str): Address of the source token of the pool.
        token_dst (str): Address of the destination token of the pool.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (str): Blockchain in which the position is held.
        web3 (obj, optional): Already instantiated web3 object.
        fee (int, optional): Fee which is set for this pool.

    Returns:
        Decimal: The token price of the source token (token_src) quoted in destination token.
    """
    if web3 is None:
        web3 = get_node(blockchain)

    token_src = Web3.to_checksum_address(token_src)
    token_dst = Web3.to_checksum_address(token_dst)
    token_src_decimals = get_decimals(token_src, blockchain, web3=web3)
    token_dst_decimals = get_decimals(token_dst, blockchain, web3=web3)

    pool = Pool(blockchain, block, web3, token_src, token_dst, fee)

    if token_src == pool.token0:
        factor = pool.price
    else:
        factor = 1 / pool.price

    return factor / Decimal(10 ** (token_dst_decimals - token_src_decimals))


def allnfts(wallet: str, block: int | str, blockchain: str, web3=None) -> list:
    """Returns all nft ids owned by a wallet.

    Args:
        wallet (str): Address of the wallet holding the position.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (str): Blockchain in which the position is held.
        web3 (obj, optional): Already instantiated web3 object.

    Returns:
        list: A list where each element is the nft id that is owned by the wallet (open and closed nfts).
    """
    nftids = []

    if web3 is None:
        web3 = get_node(blockchain)

    nft_contract = get_contract(POSITIONS_NFT, blockchain, web3=web3, abi=ABI_POSITIONS_NFT)
    nfts = nft_contract.functions.balanceOf(wallet).call(block_identifier=block)
    for nft_index in range(nfts):
        nft_id = nft_contract.functions.tokenOfOwnerByIndex(wallet, nft_index).call(block_identifier=block)
        nftids.append(nft_id)
    return nftids


def underlying_all(wallet: str, block: int | str, blockchain: str, decimals: bool = True, fee: bool = False):
    """Returns the balances of the underlying assets corresponding to all positions held by a wallet.

    Args:
        wallet (str): Address of the wallet holding the position.
        block (int or 'latest'): Block number at which the data is queried.
        blockchain (str): Blockchain in which the position is held.
        decimals (bool, optional): Specifies whether balances are returned as int if set to False, or float with the appropriate decimals if set to True. Defaults to True.
        fee (bool, optional): Specifies whether to include unclaimed fee. Defaults to False.

    Returns:
        list: A list where each element is a list with two elements, the underlying token address and its corresponding amount (with optional unclaimed fee).
    """

    balances = []
    for nft in allnfts(wallet, block, blockchain):
        balances.append(underlying(wallet, nft, block, blockchain, decimals=decimals, fee=fee))
    return list(filter(None, balances))
