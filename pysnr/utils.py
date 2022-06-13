import numpy as np
import scipy.signal
from matplotlib import mlab as mlab
import math

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


def _find_range(psd, harmonic_idx, max_length):
    left = max(0, harmonic_idx - 1)
    right = min(harmonic_idx + 1, max_length - 1)

    while left > 0 and psd[left] <= psd[left + 1]:
        left -= 1
    while right < len(psd) - 1 and psd[right - 1] >= psd[right]:
        right += 1

    left += 1
    right -= 1
    return left, right


def periodogram(data, Fs, window, method="welch", scaling="density"):
    f, pxx = None, None
    nfft = 2 ** math.ceil(math.log(len(data)) / math.log(2))
    if method == "welch":
        f, pxx = scipy.signal.periodogram(data, Fs, window, nfft=nfft, scaling=scaling, detrend=False)
    if method == "fft":
        w = scipy.signal.get_window(window, nfft)
        if scaling == "density":
            pxx, f = mlab.psd(data, NFFT=nfft, Fs=Fs, window=w)
        else:
            pxx, f = mlab.psd(data, NFFT=nfft, Fs=Fs, window=w, scale_by_freq=False)
    return f, pxx


def alias_to_nyquist(f, fs):
    tone = f % fs
    if tone > fs/2:
        return fs - tone
    else:
        return tone


def rssq(data):
    return np.sqrt(np.sum(data ** 2))


def mag2db(data, mag=10):
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