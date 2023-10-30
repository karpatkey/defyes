import pytest
from pytest import approx

from defyes import financial
from defyes.financial import ChainedPrice, Duration, Factor, FormatedFloat, Interval, MilliBell, Percent, Time


def test_formated_float():
    f = FormatedFloat(3.1415)
    assert isinstance(f, float)
    assert repr(f) == "3.142"


def test_percent(monkeypatch):
    monkeypatch.setattr(Percent, "template", "{:.3f}%")
    f = Percent(0.3456)
    assert isinstance(f, float)
    assert repr(f) == "0.346%"


def test_millibell():
    f = MilliBell(-1.3456)
    assert isinstance(f, float)
    assert repr(f) == "-1.346mB"


def test_factor():
    f = Factor(1.03125)
    assert isinstance(f, float)

    assert isinstance(f.percent, Percent)
    assert f.percent == 3.125
    assert repr(f.percent) == "3.125%"

    assert isinstance(f.millibell, MilliBell)
    assert f.millibell == approx(13.364, abs=1e-3)
    assert repr(f.millibell) == "13.36mB"


def test_chained_price():
    p = ChainedPrice(2.5, 1234, t := Time.from_calendar(2023, 1, 1))
    assert p.price == 2.5
    assert p.block_id == 1234
    assert p.time == t


@pytest.mark.parametrize("p", [1, 0.5], ids=["year", "half year"])
def test_interval(p):
    any_ = 1234
    initial_time = Time.from_calendar(2023, 1, 1)
    interval = Interval(
        initial=ChainedPrice(price=1, time=initial_time, block_id=any_),
        final=ChainedPrice(price=2, time=initial_time + Duration.days(365 * p), block_id=any_),
    )
    assert interval.rate == 2
    assert interval.rate.percent == 100
    assert interval.rate.millibell == approx(301, abs=1)
    assert interval.duration == Duration.days(365) * p

    if p == 1:  # year
        assert interval.apy == 2
        assert interval.apy.percent == 100
        assert interval.apy.millibell == approx(301, abs=1)
    elif p == 0.5:  # half year
        assert interval.apy == approx(4, abs=1e-3)
        assert interval.apy.percent == approx(300, abs=1)
        assert interval.apy.millibell == approx(602, abs=1)


def test_apy():
    apy = financial.apy(price_factor=2, time_fraction=0.5)
    assert apy == 4
    assert apy.percent == 300
