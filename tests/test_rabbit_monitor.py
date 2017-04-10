import asyncio

import aiohttp
from aiohttp import web
import pytest

from rabbit_monitor import fetch, self_healthcheck, message_count


@pytest.fixture
def cli(loop, test_client):
    app = web.Application()
    app.router.add_get('/healthcheck', self_healthcheck)
    app.router.add_get('/rabbit_aliveness_good', rabbit_fetch_good)
    app.router.add_get('/test_message_count', message_count)
    return loop.run_until_complete(test_client(app))


@pytest.yield_fixture
def loop():
    # Set-up
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop

    # Clean-up
    loop.close()


def rabbit_aliveness_good(request):
    return web.json_response({'status': 'ok'})


def mock_message_count(request):
    return web.json_response({'queue_totals': {'messages': 10}})


@asyncio.coroutine
def test_message_count(cli):
    port = cli.server.port
    url = 'http://localhost:{}/test_message_count'.format(port)
    session = aiohttp.ClientSession()
    resp = message_count(session, url)
    assert resp.status == 200


@asyncio.coroutine
def test_self_healthcheck(cli):
    resp = yield from cli.get('/healthcheck')
    assert resp.status == 200
    text = yield from resp.text()
    assert text == '{"status": "ok"}'


@asyncio.coroutine
def rabbit_fetch_good(cli):
    port = cli.server.port
    url = 'http://localhost:{}/rabbit_aliveness_good'.format(port)
    session = aiohttp.ClientSession()
    resp = yield from fetch(session=session, url=url)
    assert resp.status == 200
    text = yield from resp.text()
    assert text == '{"status": "ok"}'


@asyncio.coroutine
def test_fetch_bad(cli):
    port = cli.server.port
    url = 'http://localhost:{}/rabbit_aliveness_bad'.format(port)
    session = aiohttp.ClientSession()
    resp = yield from fetch(session=session, url=url)
    assert resp.status != 200
