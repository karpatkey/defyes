"""
This module provides a utility class `Updater` for managing callbacks.
It is supposed to be used once in a while to update all registered callbacks.
An example of a function that can be registered as a callback is `update_jsons` in `defyes/protocols/aura/newarch.py`.
"""

import inspect
import logging

logger = logging.getLogger(__name__)


class Updater:
    """
    A class that manages callbacks.

    This class provides methods to register functions as callbacks and to call all registered callbacks.

    """

    def __init__(self):
        self.callbacks = list()

    def register(self, func):
        """
        Register a function as a callback.

        The function and the frame in which it was registered are added to the list of callbacks.

        Can be used as a decorator:
            @management.updater.register
            def generic_function():
                print("hi!")
        """
        frame = inspect.stack()[1]
        self.callbacks.append((func, frame))

    def update_all(self):
        """
        Call all registered callbacks. Runs the functions in the order they were registered.

        For each callback, a log message is generated that includes the path of the callback function
        and the location from which it was registered.
        """
        logger.info("Updating all ...")
        for callback, frame in self.callbacks:
            func_path = f"{callback.__module__}.{callback.__qualname__}"
            call_path = f"{frame.filename}:{frame.lineno}"
            logger.info(f"Calling {func_path} from {call_path} ...")
            callback()


updater = Updater()
