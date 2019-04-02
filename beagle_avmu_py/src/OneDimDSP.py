import numpy as np
import scipy.signal.windows


def apply_window(sweep_data):
    return np.multiply(sweep_data, scipy.signal.windows.chebwin(len(sweep_data), 45))


def pad_data(sweep_data, front_padding_count):
    padded_data = []
    while len(padded_data) < front_padding_count:
        padded_data.append(0)
    padded_data.extend(sweep_data)

    powers_of_two = [2 ** x for x in range(8, 16)]

    final_size = powers_of_two[0]
    for size in powers_of_two:
        if size > len(padded_data):
            final_size = size
            break

    while len(padded_data) < final_size:
        padded_data.append(0)

    return np.array(padded_data)


def get_axis_and_padding(frequencies, cable_delays, num_points):
    step = abs(frequencies[0] - frequencies[-1]) / len(frequencies)
    front_padding_count = max(int(frequencies[0] / step), 0)
    freq_step = step * 1e6  # Step in MHz to Hz
    num_cells = 2 * num_points
    x_axis = np.transpose(np.array(range(0, num_cells))) * (1 / (num_cells * freq_step * 2))  # Hz to seconds
    x_axis = x_axis * 1e9  # Seconds to nanoseconds
    x_axis = x_axis - cable_delays
    x_axis = x_axis * 0.983571  # Nanoseconds to feet
    return x_axis, front_padding_count


def coherent_change_detection(data, previous):
    if previous is not None:
        diff_ccd = np.abs(data - previous)
        return np.reshape(diff_ccd, (1, 2048))
    else:
        return np.reshape(data, (1, 2048))


def detect_peaks(x, num_train, num_guard, rate_fa, axis):
    num_cells = x.size
    num_train_half = round(num_train / 2)
    num_guard_half = round(num_guard / 2)
    num_side = num_train_half + num_guard_half

    alpha = num_train * (rate_fa ** (-1 / num_train) - 1)  # threshold factor

    peak_idx = []
    for i in range(num_side, num_cells - num_side):

        if i != i - num_side + np.argmax(x[i - num_side:i + num_side + 1]):
            continue

        sum1 = np.sum(x[i - num_side:i + num_side + 1])
        sum2 = np.sum(x[i - num_guard_half:i + num_guard_half + 1])
        p_noise = (sum1 - sum2) / num_train
        threshold = alpha * p_noise

        if x[i] > threshold:
            peak_idx.append((i, .5))

    peak_idx = np.array(peak_idx, dtype=float)

    return peak_idx
