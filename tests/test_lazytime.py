from datetime import datetime, timedelta, timezone

import pytest

from defyes import lazytime
from defyes.lazytime import Duration

timestamp = 1698075172.5


@pytest.fixture()
def utc(monkeypatch):
    monkeypatch.setattr(lazytime, "default_tz", timezone.utc)


def test_calendar(utc):
    assert lazytime.calendar(2023, 10, 23, 13, 34, 54) == datetime(2023, 10, 23, 13, 34, 54, tzinfo=timezone.utc)
    lazytime.simple_change_utc(-3)
    assert lazytime.calendar(2023, 10, 23, 10, 34, 54) == datetime(2023, 10, 23, 13, 34, 54, tzinfo=timezone.utc)
    # Calendar changes from the hour 13 to 10 to be the same UTC time


def test_calendar_from_time(utc):
    dt = lazytime.calendar_from_time(timestamp)
    assert dt == datetime(2023, 10, 23, 15, 32, 52, 500000, tzinfo=timezone.utc)
    assert dt.tzinfo == timezone.utc

    lazytime.simple_change_utc(-3)
    dt = lazytime.calendar_from_time(timestamp)
    assert dt == datetime(2023, 10, 23, 15, 32, 52, 500000, tzinfo=timezone.utc)
    # The default_tz change doesn't affect the comparison with the same datetime UTC instant, but it has a different
    # timezone
    assert dt.tzinfo != timezone.utc


def test_duration_is_float():
    units = "weeks days hours minutes milliseconds microseconds".split()
    for unit in units:
        assert isinstance(Duration.sum(**{unit: 1}), float)
        assert isinstance(getattr(Duration, unit)(1), float)


def test_duration_seconds():
    assert Duration(3.5) == Duration.seconds(3.5) == Duration.sum(seconds=3.5) == 3.5


def test_duration_minutes():
    assert Duration.minutes(2) == Duration.sum(minutes=2) == 120


def test_duration_hour():
    assert Duration.hours(1) == Duration.sum(hours=1) == 3600


def test_duration_days():
    assert Duration.days(1) == Duration.sum(days=1) == Duration.hours(24)


def test_duration_weeks():
    assert Duration.weeks(3) == Duration.sum(weeks=3) == Duration.days(21)


def test_duration_milliseconds():
    assert Duration.milliseconds(1) == Duration.sum(milliseconds=1) == 0.001


def test_duration_microseconds():
    assert Duration.microseconds(1) == Duration.sum(microseconds=1) == 0.000001


def test_duration_sum_full():
    assert Duration.sum(weeks=1, days=1, hours=1, minutes=1, seconds=1, milliseconds=1, microseconds=1) == 694861.001001


def test_duration_datetime():
    td = Duration.seconds(694861.001001).timedelta
    assert isinstance(td, timedelta)
    assert td == timedelta(weeks=1, days=1, hours=1, minutes=1, seconds=1, milliseconds=1, microseconds=1)


def test_duration_repr():
    d = Duration.sum(weeks=1, days=1, hours=1, minutes=1, seconds=1, milliseconds=1, microseconds=1)
    assert repr(d) == "Duration.sum(days=8, seconds=3661, microseconds=1001)"


@pytest.mark.parametrize(
    "d",
    [86_400 + Duration.weeks(1), Duration.weeks(1) + 86_400, Duration.weeks(1) + Duration.days(1)],
    ids=["float+D", "D+float", "D+D"],
)
def test_duration_add(d):
    assert isinstance(d, Duration)
    assert isinstance(d, float)
    assert d == Duration.days(8)


@pytest.mark.parametrize(
    "d",
    [86_400 - Duration.days(1), Duration.days(1) - 86_400, Duration.days(1) - Duration.days(1)],
    ids=["float-D", "D-float", "D-D"],
)
def test_duration_sub(d):
    assert isinstance(d, Duration)
    assert isinstance(d, float)
    assert d == 0


@pytest.mark.parametrize("d", [2 * Duration(3), Duration(3) * 2], ids=["float*D", "D*float"])
def test_duration_mul(d):
    assert isinstance(d, Duration)
    assert isinstance(d, float)
    assert d == 6


def test_duration_div():
    assert isinstance(d := Duration(3) / 3, Duration)
    assert isinstance(d, float)
    assert d == 1

    assert not isinstance(d := 3 / Duration(3), Duration)
    assert isinstance(d, float)
    assert d == 1

    assert not isinstance(d := Duration(3) / Duration(3), Duration)
    assert isinstance(d, float)
    assert d == 1


def test_duration_neg():
    assert isinstance(d := -Duration(3), Duration)
    assert isinstance(d, float)
    assert d == -3
