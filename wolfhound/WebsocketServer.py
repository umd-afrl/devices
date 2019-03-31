import websockets
import asyncio


class WebsocketServer:
    signal_strength = 0
    frequency = 0

    async def handler(self, websocket, path):
        while True:
            await websocket.send(self.get_wolfhound_data())
            await asyncio.sleep(0.5)

    def get_wolfhound_data(self):
        return '{"frequency":' + str(self.frequency) + ', "signal_strength":' + str(self.signal_strength) + "}"

    def set_wolfhound_data(self, new_freq, new_signal_strength):
        self.signal_strength = new_signal_strength
        self.frequency = new_freq

    def start_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.handler, port=8090)

        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
