import logging
import os

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-rabbit-monitor: %(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))

PORT = os.getenv('SDX_RABBIT_MONITOR_PORT')
RABBITMQ_DEFAULT_PASS = os.getenv('SDX_RABBIT_MONITOR_PASS')
RABBITMQ_DEFAULT_USER = os.getenv('SDX_RABBIT_MONITOR_USER')
RABBITMQ_DEFAULT_VHOST = '%2f'

RABBIT_URL = 'http://{hostname}:{port}/api/'.format(
    hostname=os.getenv('SDX_RABBIT_MONITOR_RABBIT_HOST'),
    port=os.getenv('SDX_RABBIT_MONITOR_MGT_PORT')
)


WAIT_TIME = 120

# Number of seconds to look back and gather stats from
RABBIT_MONITOR_STATS_WINDOW = 120

# Sample frequency in stats window
RABBIT_MONITOR_STATS_INCREMENT = '30'
