from datetime import datetime, timedelta, timezone

import pytest

from defyes import lazytime
from defyes.lazytime import Duration, Time

timestamp = 1698075172.5
utc2 = timezone(timedelta(hours=2), "UTC")


@pytest.fixture()
def repr_tz_utc(monkeypatch):
    monkeypatch.setattr(lazytime, "repr_tz", timezone.utc)


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


def test_time_is_float():
    assert isinstance(t := Time.from_now(), Time)
    assert isinstance(t, float)


def test_time_calendar_type(repr_tz_utc):
    assert isinstance(Time(0).calendar, datetime)


def test_time_calendar_just_change_representation(repr_tz_utc):
    dt0 = Time(0).calendar
    assert dt0 == datetime(1970, 1, 1, tzinfo=timezone.utc)

    lazytime.repr_tz = lazytime.utc(2)
    dt2 = Time(0).calendar
    assert dt2 == datetime(1970, 1, 1, 2, tzinfo=utc2)

    assert dt0 == dt2


def test_time_repr(repr_tz_utc):
    assert repr(Time(0)) == "'1970-01-01 00:00:00'"
    lazytime.repr_tz = lazytime.utc(2)
    assert repr(Time(0)) == "'1970-01-01 02:00:00 UTC+0200'"


def test_time_from_calendar_is_always_utc_default(repr_tz_utc):
    assert Time.from_calendar(1970, 1, 1, 0, 0, 1, 100_000) == 1.1
    lazytime.repr_tz = lazytime.utc(-3)  # it does nothing
    assert Time.from_calendar(1970, 1, 1, 0, 0, 1, 100_000) == 1.1


def test_time_from_calendar_different_tzinfo(repr_tz_utc):
    assert Time.from_calendar(1970, 1, 1, 2, 0, 1, 100_000, tzinfo=utc2) == 1.1
    lazytime.repr_tz = lazytime.utc(-3)  # it does nothing
    assert Time.from_calendar(1970, 1, 1, 2, 0, 1, 100_000, tzinfo=utc2) == 1.1


def test_time_from_string(repr_tz_utc):
    assert Time.from_string("1970-01-01 00:00:00") == 0
    assert Time.from_string("1970-01-01 02:00:00 UTC+0200") == 0


def test_time_from_string_invariant(repr_tz_utc):
    """
    Changing the repr_tz doesn't affect the string parsing.
    """
    lazytime.repr_tz = lazytime.utc(2)
    assert Time.from_string("1970-01-01 00:00:00") == 0
    assert Time.from_string("1970-01-01 02:00:00 UTC+0200") == 0


def test_time_sub():
    assert isinstance(f := Time(10) - Time(9), Duration)
    assert isinstance(f, float)
    assert f == 1

    assert isinstance(f := Time(10) - Duration(9), Time)
    assert isinstance(f, float)
    assert f == 1

    assert isinstance(f := Time(10) - 9, Time)
    assert isinstance(f, float)
    assert f == 1


@pytest.mark.parametrize(
    "d", [Time(10) + Duration(9), Duration(9) + Time(10), Time(10) + 9, 9 + Time(10)], ids=["T+D", "D+T", "T+f", "f+T"]
)
def test_time_add(d):
    assert isinstance(d, Time)
    assert isinstance(d, float)
    assert d == 19
