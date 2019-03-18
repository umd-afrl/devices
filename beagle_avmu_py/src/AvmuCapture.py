from contextlib import contextmanager

import avmu


@contextmanager
def initialize():
    device = avmu.AvmuInterface()
    hop_rate = 'HOP_15K'
    points = 1024
    start_f = 250
    stop_f = 2100
    avmu_ip = '192.168.1.219'

    try:
        device.setIPAddress(avmu_ip)
        device.setIPPort(1027)
        device.setTimeout(500)
        device.setMeasurementType('PROG_SYNC')

        device.initialize()

        device.setHopRate(hop_rate)
        device.addPathToMeasure('AVMU_TX_PATH_0', 'AVMU_RX_PATH_1')

        device.utilGenerateLinearSweep(startF_mhz=start_f, stopF_mhz=stop_f, points=points)

        device.start()

        yield device

    finally:
        device.stop()


def capture(device):
    device.measure()
    return device.extractAllPaths()
