from dataclasses import dataclass
from functools import cached_property
from math import log10
from typing import NamedTuple

from .lazytime import Duration, Time

year = Duration.days(365)


class FormatedFloat(float):
    template = "{:.3f}"

    def __repr__(self):
        return self.template.format(self)


class Percent(FormatedFloat):
    template = "{:.3f}%"


class MilliBell(FormatedFloat):
    template = "{:.4g}mB"


class Factor(float):
    @property
    def percent(self) -> float:
        return Percent(100 * (self - 1))

    @property
    def millibell(self) -> float:
        return MilliBell(1000 * log10(self))


class ChainedPrice(NamedTuple):
    price: float
    block_id: int
    time: Time


@dataclass
class Interval:
    initial: ChainedPrice
    final: ChainedPrice

    @cached_property
    def rate(self) -> Factor:
        try:
            return Factor(self.final.price / self.initial.price)
        except TypeError:
            if self.final.price is None or self.initial.price is None:
                return None
            else:
                raise

    @cached_property
    def duration(self) -> Duration:
        return Duration(self.final.time - self.initial.time)

    @cached_property
    def apy(self):
        return Factor(apy(price_factor=self.rate, time_fraction=self.duration / year))


def apy(price_factor, time_fraction, periods=1):
    assert time_fraction <= 1, "Extrapolation error"
    exponent = periods + (1 - time_fraction)
    return (1 + (price_factor - 1) / exponent) ** exponent
