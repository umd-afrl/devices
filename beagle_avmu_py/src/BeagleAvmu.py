from multiprocessing import Process, Queue, Pipe

import AvmuCapture
import OneDimDSP
import WSServer


def avmu(out_queue: Queue, frequencies: Pipe, scan: bool):
    with AvmuCapture.initialize() as device:
        frequencies.send(AvmuCapture.get_frequencies(device))
        while scan:
            out_queue.put_nowait(device.capture())


def dsp(in_queue: Queue, out_queue: Queue, frequencies: Pipe, process: bool):
    freq = frequencies.recv()
    axis = OneDimDSP.get_axis(freq, 8.134, 1024)
    data = None
    while process:
        previous_data = data
        data = in_queue.get(True)
        data = OneDimDSP.apply_window(data)
        change = OneDimDSP.coherent_change_detection(data, previous_data)
        peaks = OneDimDSP.detect_peaks(data, 100, 300, 1e-4, axis)
        out_queue.put_nowait((change, peaks))


def ws(in_queue: Queue, ip='localhost', port=8008):
    WSServer.initialize(in_queue, ip, port)
    while True:
        WSServer.notify_data()


if __name__ == '__main__':
    (frequencies_in, frequencies_out) = Pipe(False)
    raw_queue = Queue()
    processed_queue = Queue()

    avmu_process = Process(target=avmu, args=(raw_queue, frequencies_out, True))
    avmu_process.start()

    dsp_process = Process(target=dsp, args=(raw_queue, processed_queue, frequencies_in, True))
    dsp_process.start()

    ws_process = Process(target=ws, args=(processed_queue,))
    ws_process.start()
