import numpy as np
import scipy.signal
from pysnr.utils import  _remove_dc_component, _alias_to_nyquist, _check_type_and_shape, _get_tone_indices_from_psd
from pysnr.utils import mag2db, bandpower


def thd_signal(signal, fs=1.0, n=6, aliased=False):
    """THD from input signal.

    This function computes the THD for an input signal.
    It assumes the fundamental frequency to be the desired signal.
    Uses a Kaiser window with beta set to 38 to compute the periodogram.

    Parameters
    ----------
    signal : numpy ndarray
        The true signal
    fs : float
        Sampling Frequency. Defaults to 1.0.
    n : int
        Number of harmonics to use (including the fundamental frequency)
    aliased : bool
        If True, converts the harmonics that are aliased into the Nyquist frequency

    Returns
    -------
    float
        The computed THD
    float
        The harmonic power magnitude
    """
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = _remove_dc_component(signal)
    f, pxx = scipy.signal.periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return thd_power_spectral_density(pxx, f, n, aliased)


def thd_power_spectral_density(pxx, frequencies, n=6, aliased=False):
    """THD from input signal.

    This function computes the THD for an input signal from its density-periodogram.
    The function assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    pxx : numpy ndarray
        The power spectral density of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    n : int
        Number of harmonics to use (including the fundamental frequency)
    aliased : bool
        If True, converts the harmonics that are aliased into the Nyquist frequency

    Returns
    -------
    float
        The computed THD
    float
        The harmonic power magnitude
    """
    pxx_dataCheck, pxx = _check_type_and_shape(pxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not pxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectral Density data and Frequency List must be 1-D arrays")
    if len(f) != len(pxx):
        raise AssertionError("Power Spectral Density data and Frequency List must be of same length")

    # Remove DC component
    pxx[0] = 2 * pxx[0]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, 0)
    pxx[iLeft:iRight + 1] = 0

    freq_indices = []
    harmonics = []

    fh_idx = np.argmax(pxx)
    first_harmonic = f[fh_idx]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, first_harmonic)
    freq_indices.append([iLeft, iHarm, iRight])
    fs = frequencies[-1] * 2

    for i in range(2, n + 1):
        h = first_harmonic * i
        if aliased:
            h = _alias_to_nyquist(h, fs)
        if not aliased and h > fs / 2:
            continue
        iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, h)
        harmonics.append(frequencies[iHarm])
        freq_indices.append([iLeft, iHarm, iRight])

    signal_power = 0
    harmonic_power = 0
    for idx, harmonic_idx in enumerate(freq_indices):
        low, harmid, up = harmonic_idx
        if idx == 0:
            signal_power = bandpower(pxx[low:up + 1], f[low:up+1])
        else:
            harmonic_power += bandpower(pxx[low:up + 1], f[low:up + 1])

    return mag2db(harmonic_power / signal_power), mag2db(harmonic_power)


def thd_power_spectrum(sxx, frequencies, rbw, n=6, aliased=False):
    """THD from input signal.

    This function computes the THD for an input signal from its spectrum-periodogram.
    The function assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    sxx : numpy ndarray
        The power spectrum of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    rbw : float
        Resolution Bandwidth computed from the window and the sampling frequency
    n : int
        Number of harmonics to use (including the fundamental frequency)
    aliased : bool
        If True, converts the harmonics that are aliased into the Nyquist frequency

    Returns
    -------
    float
        The computed THD
    float
        The harmonic power magnitude
    """
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return thd_power_spectral_density(pxx, f, n, aliased)
