import numpy as np
from pysnr.utils import mag2db, _remove_dc_component, bandpower, periodogram, _get_tone_indices_from_psd
from pysnr.utils import _check_type_and_shape


def sinad_signal(signal, fs=1.0, return_power=False):
    """SINAD from input signal without any known noise.

    This function computes the SINAD for an input signal.
    It assumes the fundamental frequency to be the desired signal

    Parameters
    ----------
    signal : numpy ndarray
        The true signal
    fs : float
        Sampling Frequency. Defaults to 1.0.
    return_power : bool
        If True, the total noise and harmonic power magnitude is returned

    Returns
    -------
    float
        The computed SINAD
    float (optional)
        The total noise and harmonic power magnitude
    """
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = _remove_dc_component(signal)
    f, pxx = periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return sinad_power_spectral_density(pxx, f, return_power)


def sinad_power_spectral_density(pxx, frequencies, return_power=False):
    """SINAD from input signal without any known noise.

    This function computes the SINAD for an input signal from its density-periodogram.
    The function assumes the fundamental frequency to be the desired signal

    Parameters
    ----------
    pxx : numpy ndarray
        The power spectral density of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    return_power : bool
        If True, the total noise and harmonic power magnitude is returned

    Returns
    -------
    float
        The computed SINAD
    float (optional)
        The total noise and harmonic power magnitude
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

    fh_idx = np.argmax(pxx)
    first_harmonic = f[fh_idx]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, first_harmonic)
    signal_pxx = np.copy(pxx[iLeft:iRight + 1])
    signal_f = np.copy(f[iLeft:iRight + 1])
    pxx[iLeft:iRight + 1] = 0.0

    estimated_noise_density = np.median(pxx[pxx > 0])
    for idx in np.where(pxx == 0)[0].flatten():
        pxx[idx] = estimated_noise_density
    pxx = np.min(np.vstack((pxx, origPxx)), 0)
    total_noise = bandpower(pxx, f)
    signal_power = bandpower(signal_pxx, signal_f)
    if return_power:
        return mag2db(signal_power / total_noise), mag2db(total_noise)
    return mag2db(signal_power / total_noise)


def sinad_power_spectrum(sxx, frequencies, rbw, return_power=False):
    """SINAD from input signal without any known noise.

    This function computes the SINAD for an input signal from its spectrum-periodogram.
    The function assumes the fundamental frequency to be the desired signal

    Parameters
    ----------
    sxx : numpy ndarray
        The power spectrum of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    rbw : float
        Resolution Bandwidth computed from the window and the sampling frequency
    return_power : bool
        If True, the total noise and harmonic power magnitude is returned

    Returns
    -------
    float
        The computed SINAD
    float (optional)
        The total noise and harmonic power magnitude
    """
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return sinad_power_spectral_density(pxx, f, return_power)
