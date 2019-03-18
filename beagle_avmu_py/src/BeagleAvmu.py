import time
from multiprocessing import Process, Queue

import AvmuCapture


def avmu(queue):
    with AvmuCapture.initialize() as device:
        time.sleep(.1)
        print(AvmuCapture.capture(device))


def dsp(queue):


def ws(queue):


if __name__ == '__main__':
    avmu_queue = Queue()
    dsp_queue = Queue()
    ws_queue = Queue()

    avmu_process = Process(target=avmu, args=avmu_queue)
    avmu_process.start()

    dsp_process = Process(target=dsp, args=dsp_queue)
    dsp_process.start()

    ws_process = Process(target=ws, args=ws_queue)
    ws_process.start()
