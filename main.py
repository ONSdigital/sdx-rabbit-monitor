import logging
import sys

import requests
from structlog import wrap_logger

import settings

__version__ = "0.0.1"

logging.basicConfig(level=settings.LOGGING_LEVEL,
                    format=settings.LOGGING_FORMAT)
logger = wrap_logger(logging.getLogger(__name__))


def shutdown():
    logger.info("Shutting down")
    sys.exit(0)

def main():
    logger.info("Starting rabbit monitor")
    while True:
        pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
