import inspect
import logging

logger = logging.getLogger(__name__)


class Updater:
    def __init__(self):
        self.callbacks = list()

    def register(self, func):
        frame = inspect.stack()[1]
        self.callbacks.append((func, frame))

    def update_all(self):
        logger.info("Updating all ...")
        for callback, frame in self.callbacks:
            func_path = f"{callback.__module__}.{callback.__qualname__}"
            call_path = f"{frame.filename}:{frame.lineno}"
            logger.info(f"Calling {func_path} from {call_path} ...")
            callback()


updater = Updater()
