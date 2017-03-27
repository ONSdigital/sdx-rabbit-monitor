#!/usr/bin/env python
#   coding: UTF-8
from collections import namedtuple
import logging
import sys
from time import sleep

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from structlog import wrap_logger

import settings

__version__ = "0.0.1"

logging.basicConfig(level=settings.LOGGING_LEVEL,
                    format=settings.LOGGING_FORMAT)
logger = wrap_logger(logging.getLogger(__name__))

Settings = namedtuple('Settings',
                      [
                          'rabbit_url',
                          'rabbit_default_user',
                          'rabbit_default_pass',
                          'wait_time',
                      ])


class RabbitMonitor():

    def __init__(self):
        logger.info("Creating RabbitMonitor object")

        self.settings = Settings(wait_time=settings.WAIT_TIME,
                                 rabbit_url=settings.RABBIT_URL,
                                 rabbit_default_user=settings.RABBITMQ_DEFAULT_USER,
                                 rabbit_default_pass=settings.RABBITMQ_DEFAULT_PASS)

        healthcheck_url = self.settings.rabbit_url + 'healthchecks/node'
        aliveness_url = (self.settings.rabbit_url +
                         'aliveness-test/{}'.format(settings.RABBITMQ_DEFAULT_VHOST))

        self.urls = {'healthcheck': healthcheck_url,
                     'aliveness': aliveness_url}

        self.session = requests.Session()
        self.session.auth = (self.settings.rabbit_default_user,
                             self.settings.rabbit_default_pass)

    def call_healthcheck(self):
        logger.info('Getting rabbit healthcheck status')
        healthcheck = self.session.get(self.urls['healthcheck'],
                                       hooks=dict(response=self.process_healthcheck))

    def process_healthcheck(self, r, *args, **kwargs):
        if r.status_code == 200:
            logger.info('Rabbit health ok', status=r.status_code)
        else:
            logger.error('Rabbit health bad', status=r.status_code)

    def call_aliveness(self):
        logger.info('Getting rabbit aliveness status')
        aliveness = self.session.get(self.urls['aliveness'],
                                     hooks=dict(response=self.process_aliveness))

    def process_aliveness(self, r, *args, **kwargs):
        if r.status_code == 200:
            logger.info('Rabbit aliveness ok', status=r.status_code)
        else:
            logger.error('Rabbit aliveness bad', status=r.status_code)

    def shutdown(self):
        logger.info("Shutting down")
        sys.exit()

    def run(self):
        logger.info("Starting rabbit monitor", version=__version__)

        retries = Retry(total=5, backoff_factor=0.1)
        self.session.mount('http://', HTTPAdapter(max_retries=retries))

        while True:
            self.call_healthcheck()
            self.call_aliveness()
            sleep(self.WAIT_TIME)


if __name__ == "__main__":
    try:
        logger.info("Starting rabbit monitor", version=__version__)
        rabbit_monitor = RabbitMonitor()
        rabbit_monitor.run()
    except KeyboardInterrupt:
        rabbit_monitor.shutdown()
