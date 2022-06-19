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


def _get_tone_indices_from_psd(pxx, frequencies, tone_freq):
    idxTone = np.nan
    idxLeft = 0
    idxRight = 0

    if frequencies[0] <= tone_freq < frequencies[-1]:
        idxTone = np.argmin(np.abs(frequencies - tone_freq))
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

    if np.isnan(idxTone):
        return idxTone, 0, -1
    return idxTone, idxLeft, idxRight


def _alias_to_nyquist(f, fs):
    tone = f % fs
    if tone > fs/2:
        return fs - tone
    else:
        return tone


def _remove_dc_component(signal):
    return signal - np.mean(signal)


def periodogram(data, Fs, window, method="welch", scaling="density"):
    """Computes the periodogram from signal.

    This function computes the periodogram using one of two techniques - Welch method or FFT method
    By default, it is set to Welch method.

    Parameters
    ----------
    data : numpy ndarray
        The signal whose periodogram is to be computed
    Fs : numpy ndarray
        Sampling Freqeuncy of input signal
    window : str or tuple or array_like
        Desired window to use. This is passed as an input to scipy's get_window() function
    method : str
        Decides which method to use for computing the periodogram. Can be `welch` or 'fft'
    scaling : str
        Decides whether to compute the power spectral density or the power spectrum. Can be 'density' or 'spectrum'

    Returns
    -------
    numpy ndarray
        List of frequencies
    numpy ndarray
        The periodogram
    """
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


def rssq(data):
    """Computes the root of sum of squares.


    Parameters
    ----------
    data : numpy ndarray
        Array of numbers

    Returns
    -------
    float
        The computed value
    """
    return np.sqrt(np.sum(data ** 2))


def mag2db(data, scaling=10):
    """Converts the magnitude to decibels


    Parameters
    ----------
    data : flaot or numpy ndarray
        Item to be converted
    scaling : int
        Value by which the log is to be scaled


    Returns
    -------
    float or numpy ndarray
        The converted items
    """
    return scaling * np.log10(data, where=(data != 0))


def enbw(window, Fs=None):
    """Computes the equivalent noise bandwidth

    Parameters
    ----------
    window : numpy ndarray
        The window as an array of floats.
    Fs : float
        Sampling frequency of original signal

    Returns
    -------
    float
        The computed value
    """
    bw = (np.sqrt(np.mean(window**2))/np.mean(window)) ** 2
    if Fs is not None:
        bw = bw * Fs/len(window)
    return bw


def bandpower(pxx, f):
    """Computes the equivalent noise bandwidth

    Parameters
    ----------
    pxx : numpy ndarray
        The periodogram values in the power spectral density form
    f : numpy ndarray
        The frequencies corresponding to the periodogram

    Returns
    -------
    float
        The computed value
    """
    if len(pxx) == 0:
        return np.nan
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