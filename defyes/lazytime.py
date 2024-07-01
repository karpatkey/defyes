"""
# Lazy Time

The main resources from this module are the classes Duration and Time.

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


class RelativeTime(Duration):
    cases = [
        ("second", "seconds", Duration.minutes(1)),
        ("minute", "minutes", Duration.hours(1)),
        ("hour", "hours", Duration.days(1)),
        ("day", "days", Duration.weeks(1)),
        ("week", "weeks", Duration.days(30)),
        ("month", "months", Duration.days(365)),
        ("year", "years", float("inf")),
    ]

    @classmethod
    def _abs_unit(cls, time):
        abs_t = abs(time)
        divider = 1
        for singular, plural, limit in cls.cases:
            if abs_t < limit:
                t_units = int(abs_t / divider)
                return (1, singular) if t_units == 1 else (t_units, plural)
            divider = limit

    @cached_property
    def humanized(self):
        if abs(self) < 1:
            return "now"
        abs_t_units, unit = self._abs_unit(self)
        if self < 0:
            return f"about {abs_t_units:.0f} {unit} ago"
        else:
            return f"in about {abs_t_units:.0f} {unit}"


class Time(float):
    """
    A regular float class which represents the float POSIX timestamp in seconds, with a lazy conversion to an aware
    datetime, or string, using `repr_tz` as default timezone for representation.
    """

    isoformat = {
        "sep": " ",
        "timespec": "auto",
    }

    time_interval_class = Duration
    relative_time_class = RelativeTime

    @cached_property
    def calendar(self) -> datetime:
        return datetime.fromtimestamp(self, tz=repr_tz)

    def __repr__(self):
        return repr(str(self))

    def __str__(self):
        string = self.calendar.isoformat(**self.isoformat)
        return string[:-6] if string.endswith("+00:00") else string

    @classmethod
    def from_calendar(
        cls, year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
    ) -> TimeOrDerived:
        try:
            return cls(datetime(year, month, day, hour, minute, second, microsecond, tzinfo=tzinfo).timestamp())
        except TypeError:
            string = year
            return cls.from_string(string)

    @classmethod
    def from_string(cls, string: str):
        dt = datetime.fromisoformat(string)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return cls(dt.timestamp())

    @classmethod
    def now(cls):
        return cls(time.time())

    @property
    def since_now(self) -> relative_time_class:
        return self.relative_time_class(self - time.time())

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
