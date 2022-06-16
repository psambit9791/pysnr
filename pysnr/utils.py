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


def _get_tone_indices_from_psd(pxx, frequencies, toneFreq):
    idxTone = None
    idxLeft = None
    idxRight = None

    if frequencies[0] <= toneFreq < frequencies[-1]:
        idxTone = np.argmin(np.abs(frequencies - toneFreq))
        iLeftBin = max(0, idxTone - 1)
        iRightBin = min(idxTone+1, len(frequencies))
        idxMax = np.argmax(pxx[iLeftBin: iRightBin+1])
        idxTone = iLeftBin + idxMax
        idxLeft = max(0, idxTone - 1)
        idxRight = min(idxTone + 1, len(pxx)-1)

        while (idxLeft > -1) and (pxx[idxLeft-1] <= pxx[idxLeft]):
            idxLeft -= 1
        while (idxRight < len(pxx) - 1) and (pxx[idxRight] >= pxx[idxRight+1]):
            idxRight += 1

        idxLeft = max(0, idxLeft)
        idxRight = min(idxRight, len(pxx)-1)

    return idxTone, idxLeft, idxRight


def periodogram(data, Fs, window, method="welch", scaling="density"):
    f, pxx = None, None
    if method == "welch":
        f, pxx = scipy.signal.periodogram(data, Fs, window, scaling=scaling, detrend=False)
    if method == "fft":
        N = len(data)
        w = scipy.signal.get_window(window, N)
        signal = data * w
        dftout = np.abs(np.fft.rfft(signal))
        f = np.fft.rfftfreq(N, d=1.0/Fs)
        if scaling == "density":
            pxx = (1.0/(Fs * N)) * (dftout ** 2)
        else:
            pxx = (1.0 / (N ** 2)) * (dftout ** 2)
        pxx[1:N-1] = 2 * pxx[1:N-1]
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