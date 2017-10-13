import asyncio
import json

import aiohttp
from aiohttp import web
import pytest
import os
import unittest

os.environ['RABBIT_MONITOR_WAIT_TIME'] = '300'
os.environ['RABBIT_MONITOR_STATS_WINDOW'] = '300'
os.environ['RABBIT_MONITOR_STATS_INCREMENT'] = '30'
os.environ['SDX_RABBIT_MONITOR_PASS'] = 'secret'
os.environ['SDX_RABBIT_MONITOR_USER'] = 'rabbit'
os.environ['SDX_RABBIT_MONITOR_DEFAULT_VHOST'] = '%2f'
os.environ['SDX_RABBIT_MONITOR_RABBIT_HOST'] = '0.0.0.0'
os.environ['SDX_RABBIT_MONITOR_MGT_PORT'] = '15672'
os.environ['SDX_RABBIT_MONITOR_WAIT_TIME'] = '30'
os.environ['SDX_RABBIT_MONITOR_STATS_WINDOW'] = '5'
os.environ['SDX_RABBIT_MONITOR_STATS_INCREMENT'] = '5'
os.environ['PORT'] = '5000'

from rabbit_monitor import fetch, self_healthcheck, message_count, nodes_info
from rabbit_monitor import check_globals


@pytest.fixture
def cli(loop, test_client):
    app = web.Application()
    app.router.add_get('/healthcheck', self_healthcheck)
    app.router.add_get('/rabbit_aliveness_good', rabbit_fetch_good)
    app.router.add_get('/test_message_count', mock_message_count)
    app.router.add_get('/test_nodes', mock_nodes)
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


@asyncio.coroutine
def mock_message_count(request):
    return web.json_response({'queue_totals': {
                              'messages': 10,
                              'messages_ready': 1,
                              'messages_unacknowledged': 1,
                              'messages_details': {
                                  'rate': 0.0,
                              }}},
                             status=200)


@asyncio.coroutine
def test_message_counts(cli):
    port = cli.server.port
    url = 'http://localhost:{}/test_message_count'.format(port)
    session = aiohttp.ClientSession()
    resp = yield from message_count(session, url)
    assert resp.status == 200
    text = yield from resp.text()
    text = json.loads(text)
    queue_totals = text.get('queue_totals')
    assert 10 == queue_totals.get('messages')
    assert 0.0 == queue_totals.get('messages_details', {}).get('rate')
    assert 1 == queue_totals.get('messages_ready')
    assert 1 == queue_totals.get('messages_unacknowledged')


@asyncio.coroutine
def mock_nodes(request):
    return web.json_response([{"name": "rabbit@76b7837eff57",
                               "mem_limit": 838474137,
                               "disk_free_limit": 50000000,
                               "mem_used": 77209008,
                               "disk_free": 58268864512}],
                             status=200)


@asyncio.coroutine
def test_node_info(cli):
    port = cli.server.port
    url = 'http://localhost:{}/test_nodes'.format(port)
    session = aiohttp.ClientSession()
    name, free_disk_space, free_disk_space_limit, percent_disk, memory_used, memory_used_limit, percent_mem = yield from nodes_info(session, url)
    assert "rabbit@76b7837eff57" == name
    assert 58268864512 == free_disk_space
    assert 77209008 == memory_used
    assert 50000000 == free_disk_space_limit
    assert 838474137 == memory_used_limit
    assert '99.91%' == percent_disk
    assert '90.79%' == percent_mem


@asyncio.coroutine
def test_self_healthcheck(cli):
    resp = yield from cli.get('/healthcheck')
    assert resp.status == 200
    text = yield from resp.text()
    assert text == '{"status": "ok"}'


@asyncio.coroutine
def rabbit_fetch_good(cli):
    port = int(cli.server.port)
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


class CheckGlobals(unittest.TestCase):

    def test_check_globals_negative(self):
        class MockModule:

            SDX_VAR1 = "some/value"
            SDX_VAR2 = None

        self.assertFalse(check_globals(MockModule))

    def test_check_globals_positive(self):
        class MockModule:

            SDX_VAR1 = "some/value"
            SDX_VAR2 = 8080

        self.assertTrue(check_globals(MockModule))
