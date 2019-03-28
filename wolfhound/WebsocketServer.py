import websockets
import asyncio


class WebsocketServer:

    signal_strength = 0

    async def handler(self, websocket, path):
        while True:
            await websocket.send(self.get_wolfhound_data())
            await asyncio.sleep(0.5)

    def get_wolfhound_data(self):
        return "{'signal_strength':" + str(self.signal_strength) + "}"

    def set_wolfhound_data(self, new_signal_strength):
        self.signal_strength = new_signal_strength

    def start_server(self):
        start_server = websockets.serve(self.handler, '127.0.0.1', 80)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
