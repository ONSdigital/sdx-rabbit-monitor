#!/usr/bin/env python
#   coding: UTF-8
from collections import namedtuple
from json import dumps
import logging
from multiprocessing import Process
import os
import sys
from time import sleep

from bottle import Bottle, response, run
import requests
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

    def start(self):
        logger.info("Starting sdx-rabbit-monitor", version=__version__)

        try:
            while True:
                self.call_healthcheck()
                self.call_aliveness()
                sleep(self.settings.wait_time)
        except KeyboardInterrupt:
            self.shutdown()

    def shutdown(self, signal=None, frame=None):
        logger.info("Shutting down sdx-rabbit-monitor")
        try:
            self._p.shutdown()
        except AttributeError:
            # Process not started
            pass

        sys.exit()

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


app = Bottle()


@app.route('/healthcheck')
def healthcheck():
    logger.info('sdx-rabbit-monitor self healthcheck', status=200)
    response.content_type = 'application/json'
    return dumps({'status': 'ok'})


def main():
    port = int(os.getenv("port", 5000))
    p = Process(target=run, args=(app,), kwargs={'port': port})
    p.start()
    try:
        rm = RabbitMonitor()
        rm.start()
    except KeyboardInterrupt:
        p.terminate()
        p.join()
        rm.shutdown()


if __name__ == "__main__":
    main()
