import logging
import sys

from defyes import add_stderr_logger

logger = logging.getLogger(__name__)
add_stderr_logger()
try:
    command = sys.argv[1]
except IndexError:
    logger.error("Try command 'update' to run the updater.")
else:
    match command:
        case "update":
            from defyes import management, portfolio  # noqa

            management.updater.update_all()
        case _:
            logger.error(f"Unknown command {command!r}.")
