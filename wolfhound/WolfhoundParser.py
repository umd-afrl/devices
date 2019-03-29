from pyftdi.ftdi import Ftdi


class WolfhoundParser:
    WolfHound = Ftdi()

    WolfHound.add_custom_vendor(0x09D6)
    WolfHound.add_custom_product(0x09D6, 0x1000)

    WolfHound.open_from_url("ftdi://2518:4096/1")

    WolfHound.set_baudrate(57600)

    WolfHound.write_data([17, 18, 3, 0, 0, 17, 19])

    WolfHound.write_data([17, 18, 3, 0, 0, 17, 19])

    recordState = 1
    recordID = None
    recordData = []
    recordLength = 0

    def reset(self):
        self.recordState = 1
        self.recordLength = 0
        self.recordData = []

    def checksum(self):
        rec = self.recordID
        for i in range(self.recordLength):
            rec ^= self.recordData[i]

    def recordComplete(self):
        return self.recordState == 7

    def parseByte(self, data):
        if self.recordState == 1:
            if data == 17:
                self.recordState = 2
        elif self.recordState == 2:
            if data != 18:
                self.recordState = 1
            else:
                self.recordState = 3
        elif self.recordState == 3:
            self.recordID = data
            if self.recordID != 17:
                self.recordState = 5
            else:
                self.recordState = 4
        elif self.recordState == 4:
            if data != 20:
                self.recordState = 1
            else:
                self.recordState = 5
        elif self.recordState == 5:
            if data == 17:
                self.recordState = 6
            else:
                self.recordData.append(data)
                self.recordLength += 1
                if len(self.recordData) == 8192:
                    self.recordState = 1
        elif self.recordState == 6:
            if data == 19:
                self.recordState = 7
                print("Complete Record!")
                if self.checksum() != 0:
                    self.recordState = 1
                print("Valid Record")
                print(self.recordLength)
            elif self.recordState == 20:
                self.recordState = 5
                self.recordLength += 1
                self.recordData.append(17)
            else:
                self.recordState = 1
        if self.recordState == 1:
            self.reset()
        return 0

    while True:
        wolfData = list(WolfHound.read_data(8192))

        for byte in wolfData:
            parseByte(byte)

            if recordLength == 7:
                test1 = '{0:08b}'.format(recordData[2])
                test2 = '{0:02b}'.format(recordData[3])
                test3 = test2 + test1
                test3 = int(test3, 2)
                print("Frequency: ")
                print(test3)

                test4 = '{0:08b}'.format(recordData[4])
                test5 = '{0:02b}'.format(recordData[5])
                test6 = test5 + test4
                test6 = int(test6, 2)
                print("Signal Strength: ")
                test6 = test6 / 10
                print(test6)
