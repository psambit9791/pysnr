import numpy as np
from pysnr.utils import mag2db, bandpower, periodogram
from pysnr.utils import _check_type_and_shape, _remove_dc_component, _get_tone_indices_from_psd, _get_peak_border


def sfdr_signal(signal, fs=1.0, msd=0):
    """SFDR from input signal.

    This function computes the SFDR for an input signal.
    It assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    signal : numpy ndarray
        The true signal
    fs : float
        Sampling Frequency. Defaults to 1.0.
    msd : int
        Minimum number of discrete Fourier bins to ignore for the SFDR computation

    Returns
    -------
    float
        The computed SFDR
    float
        The spurious power magnitude
    """
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = _remove_dc_component(signal)
    f, pxx = periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return sfdr_power_spectral_density(pxx, f, msd)


def sfdr_power_spectral_density(pxx, frequencies, msd=0):
    """SFDR from input signal.

    This function computes the SFDR for an input signal from its density-periodogram.
    The function assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    pxx : numpy ndarray
        The power spectral density of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    msd : int
        Minimum number of discrete Fourier bins to ignore for the SFDR computation

    Returns
    -------
    float
        The computed SFDR
    float
        The spurious power magnitude
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

    # Largest Frequency
    fh_idx = np.argmax(pxx)
    first_harmonic = f[fh_idx]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, first_harmonic)
    signal_pxx = np.copy(pxx[iLeft:iRight + 1])
    signal_f = np.copy(f[iLeft:iRight + 1])
    pxx[iLeft:iRight + 1] = 0.0

    # Remove MSD if greater than 0
    pxx[np.abs(f-first_harmonic) < msd] = 0.0

    # Identify Spurious Bin
    spur_idx = np.argmax(pxx)
    spur_freq = f[spur_idx]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, spur_freq)
    spur_pxx = np.copy(pxx[iLeft:iRight + 1])
    spur_f = np.copy(f[iLeft:iRight + 1])

    signal_power = bandpower(signal_pxx, signal_f)
    spur_power = bandpower(spur_pxx, spur_f)
    return mag2db(signal_power / spur_power), mag2db(spur_power)


def sfdr_power_spectrum(sxx, frequencies, msd=0):
    """SFDR from input signal.

    This function computes the SFDR for an input signal from its spectrum-periodogram.
    The function assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    sxx : numpy ndarray
        The power spectrum of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    msd : int
        Minimum number of discrete Fourier bins to ignore for the SFDR computation

    Returns
    -------
    float
        The computed SFDR
    float
        The spurious power magnitude
    """
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")

    # Remove DC component
    sxx[0] = 2 * sxx[0]
    idx_dc_stop = np.argwhere(sxx[0:len(sxx)-1] < sxx[1:len(sxx)]).flatten()[0]
    if not np.isnan(idx_dc_stop) and idx_dc_stop != 0:
        sxx[0:idx_dc_stop+1] = 0.0

    fund_idx = np.argmax(sxx)
    fund_freq = f[fund_idx]
    fund_pow = sxx[fund_idx]
    leftBinFund, rightBinFund = _get_peak_border(sxx, f, fund_freq, fund_idx, msd)
    sxx[leftBinFund: rightBinFund+1] = 0.0

    spur_idx = np.argmax(sxx)
    spur_pow = sxx[spur_idx]

    return mag2db(fund_pow / spur_pow), mag2db(spur_pow)