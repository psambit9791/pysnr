import numpy as np
from pysnr.utils import rssq, mag2db, _remove_dc_component, bandpower, _alias_to_nyquist, periodogram, _get_tone_indices_from_psd
from pysnr.utils import _check_type_and_shape


def snr_signal_noise(signal, noise, return_power=False):
    """SNR from input signal and known noise.

    This function computes the SNR for a signal and a known noise.

    Parameters
    ----------
    signal : numpy ndarray
        The true signal
    noise : numpy ndarray
        The noise
    return_power : bool
        If True, the noise magnitude is returned

    Returns
    -------
    float
        The computed SNR
    float (optional)
        The noise magnitude
    """
    signalCheck, signal = _check_type_and_shape(signal)
    noiseCheck, noise = _check_type_and_shape(noise)
    if not signalCheck or not noiseCheck:
        raise TypeError("Signal and Noise must be 1-D arrays")
    if return_power:
        return mag2db(rssq(signal)**2 / rssq(noise)**2), rssq(noise)**2
    return mag2db(rssq(signal)**2 / rssq(noise)**2)


def snr_signal(signal, fs=1.0, n=6, aliased=False, return_power=False):
    """SNR from input signal without any known noise.

    This function computes the SNR for a signal where the noise is not known.
    It assumes the fundamental frequency to be the desired signal

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
    return_power : bool
        If True, the noise magnitude is returned

    Returns
    -------
    float
        The computed SNR
    float (optional)
        The noise power magnitude
    """
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = _remove_dc_component(signal)
    f, pxx = periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return snr_power_spectral_density(pxx, f, n, aliased, return_power)


def snr_power_spectral_density(pxx, frequencies, n=6, aliased=False, return_power=False):
    """SNR from input signal without any known noise.

    This function computes the SNR for a signal where the noise is not known from its density-periodogram.
    The function assumes the fundamental frequency to be the desired signal

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
    return_power : bool
        If True, the noise magnitude is returned

    Returns
    -------
    float
        The computed SNR
    float (optional)
        The noise power magnitude
    """

    pxx_dataCheck, pxx = _check_type_and_shape(pxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not pxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectral Density data and Frequency List must be 1-D arrays")
    if len(f) != len(pxx):
        raise AssertionError("Power Spectral Density data and Frequency List must be of same length")

    origPxx = np.copy(pxx)

    # Remove DC component
    pxx[0] = 2 * pxx[0]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, 0)
    pxx[0:iRight+1] = 0

    freq_indices = []
    harmonics = []

    fh_idx = np.argmax(pxx)
    first_harmonic = f[fh_idx]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, first_harmonic)
    freq_indices.append([iLeft, iHarm, iRight])
    fs = frequencies[-1] * 2

    for i in range(2, n+1):
        h = first_harmonic * i
        if aliased:
            h = _alias_to_nyquist(h, fs)
        if not aliased and h > fs/2:
            continue
        iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, h)
        harmonics.append(frequencies[iHarm])
        freq_indices.append([iLeft, iHarm, iRight])

    signal_power = np.empty(0)
    low_up_first_harmonic = np.empty(0)
    for idx, harmonic_idx in enumerate(freq_indices):
        low, harmid, up = harmonic_idx
        if idx == 0:
            signal_power = np.copy(pxx[low:up+1])
            low_up_first_harmonic = np.copy(f[low:up+1])
        pxx[low:up+1] = 0.0

    estimated_noise_density = np.median(pxx[pxx > 0])
    for idx in np.where(pxx == 0)[0].flatten():
        pxx[idx] = estimated_noise_density
    pxx = np.min(np.vstack((pxx, origPxx)), 0)
    total_noise = bandpower(pxx, f)
    signal_power = bandpower(signal_power, low_up_first_harmonic)
    if return_power:
        return mag2db(signal_power / total_noise), mag2db(total_noise)
    return mag2db(signal_power / total_noise)


def snr_power_spectrum(sxx, frequencies, rbw, n=6, aliased=False, return_power=False):
    """SNR from input signal without any known noise.

    This function computes the SNR for a signal where the noise is not known from its spectrum-periodogram.
    The function assumes the fundamental frequency to be the desired signal

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
    return_power : bool
        If True, the noise magnitude is returned

    Returns
    -------
    float
        The computed SNR
    float (optional)
        The noise power magnitude
    """
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return snr_power_spectral_density(pxx, f, n, aliased, return_power)