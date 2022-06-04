import numpy as np
import scipy.signal

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


def _mag2db(data, mag=20):
    return mag * np.log10(data, where=(data != 0))


def _find_range(f, harmonic_idx):
    upper = None
    lower = None
    for i in range(harmonic_idx + 1, len(f)-1):
        if f[i+1] >= f[i]:
            upper = i
            break
    for i in range(harmonic_idx-1, 1, -1):
        if f[i-1] <= f[i]:
            lower = i+1
            break
    return lower, upper


def snr_signal_noise(signal, noise):
    signalCheck, signal = _check_type_and_shape(signal)
    noiseCheck, noise = _check_type_and_shape(noise)
    if not signalCheck or not noiseCheck:
        raise TypeError("Signal and Noise must be 1-D arrays")
    return _mag2db(_rssq(signal) / _rssq(noise))


def snr_signal_only(signal, fs=1.0, n=6):
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    f, pxx = scipy.signal.periodogram(signal, fs, window=('kaiser', 38))
    pxxDB = _mag2db(pxx)
    _, DCup = _find_range(pxxDB, 0)
    f = f[DCup:]
    pxxDB = pxxDB[DCup:]
    first_harmonic = f[np.argmax(pxxDB)]

    freq_indices = []
    harmonics = []
    for i in range(1, n+1):
        h = first_harmonic*i
        harmonics.append(h)
        searchout = np.where(f == h)
        if len(searchout[0]) == 1:
            freq_indices.append(searchout)
    freq_indices = np.array(freq_indices).flatten()

    signal_power = np.empty(0)
    for harmonic_idx in freq_indices:
        low, up = _find_range(pxxDB, harmonic_idx)
        signal_power = np.hstack((signal_power, np.copy(pxxDB[low:up])))
        pxxDB[low:up] = 0.0

    pxxMed = np.median(pxxDB[pxxDB != 0])
    signal_power = np.array(signal_power).flatten()
    return 2*np.sum(signal_power/pxxMed)