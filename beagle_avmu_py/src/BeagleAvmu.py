import asyncio
from multiprocessing import Process, Queue, Pipe
import queue
import time

import AvmuCapture
import OneDimDSP
import Server

def avmu(out_queue: Queue, frequencies: Pipe, toggle: Queue, scan: bool):
    with AvmuCapture.initialize(hop_rate='HOP_15K') as device:
        frequencies.send(AvmuCapture.get_frequencies(device))
        while True:
            try:
                if toggle.get_nowait() == "toggle":
                    scan = not scan
                    if scan:
                        AvmuCapture.begin_capture(device)
                    else:
                        AvmuCapture.end_capture(device)
            except queue.Empty:
                pass
            if scan:
                device.measure()
                out_queue.put_nowait(device.extractAllPaths()[0][1]['data'])

def dsp(in_queue: Queue, out_queue: Queue, frequencies: Pipe, process: bool):
    freq = frequencies.recv()
    axis, front_padding_count = OneDimDSP.get_axis_and_padding(freq, 8.134, 1024)
    range_data = None
    while process:
        previous_data = range_data
        data = in_queue.get(True)
        data = OneDimDSP.apply_window(data, 1024)
        range_data = OneDimDSP.pad_and_ifft(data, front_padding_count)
        change = OneDimDSP.coherent_change_detection(range_data, previous_data)
        peaks = OneDimDSP.detect_peaks(change[0], 100, 300, 1e-4)
        out_queue.put_nowait((change, peaks))


def ws(in_queue: Queue, toggle_queue: Queue):
    asyncio.ensure_future(Server.start(in_queue, toggle_queue))
    loop = asyncio.get_event_loop()
    loop.run_forever()


if __name__ == '__main__':
    (frequencies_in, frequencies_out) = Pipe(False)
    toggle_queue = Queue()
    raw_queue = Queue()
    processed_queue = Queue()

    avmu_process = Process(target=avmu, args=(raw_queue, frequencies_out, toggle_queue, True))
    avmu_process.start()

    dsp_process = Process(target=dsp, args=(raw_queue, processed_queue, frequencies_in, True))
    dsp_process.start()

    ws_process = Process(target=ws, args=(processed_queue, toggle_queue))
    ws_process.start()
