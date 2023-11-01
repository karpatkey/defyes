"""
# Lazy Time

The main resources from this module are the clases Duration and Time.

The calendar interpretation of time is always aware with default UTC. It includes string and tuple/args interpretation.
But you could specify for example UTC-0300 at the end of the string or a `tzinfo` when using `Time.from_calendar`.

You could modify the process level value of `repr_tz` to use a different timezone just for calendar representation of
time, which includes string and datetime representation.

In case you wanted to modify the `repr_tz`, you could use the helper `utc(hours)` to generate a tzinfo object.
"""

import time
from datetime import datetime, timedelta, timezone
from functools import cached_property
from typing import TypeVar

repr_tz = timezone.utc


def utc(hours=0):
    """
    Generate a tzinfo object with an offset with respect to UTC, otherwise return timezone.utc.
    """
    if hours == 0:
        return timezone.utc
    else:
        return timezone(timedelta(hours=hours), "UTC")


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
    A regular float class which represent the POSIX timestamp, with a lazy conversion to datetime aware with repr_tz
    when expecting its string or datetime representation.
    """

    utc_format = "%Y-%m-%d %H:%M:%S"
    general_format = "%Y-%m-%d %H:%M:%S %Z%z"

    @property
    def format(self):
        return self.utc_format if repr_tz == timezone.utc else self.general_format

    time_interval_class = Duration

    @cached_property
    def calendar(self) -> datetime:
        return datetime.fromtimestamp(self, tz=repr_tz)

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        return self.calendar.strftime(self.format)

    @classmethod
    def from_calendar(
        cls, year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    ) -> TimeOrDerived:
        try:
            return cls(datetime(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo).timestamp())
        except TypeError:
            return cls(datetime.strptime(year, cls.format).replace(tzinfo=timezone.utc).timestamp())

    @classmethod
    def from_string(cls, string: str):
        try:
            dt = datetime.strptime(string, cls.utc_format)
        except ValueError:
            dt = datetime.strptime(string, cls.general_format)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
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
