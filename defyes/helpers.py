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
