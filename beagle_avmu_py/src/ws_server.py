import asyncio
import json
import logging
from multiprocessing import Queue

import websockets

logging.basicConfig()

queue = Queue()

clients = set()


def data_event():
    return json.dump(queue.get())


async def notify_data():
    if clients:  # asyncio.wait doesn't accept an empty list
        message = data_event()
        await asyncio.wait([user.send(message) for user in clients])


async def register(websocket):
    clients.add(websocket)


async def unregister(websocket):
    clients.remove(websocket)


async def avmu(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        await websocket.send(data_event())
    finally:
        await unregister(websocket)


asyncio.get_event_loop().run_until_complete(websockets.serve(avmu, 'localhost', 8080))
asyncio.get_event_loop().run_forever()
