#!/usr/bin/env python
#   coding: UTF-8
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


class RabbitMonitor():

    RABBIT_URL = settings.RABBIT_URL
    RABBITMQ_DEFAULT_USER = settings.RABBITMQ_DEFAULT_USER
    RABBITMQ_DEFAULT_PASS = settings.RABBITMQ_DEFAULT_PASS
    WAIT_TIME = settings.WAIT_TIME

    def __init__(self):
        logger.info("Creating RabbitMonitor object")
        self.session = requests.Session()
        self.session.auth = (settings.RABBITMQ_DEFAULT_USER,
                             settings.RABBITMQ_DEFAULT_PASS)

    def start(self):
        logger.info("Starting sdx-rabbit-monitor", version=__version__)

        try:
            while True:
                self.call_healthcheck()
                self.call_aliveness()
                sleep(self.WAIT_TIME)
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
        healthcheck = self.session.get(settings.URLS['healthcheck'],
                                       hooks=dict(response=self.process_healthcheck))

    def process_healthcheck(self, r, *args, **kwargs):
        if r.status_code == 200:
            logger.info('Rabbit health ok', status=r.status_code)
        else:
            logger.error('Rabbit health bad', status=r.status_code)

    def call_aliveness(self):
        logger.info('Getting rabbit aliveness status')
        aliveness = self.session.get(settings.URLS['aliveness'],
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
