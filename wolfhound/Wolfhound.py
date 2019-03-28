import time
from WebsocketServer import WebsocketServer
from WolfhoundParser import WolfhoundParser
from threading import Thread

server = WebsocketServer
serverThread = Thread(target=server.start_server)
serverThread.start()

parser = WolfhoundParser

strengthList = []

while True:
    for byte in parser.data:
        parser.parseByte(byte)
        print(parser.recordData)
        if parser.recordLength == 7:
            print("Signal Strength: ")
            print(parser.recordData[4])
            strengthData = parser.recordData[4]
            server.set_wolfhound_data(strengthData)
            strengthList.append(parser.recordData[4])
        time.sleep(0.5)



