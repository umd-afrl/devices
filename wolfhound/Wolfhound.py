from WebsocketServer import WebsocketServer
from WolfhoundParser import WolfhoundParser
from threading import Thread

server = WebsocketServer()
serverThread = Thread(target=server.start_server)
serverThread.start()

parser = WolfhoundParser()

strengthList = []

while True:
    wolfData = list(parser.WolfHound.read_data(8192))

    for byte in wolfData:
        parser.parseByte(byte)

        if parser.recordLength == 7:
            test1 = '{0:08b}'.format(parser.recordData[2])
            test2 = '{0:02b}'.format(parser.recordData[3])
            test3 = test2 + test1
            test3 = int(test3, 2)
            test4 = '{0:08b}'.format(parser.recordData[4])
            test5 = '{0:02b}'.format(parser.recordData[5])
            test6 = test5 + test4
            test6 = int(test6, 2)
            test6 = test6 / 10
            server.set_wolfhound_data(test3, test6)
