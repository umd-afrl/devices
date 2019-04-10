import asyncio
import json
import logging
import os
from multiprocessing import Queue, Pipe
import queue

import aiohttp_cors
from aiohttp import web

from NumpyComplexArrayEncoder import NumpyComplexArrayEncoder

WEB_ROOT = '/home/debian/ui/controlpanel/'
SERVER = web.Application()
in_queue = Queue()
toggle_queue = Queue()

cors = aiohttp_cors.setup(SERVER)


async def root_handler(request):
    return web.FileResponse(os.path.join(WEB_ROOT, 'index.html'))

async def websocket_handler(request):
    ws = web.WebSocketResponse(autoclose=False, compress=False)
    await ws.prepare(request)

    print('Adding client')
    request.app['websockets'].add(ws)

    await send_data(request.app)

    return ws


async def send_data(app):
    while True:
       # print(len(app['websockets']))
        try:
            data = in_queue.get_nowait()
        #print(data)
            for client in app['websockets']:
                await client.send_str(json.dumps(data, cls=NumpyComplexArrayEncoder))
                await asyncio.sleep(0)
        except queue.Empty:
            pass
       # print('all done')
        await asyncio.sleep(0)


async def writer(send_queue, socket):
    while True:
        data = await send_queue.get()
        json.dumps(data, cls=NumpyComplexArrayEncoder)
        await socket.send_str(data)


async def toggle_handler(request):
    toggle_queue.put_nowait("toggle")
    return web.Response()


async def on_startup(app):
    #loop = asyncio.get_event_loop()
    #app['queue_listener'] = loop.create_task(send_data(app))
    app['websockets'] = set()


async def on_shutdown(app):
    # close peer connections
    for socket in set(app['websockets']):
        await socket.close()


async def start(queue: Queue, toggle: Queue, ip='192.168.1.7', port=8080):
    global SERVER, runner, site, in_queue, toggle_queue
    SERVER.on_startup.append(on_startup)
    SERVER.on_shutdown.append(on_shutdown)
    SERVER.router.add_get('/', root_handler)
    SERVER.router.add_get('/ws', websocket_handler)
    SERVER.router.add_post('/toggleavmu', toggle_handler)
    SERVER.router.add_static(prefix='/', path=WEB_ROOT)
    in_queue = queue
    toggle_queue = toggle
    logging.basicConfig(level=logging.DEBUG)
    runner = web.AppRunner(SERVER)
    await runner.setup()
    site = web.TCPSite(runner, ip, port)
    await site.start()
    print('Site available at http://' + site.__getattribute__('_host') + ':' + str(site.__getattribute__('_port')))


async def end():
    await SERVER.shutdown()


if __name__ == '__main__':
    asyncio.ensure_future(start(Queue(), Queue(), ip='localhost', port=8080))
    loop = asyncio.get_event_loop()

    for i in range(1000):
        in_queue.put_nowait(i)
    loop.run_forever()
