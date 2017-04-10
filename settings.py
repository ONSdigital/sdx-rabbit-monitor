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

WAIT_TIME = os.getenv('RABBIT_MONITOR_WAIT_TIME', 300)
