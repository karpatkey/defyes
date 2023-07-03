import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class LiquidityPosition:
    # token0: int
    fee: int
    currentprice: int
    # token1: Optional[int] = None
    amount0: Optional[int] = 0
    amount1: Optional[int] = 0
    percentupper: Optional[int] = 0
    percentlower: Optional[int] = 0
    upperprice: Optional[int] = None
    lowerprice: Optional[int] = None
    uppertick: Optional[int] = None
    lowertick: Optional[int] = None
    basetick: int = 1.0001

    def __post_init__(self):
        self.tickspacing = self.get_tickspacing()
        self.percentupper = (1 + (self.percentupper / 100)) * self.currentprice
        self.percentlower = (1 + (self.percentlower / 100)) * self.currentprice
        self.sqrcurrentprice = self.currentprice**0.5

        if self.upperprice is not None:
            self.upperprice = self.get_price(self.upperprice)
        elif self.uppertick is not None:
            self.upperprice = self.get_price((self.basetick ** (self.uppertick / 2)) ** 2)
        else:
            self.upperprice = self.get_price(self.percentupper)

        if self.lowerprice is not None:
            self.lowerprice = self.get_price(self.lowerprice)
        elif self.lowertick is not None:
            self.lowerprice = self.get_price((self.basetick ** (self.lowertick / 2)) ** 2)
        else:
            self.lowerprice = self.get_price(self.percentlower)
        self.sqrupperprice = self.upperprice**0.5
        self.sqrlowerprice = self.lowerprice**0.5
        self.liquidity = self.get_liquidity()
        self.uppertick = 2 * math.log(self.sqrupperprice) / math.log(self.basetick)
        self.lowertick = 2 * math.log(self.sqrlowerprice) / math.log(self.basetick)

    def get_price(self, price) -> int:
        pricesqr = math.sqrt(price)
        tick = 2 * math.log(pricesqr) / math.log(self.basetick)
        rounded = round(tick / self.tickspacing)
        tickdef = self.basetick ** ((rounded * self.tickspacing) / 2)
        return tickdef * tickdef

    def get_liquidity(self) -> int:
        if self.amount0 > 0:
            return (
                self.amount0 * self.sqrcurrentprice * self.sqrupperprice / (self.sqrupperprice - self.sqrcurrentprice)
            )
        else:
            return self.amount1 / (self.sqrcurrentprice - self.sqrlowerprice)

    def get_tickspacing(self) -> int:
        for k, v in [[1, 200], [0.3, 60], [0.01, 1], [0.05, 10]]:
            if k == self.fee:
                return v

    def get_amount1(self) -> int:
        amount1 = self.liquidity * (self.sqrcurrentprice - self.sqrlowerprice)
        return "Amount1 needed is: {}, with lowertick: {} and lowerprice: {}, uppertick: {} and upperprice: {}, fee: {} and currentprice: {}".format(
            amount1, self.lowertick, self.lowerprice, self.uppertick, self.upperprice, self.fee, self.currentprice
        )

    def get_amount0(self) -> int:
        amount0 = (
            self.liquidity * (self.sqrupperprice - self.sqrcurrentprice) / (self.sqrcurrentprice * self.sqrupperprice)
        )
        return "Amount0 needed is: {}, with lowertick: {} and lowerprice: {}, uppertick: {} and upperprice: {}, fee: {} and currentprice: {}".format(
            amount0, self.lowertick, self.lowerprice, self.uppertick, self.upperprice, self.fee, self.currentprice
        )


# test = LiquidityPosition(fee=0.3, amount1=10000, currentprice=1210.62, percentupper=78, percentlower=-49)
# print(test.get_amount0())

# test = LiquidityPosition(fee=0.3, amount0=5, currentprice=1210.62, upperprice=2000, lowerprice=600)
# print(test.get_amount1())

# test = LiquidityPosition(fee=0.3, amount0=5, currentprice=0.072139, uppertick=-19380, lowertick=-31680)
# print(test.get_amount1())
