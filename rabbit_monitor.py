#!/usr/bin/env python
#   coding: UTF-8
import asyncio
from collections import namedtuple
import logging
import os

import aiohttp
from aiohttp import web
from structlog import wrap_logger

import settings

__version__ = "0.0.1"

logging.basicConfig(level=settings.LOGGING_LEVEL,
                    format=settings.LOGGING_FORMAT)
logger = wrap_logger(logging.getLogger(__name__))

Settings = namedtuple('Settings',
                      [
                          'port',
                          'rabbit_url',
                          'rabbit_default_user',
                          'rabbit_default_pass',
                          'rabbit_default_vhost',
                          'wait_time',
                      ])

logger.info("Creating RabbitMonitor object")

settings = Settings(port=os.getenv("PORT", 5000),
                    wait_time=settings.WAIT_TIME,
                    rabbit_url=settings.RABBIT_URL,
                    rabbit_default_user=settings.RABBITMQ_DEFAULT_USER,
                    rabbit_default_pass=settings.RABBITMQ_DEFAULT_PASS,
                    rabbit_default_vhost=settings.RABBITMQ_DEFAULT_VHOST)

healthcheck_url = settings.rabbit_url + 'healthchecks/node'
aliveness_url = (settings.rabbit_url +
                 'aliveness-test/{}'.format(settings.rabbit_default_vhost))

urls = {'healthcheck': healthcheck_url,
        'aliveness': aliveness_url}

"""
def shutdown():
    logger.info("Shutting down sdx-rabbit-monitor")
    sys.exit()

"""


@asyncio.coroutine
def fetch(session, url):
    with aiohttp.Timeout(5):
        resp = yield from session.get(url)
        try:
            return resp
        except Exception as e:
            # .close() on exception.
            resp.close()
            raise e
        finally:
            # .release() otherwise to return connection into free connection pool.
            # It's ok to release closed response:
            # https://github.com/KeepSafe/aiohttp/blob/master/aiohttp/client_reqrep.py#L664
            yield from resp.release()


@asyncio.coroutine
def aliveness(session):
    logger.info('Getting rabbit aliveness status')
    resp = yield from fetch(session, urls['aliveness'])
    if resp.status == 200:
        logger.info('Rabbit aliveness ok', status=resp.status)
    else:
        logger.error('Rabbit aliveness bad', status=resp.status)
    return resp


@asyncio.coroutine
def healthcheck(session):
    logger.info('Getting rabbit healthcheck status')
    resp = yield from fetch(session, urls['healthcheck'])
    if resp.status == 200:
        logger.info('Rabbit healthcheck ok', status=resp.status)
    else:
        logger.error('Rabbit healthcheck bad', status=resp.status)
    return resp


@asyncio.coroutine
def monitor_rabbit(app):
    auth = aiohttp.BasicAuth(settings.rabbit_default_pass,
                             settings.rabbit_default_user)

    try:
        session = aiohttp.ClientSession(loop=app.loop,
                                        auth=auth)
        while True:
            yield from aliveness(session)
            yield from healthcheck(session)
            yield from asyncio.sleep(settings.wait_time)
    except asyncio.CancelledError:
        logger.info("Stopping rabbit monitoring")


@asyncio.coroutine
def start_background_tasks(app):
    app['rabbit_poller'] = app.loop.create_task(monitor_rabbit(app))


@asyncio.coroutine
def cleanup_background_tasks(app):
    app['rabbit_poller'].cancel()
    yield from app['rabbit_poller']


@asyncio.coroutine
def self_healthcheck(request):
    logger.info('sdx-rabbit-monitor self healthcheck', status=200)
    return web.json_response({'status': 'ok'})


def init(app):
    logger.info("Starting sdx-rabbit-monitor", version=__version__)
    app.router.add_get('/healthcheck', self_healthcheck)
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)
    return app


app = web.Application(loop=None)
app = init(app)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    web.run_app(app, port=int(settings.port), loop=loop)
