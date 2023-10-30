from dataclasses import dataclass
from functools import cached_property
from math import log10

from .lazytime import Duration, Time

year = Duration.days(365)


class FormatedFloat(float):
    template = "{:.3f}"

    def __repr__(self):
        return self.template.format(self)


class Percent(FormatedFloat):
    template = "{:.4g}%"


class MilliBell(FormatedFloat):
    template = "{:.4g}mB"


class Factor(float):
    @property
    def percent(self) -> Percent:
        return Percent(100 * (self - 1))

    @property
    def millibell(self) -> MilliBell:
        return MilliBell(1000 * log10(self))


@dataclass(frozen=True)
class ChainedPrice:
    price: float
    block_id: int
    time: Time


@dataclass(frozen=True)
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
    def apy(self) -> Factor:
        return apy(price_factor=self.rate, time_fraction=self.duration / year)


def apy(price_factor, time_fraction) -> Factor:
    assert time_fraction <= 1, "Extrapolation error"
    return Factor(price_factor ** (1 / time_fraction))
