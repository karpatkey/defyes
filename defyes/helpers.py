"""
This module provides a utility decorator `timeit` for timing the execution of methods.

The `timeit` decorator measures the time taken to execute a method and stores the timing in the object's dictionary.
The timing information includes the duration of the last call,
 the cumulative sum of all call durations, and the number of calls made.

Functions:
    timeit(method): A decorator that times the execution of a method and stores the timing in the object's dictionary.
"""

import time
from functools import wraps

from defyes.lazytime import Duration


def timeit(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        t0 = time.monotonic()
        result = method(self, *args, **kwargs)
        t1 = time.monotonic()
        attr = f"{method.__name__}_timeit"
        try:
            ti = self.__dict__[attr]
        except KeyError:
            ti = {}
        cumsum = ti.get("cumsum", 0)
        n_calls = ti.get("n_calls", 0)
        duration = Duration.seconds(t1 - t0)
        cumsum += duration
        n_calls += 1
        self.__dict__[attr] = {
            "last_call": {"duration": duration, "args": args, "kwargs": kwargs},
            "cumsum": cumsum,
            "n_calls": n_calls,
        }
        return result

    return wrapper
