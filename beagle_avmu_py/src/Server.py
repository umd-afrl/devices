import asyncio
import json
import logging
import os
from queue import Empty
from multiprocessing import Queue

import aiohttp_cors
from aiohttp import web

from NumpyComplexArrayEncoder import NumpyComplexArrayEncoder

WEB_ROOT = '/home/debian/ui/controlpanel/'
SERVER = web.Application()
in_queue = Queue()

cors = aiohttp_cors.setup(SERVER)


async def root_handler(request):
    return web.FileResponse(os.path.join(WEB_ROOT, 'index.html'))


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    await writer(ws)
    async for msg in ws:
        pass
    return ws


async def writer(ws):
    try:
        print('opened')
        while True:
            try:
                global in_queue
                data = in_queue.get_nowait()
                json.dumps(data, cls=NumpyComplexArrayEncoder)
                await ws.send_str(data)
                await asyncio.sleep(0.01)
            except Empty:
                pass
    except Exception as error:
        print('closed:', error)


async def on_shutdown(app):
    # close peer connections
    for socket in set(app['websockets']):
        await socket.close()


async def start(queue: Queue, ip='192.168.1.7', port=8080):
    global SERVER, runner, site, QUEUE
    SERVER.on_shutdown.append(on_shutdown)
    SERVER.router.add_get('/', root_handler)
    SERVER.router.add_get('/ws', websocket_handler)
    SERVER.router.add_static(prefix='/', path=WEB_ROOT)
    QUEUE = queue
    logging.basicConfig(level=logging.DEBUG)
    runner = web.AppRunner(SERVER)
    await runner.setup()
    site = web.TCPSite(runner, ip, port)
    await site.start()
    print('Site available at http://' + site.__getattribute__('_host') + ':' + str(site.__getattribute__('_port')))


async def end():
    await SERVER.shutdown()


if __name__ == '__main__':
    asyncio.ensure_future(start(Queue(), ip='192.168.1.7', port=8080))
    loop = asyncio.get_event_loop()
    loop.run_forever()
