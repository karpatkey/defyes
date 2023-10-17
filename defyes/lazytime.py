import time
from datetime import datetime, timedelta, timezone
from functools import cached_property, partial
from typing import TypeVar

utc = partial(datetime, tzinfo=timezone.utc)
utc_from_timestamp = partial(datetime.fromtimestamp, tz=timezone.utc)

DurationOrDerived = TypeVar("DurationOrDerived", bound="Duration")


class Duration(float):
    """
    A regular float class which represent a duration in seconds, but it could be constructed from several time units,
    like timedelta, but faster that that if timedelta.total_seconds() is expected included in the computation.
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
            s += weeks * 604800
        if days:
            s += days * 86400
        if hours:
            s += hours * 3600
        if minutes:
            s += minutes * 60
        if milliseconds:
            s += milliseconds / 1000
        if microseconds:
            s += microseconds / 1000000
        return cls(s)

    @classmethod
    def weeks(cls, weeks) -> DurationOrDerived:
        return cls(604800 * weeks)

    @classmethod
    def days(cls, days) -> DurationOrDerived:
        return cls(86400 * days)

    @classmethod
    def hours(cls, hours) -> DurationOrDerived:
        return cls(3600 * hours)

    @classmethod
    def minutes(cls, minutes) -> DurationOrDerived:
        return cls(60 * minutes)

    @classmethod
    def milliseconds(cls, milliseconds) -> DurationOrDerived:
        return cls(milliseconds / 1000)

    @classmethod
    def microseconds(cls, microseconds) -> DurationOrDerived:
        return cls(microseconds / 1000000)

    def __sub__(self, other) -> DurationOrDerived:
        return self.__class__(super().__sub__(other))

    def __add__(self, other) -> DurationOrDerived:
        result = super().__add__(other)
        if isinstance(other, self.absolut_time_class):
            return self.absolut_time_class(result)
        else:
            return self.__class__(result)

    __radd__ = __add__

    def __mul__(self, other) -> DurationOrDerived:
        return self.__class__(super().__mul__(other))

    def __div__(self, other) -> DurationOrDerived:
        return self.__class__(super().__div__(other))

    def __neg__(self) -> DurationOrDerived:
        return self.__class__(super().__neg__())


Duration.seconds = classmethod(Duration)


TimeOrDerived = TypeVar("TimeOrDerived", bound="Time")


class Time(float):
    """
    A regular float class which represent the POSIX timestamp, with a lazy conversion to UTC datetime when expecting its
    representation or when using the .utc property.
    """

    format = "%Y-%m-%d %H:%M:%S UTC"

    time_interval_class = Duration

    @cached_property
    def utc(self):
        return utc_from_timestamp(self)

    def __repr__(self):
        return repr(self.utc.strftime(self.format))

    @classmethod
    def from_utc(cls, year, month=1, day=1, hour=0, minute=0, second=0, microsecond=0):
        try:
            return cls(utc(year, month, day, hour, minute, second, microsecond).timestamp())
        except TypeError:
            return cls(datetime.strptime(year, cls.format).replace(tzinfo=timezone.utc).timestamp())

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

    def __radd__(self, other) -> TimeOrDerived:
        return self.__class__(super().__radd__(other))


Duration.absolut_time_class = Time
