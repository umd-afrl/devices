import asyncio
import os
from multiprocessing import Queue

import aiohttp_cors
from aiohttp import web

from NumpyComplexArrayEncoder import NumpyComplexArrayEncoder

WEB_ROOT = '/home/debian/ui/controlpanel/'
SERVER = web.Application()
QUEUE = Queue()

cors = aiohttp_cors.setup(SERVER)

resource = cors.add(SERVER.router.add_resource("/hello"))


async def root_handler(request):
    return web.FileResponse(os.path.join(WEB_ROOT, 'index.html'))


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await asyncio.create_task(writer(ws))
    async for msg in ws:
        pass
    return ws


async def writer(ws):
    try:
        print('opened')
        while True:
            await ws.send_json(QUEUE.get_nowait(), dumps=NumpyComplexArrayEncoder)
            await asyncio.sleep(0.01)
    except Exception as error:
        print('closed:', type(error))


async def on_shutdown(app):
    # close peer connections
    for socket in set(app['websockets']):
        await socket.close()


async def start(queue: Queue, ip='192,168,1,7', port=80):
    global runner, site, QUEUE
    QUEUE = queue
    runner = web.AppRunner(SERVER)
    await runner.setup()
    site = web.TCPSite(runner, ip, port)
    await site.start()
    print('Site available at http://' + site.__getattribute__('_host') + ':' + str(site.__getattribute__('_port')))


async def end():
    await SERVER.shutdown()
