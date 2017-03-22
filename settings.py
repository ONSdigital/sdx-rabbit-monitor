import logging
import os

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-rabbit-monitor: %(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))
