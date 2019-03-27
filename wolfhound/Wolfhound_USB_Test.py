from pyftdi.ftdi import Ftdi
import time
import websockets

WolfHound = Ftdi()

def usb_test():

    objects = []
    objects = Ftdi.find_all([(0x09D6, 0x1000)])

    print(objects)


usb_test()

serialNumber = ""
stopBits = 0


def Open(self):
    deviceInfoList = Ftdi.find_all()
    self.setBaudRate()

    return False


def setBaudRate(self):
    return Ftdi.set_baudrate(Ftdi(), 57600)


WolfHound.add_custom_vendor(0x09D6)
WolfHound.add_custom_product(0x09D6, 0x1000)

WolfHound.open_from_url("ftdi://2518:4096/1")

WolfHound.set_baudrate(57600)


WolfHound.write_data([17, 18, 3, 0, 0, 17, 19])


WolfHound.write_data([17, 18, 3, 0, 0, 17, 19])

data = list(WolfHound.read_data(8192))


recordState = 1
recordID = None
recordData = []
recordLength = 0


def reset():
   global recordState
   global recordLength
   global recordData
   recordState = 1
   recordLength = 0
   recordData = []


def checksum():
   global recordLength
   global recordID
   rec = recordID
   for i in range(recordLength):
       rec ^= recordData[i]


def recordComplete():
   global recordState
   return recordState == 7


def parseByte(data):
   global recordData
   global recordState
   global recordID
   global recordLength

   if recordState == 1:
       if data == 17:
           recordState = 2
   elif recordState == 2:
       if data != 18:
           recordState = 1
       else:
           recordState = 3
   elif recordState == 3:
       recordID = data
       if recordID != 17:
           recordState = 5
       else:
           recordState = 4
   elif recordState == 4:
       if data != 20:
           recordState = 1
       else:
           recordState = 5
   elif recordState == 5:
       if data == 17:
           recordState = 6
       else:
           recordData.append(data)
           recordLength += 1
           if len(recordData) == 8192:
               recordState = 1
   elif recordState == 6:
       if data == 19:
           recordState = 7
           print("Complete Record!")
           if checksum() != 0:
               recordState = 1
           print("Valid Record")
           print(recordLength)
       elif recordState == 20:
           recordState = 5
           recordLength += 1
           recordData.append(17)
       else:
           recordState = 1
   if recordState == 1:
       reset()
   return 0

WolfHound.write_data([17, 18, 4, 17, 19, 17, 19])

strengthList = []

while True:
    for byte in data:
        parseByte(byte)
        print(recordData)
        if recordLength == 7:
            print("Signal Strength: ")
            print(recordData[4])
            strengthData = recordData[4]
            strengthList.append(recordData[4])
        time.sleep(0.5)



