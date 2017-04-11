import logging
import os

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-rabbit-monitor: %(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))

RABBITMQ_DEFAULT_PASS = os.getenv('RABBITMQ_DEFAULT_PASS', default='rabbit')
RABBITMQ_DEFAULT_USER = os.getenv('RABBITMQ_DEFAULT_USER', default='rabbit')
RABBITMQ_DEFAULT_VHOST = os.getenv('RABBITMQ_DEFAULT_VHOST', default='%2f')

RABBIT_URL = 'http://{hostname}:{port}/api/'.format(
    hostname=os.getenv('RABBITMQ_HOST', 'rabbit'),
    port=os.getenv('RABBIT_MGT_PORT', 15672)
)

WAIT_TIME = os.getenv('RABBIT_MONITOR_WAIT_TIME', 10)

# Number of seconds to look back and gather stats from
RABBIT_MONITOR_STATS_WINDOW = os.getenv('RABBIT_MONITOR_STATS_WINDOW',
                                        WAIT_TIME)

# Sample frequency in stats window
RABBIT_MONITOR_STATS_INCREMENT = os.getenv('RABBIT_MONITOR_STATS_INCREMENT',
                                           str(RABBIT_MONITOR_STATS_WINDOW / 10),
                                           )
