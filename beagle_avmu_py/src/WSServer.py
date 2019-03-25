import asyncio
import json
import logging
from multiprocessing import Queue

import websockets



logging.basicConfig()

queue = Queue()

clients = set()


def initialize(in_queue: Queue, ip: str, port: int):
    global queue
    queue = in_queue
    asyncio.get_event_loop().run_until_complete(websockets.serve(avmu, ip, port))
    asyncio.get_event_loop().run_forever()


def data_event():
    global queue
    return json.dumps(queue.get(block=True))


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
