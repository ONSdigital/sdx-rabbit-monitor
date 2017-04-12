import asyncio

from aiohttp import web

from rabbit_monitor import init

loop = asyncio.get_event_loop_policy().get_event_loop()
app = web.Application(loop=loop)
app = init(app)
