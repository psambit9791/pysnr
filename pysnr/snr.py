import scipy as sp
import numpy as np


def _check_type_and_shape(data):
    if isinstance(data, np.ndarray):
        if len(data.shape) != 1:
            return False, None
        return True, data
    elif isinstance(data, list):
        data = np.array(data)
        if len(data.shape) != 1:
            return False, None
        return True, data
    else:
        return False, None


def _rssq(data):
    return np.sqrt(np.sum(data ** 2))


def mag2db(data):
    return 20 * np.log10(data)


def snr(signal, noise):
    signalCheck, signal = _check_type_and_shape(signal)
    noiseCheck, noise = _check_type_and_shape(noise)
    if signalCheck == False or noiseCheck == False:
        raise AttributeError("Signal and Noise must be 1D arrays")

    return mag2db(_rssq(signal) / _rssq(noise))