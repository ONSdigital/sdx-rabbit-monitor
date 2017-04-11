#!/usr/bin/env python
#   coding: UTF-8
import asyncio
from collections import namedtuple
import json
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
                          'stats_window',
                          'stats_incr',
                      ])

settings = Settings(port=os.getenv("PORT", 5000),
                    wait_time=settings.WAIT_TIME,
                    rabbit_url=settings.RABBIT_URL,
                    rabbit_default_user=settings.RABBITMQ_DEFAULT_USER,
                    rabbit_default_pass=settings.RABBITMQ_DEFAULT_PASS,
                    rabbit_default_vhost=settings.RABBITMQ_DEFAULT_VHOST,
                    stats_window=settings.RABBIT_MONITOR_STATS_WINDOW,
                    stats_incr=settings.RABBIT_MONITOR_STATS_INCREMENT,)

healthcheck_url = settings.rabbit_url + 'healthchecks/node'
aliveness_url = (settings.rabbit_url +
                 'aliveness-test/{}'.format(settings.rabbit_default_vhost))
message_url = (settings.rabbit_url +
               'overview/')

urls = {'healthcheck': healthcheck_url,
        'aliveness': aliveness_url,
        'messages': message_url,
        }

params = {'lengths_age': settings.stats_window,
          'lengths_incr': settings.stats_incr,
          }


@asyncio.coroutine
def fetch(session, url):
    with aiohttp.Timeout(5):
        resp = None
        try:
            return (yield from session.get(url,
                                           params=params))
        except Exception as e:
            logger.error(e, status='bad')
            if resp is not None:
                yield from resp.close()
        finally:
            if resp is not None:
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
def message_count(session, url=None):
    logger.info('Getting message counts')
    if url is None:
        resp = yield from fetch(session, urls['messages'])
    else:
        resp = yield from fetch(session, url)

    if resp.status == 200:
        text = yield from resp.text()
        text = json.loads(text)

        queue_totals = text.get('queue_totals')
        logger.info('Rabbit messages',
                    status=resp.status,
                    count=queue_totals.get('messages'),
                    rate=queue_totals.get('messages_details', {}).get('rate'),
                    ready=queue_totals.get('messages_ready'),
                    unackd=queue_totals.get('messages_unacknowledged'))
    return resp


@asyncio.coroutine
def monitor_rabbit(app):
    auth = aiohttp.BasicAuth(settings.rabbit_default_pass,
                             settings.rabbit_default_user)

    try:
        session = aiohttp.ClientSession(loop=app.loop,
                                        auth=auth)
        while True:
            tasks = [
                aliveness(session),
                healthcheck(session),
                message_count(session),
            ]
            tasks = asyncio.gather(*[task for task in tasks],
                                   return_exceptions=True)
            yield from asyncio.sleep(settings.wait_time)
    except asyncio.CancelledError:
        logger.info("Stopping rabbit monitoring")
    finally:
        yield from session.close()


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
