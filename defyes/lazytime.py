"""
# Lazy Time

The main resources from this module are the clases Duration and Time, which internally use the funcions `calendar` and
`calendar_from_time`.

The idea is not to deal with mixed timezone, but you could modify the process level configuration of `default_tz` to use
a different timezone from UTC for calendar representation of time and for calendar interpretation of time, for example
when the user code refers to the begining of a day.

In case you wanted to modify the `default_tz`, this module has a `simple_change_utc` function to just add an UTC offset.
"""

import time
from datetime import datetime, timedelta, timezone
from functools import cached_property
from typing import TypeVar

from dateutil.parser import parse

default_tz = timezone.utc


def simple_change_utc(offset_in_hours):
    """
    This function modify the global `default_tz` using a datetime.timezone object as tzinfo, which is a simple way the
    add and offset to UTC. This is simpler than `pytz`, but you could set `default_tz` manually with an tzinfo from
    `pytz` as well.
    """
    global default_tz
    default_tz = timezone(timedelta(hours=offset_in_hours), "UTC")


def calendar(year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) -> datetime:
    """
    Aware `datetime`, from calendar parameters, but with tzinfo using `default_tz`.
    """
    return datetime(year, month, day, hour, minute, second, microsecond, tzinfo=default_tz)


def calendar_from_time(timestamp) -> datetime:
    """
    Aware `datetime`, from POSIX timestamp, but with tzinfo using `default_tz`.
    """
    return datetime.fromtimestamp(timestamp, tz=default_tz)


DurationOrDerived = TypeVar("DurationOrDerived", bound="Duration")


class Duration(float):
    """
    A regular float class which represent a duration in seconds, but it could be constructed from several time units,
    like timedelta, but faster than that if timedelta.total_seconds() is expected included in the computation.
    """

    @cached_property
    def timedelta(self) -> timedelta:
        return timedelta(seconds=self)

    def __repr__(self):
        return f"Duration.sum{repr(self.timedelta)[18:]}"

    @classmethod
    def sum(cls, days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=0, weeks=0) -> DurationOrDerived:
        s = seconds
        if weeks:
            s += weeks * 604_800
        if days:
            s += days * 86_400
        if hours:
            s += hours * 3_600
        if minutes:
            s += minutes * 60
        if milliseconds:
            s += milliseconds / 1_000
        if microseconds:
            s += microseconds / 1_000_000
        return cls(s)

    @classmethod
    def seconds(cls, seconds) -> DurationOrDerived:
        return cls(seconds)

    @classmethod
    def weeks(cls, weeks) -> DurationOrDerived:
        return cls(604_800 * weeks)

    @classmethod
    def days(cls, days) -> DurationOrDerived:
        return cls(86_400 * days)

    @classmethod
    def hours(cls, hours) -> DurationOrDerived:
        return cls(3_600 * hours)

    @classmethod
    def minutes(cls, minutes) -> DurationOrDerived:
        return cls(60 * minutes)

    @classmethod
    def milliseconds(cls, milliseconds) -> DurationOrDerived:
        return cls(milliseconds / 1_000)

    @classmethod
    def microseconds(cls, microseconds) -> DurationOrDerived:
        return cls(microseconds / 1_000_000)

    def __sub__(self, other) -> DurationOrDerived:
        return self.__class__(super().__sub__(other))

    __rsub__ = __sub__

    def __add__(self, other) -> DurationOrDerived:
        result = super().__add__(other)
        if isinstance(other, self.absolut_time_class):
            return self.absolut_time_class(result)
        else:
            return self.__class__(result)

    __radd__ = __add__

    def __mul__(self, other) -> DurationOrDerived:
        return self.__class__(super().__mul__(other))

    __rmul__ = __mul__

    def __truediv__(self, other) -> DurationOrDerived:
        result = super().__truediv__(other)
        return result if isinstance(other, self.__class__) else self.__class__(result)

    def __neg__(self) -> DurationOrDerived:
        return self.__class__(super().__neg__())


TimeOrDerived = TypeVar("TimeOrDerived", bound="Time")


class Time(float):
    """
    A regular float class which represent the POSIX timestamp, with a lazy conversion to datetime aware with UTC default
    when expecting its representation or when using the .calendar property.
    """

    @property
    def format(self):
        return "%Y-%m-%d %H:%M:%S" if default_tz == timezone.utc else "%Y-%m-%d %H:%M:%S %Z%z"

    time_interval_class = Duration

    @cached_property
    def calendar(self) -> datetime:
        return calendar_from_time(self)

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        return self.calendar.strftime(self.format)

    @classmethod
    def from_calendar(cls, year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0) -> TimeOrDerived:
        try:
            return cls(calendar(year, month, day, hour, minute, second, microsecond).timestamp())
        except TypeError:
            return cls(datetime.strptime(year, cls.format).replace(tzinfo=timezone.utc).timestamp())

    @classmethod
    def from_string(cls, string: str):
        dt = parse(string)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=default_tz)
        return cls(dt.timestamp())

    @classmethod
    def from_now(cls):
        return cls(time.time())

    def __sub__(self, other) -> time_interval_class | TimeOrDerived:
        result = super().__sub__(other)
        if isinstance(other, self.__class__):
            return self.time_interval_class(result)
        else:
            return self.__class__(result)

    def __add__(self, other) -> TimeOrDerived:
        return self.__class__(super().__add__(other))

    __radd__ = __add__


Duration.absolut_time_class = Time
