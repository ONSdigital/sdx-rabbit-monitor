import json
import logging
import os

LOGGING_FORMAT = "%(asctime)s|%(levelname)s: sdx-rabbit-monitor: %(message)s"
LOGGING_LEVEL = logging.getLevelName(os.getenv('LOGGING_LEVEL', 'DEBUG'))

if os.getenv("CF_DEPLOYMENT", False):
    vcap_services = os.getenv("VCAP_SERVICES")
    parsed_vcap_services = json.loads(vcap_services)
    rabbit_config = parsed_vcap_services.get('rabbitmq')
    credentials = rabbit_config[0].get('credentials')
    PORT = credentials.get('port')
    RABBITMQ_DEFAULT_PASS = credentials.get('default_password')
    RABBITMQ_DEFAULT_USER = credentials.get('default_user')
    RABBITMQ_DEFAULT_VHOST = credentials.get('vhost')
    SDX_RABBIT_MONITOR_RABBIT_HOST = credentials.get('host')
    SDX_RABBIT_MONITOR_MGT_PORT = credentials.get('management_port')
    RABBIT_URL = 'http://{hostname}:{port}/api/'.format(
        hostname=SDX_RABBIT_MONITOR_RABBIT_HOST,
        port=SDX_RABBIT_MONITOR_MGT_PORT)


else:
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
