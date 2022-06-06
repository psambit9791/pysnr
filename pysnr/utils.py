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


def _find_range(psd, harmonic_idx):
    left = harmonic_idx - 1
    right = harmonic_idx + 1

    while left > 0 and psd[left] <= psd[left + 1]:
        left -= 1
    while right < len(psd) - 1 and psd[right - 1] >= psd[right]:
        right += 1

    left += 1
    right -= 1
    return left, right


def rssq(data):
    return np.sqrt(np.sum(data ** 2))


def mag2db(data, mag=20):
    return mag * np.log10(data, where=(data != 0))


def remove_dc_component(signal):
    return signal - np.mean(signal)


def enbw(window, Fs=None):
    bw = (np.sqrt(np.mean(window**2))/np.mean(window)) ** 2
    if Fs is not None:
        bw = bw * Fs/len(window)
    return bw


def bandpower(pxx, f):
    sxx = []
    widths = np.diff(f)
    missing_width = (f[-1] - f[0])/(len(f) - 1)
    if f[0] == 0:
        widths = np.hstack((missing_width, widths))
    else:
        widths = np.hstack((widths, missing_width))
    for p, w in zip(pxx, widths):
        sxx.append(p*w)
    return np.sum(np.array(sxx))