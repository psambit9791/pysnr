import numpy as np
from pysnr.utils import mag2db, bandpower, periodogram
from pysnr.utils import _check_type_and_shape, _remove_dc_component, _get_tone_indices_from_psd


def toi_signal(signal, fs=1.0):
    """TOI from input signal.

    This function computes the TOI for an input signal.
    It assumes the fundamental frequency to be the desired signal.
    Uses a Kaiser window with beta set to 38 to compute the periodogram.

    Parameters
    ----------
    signal : numpy ndarray
        The true signal
    fs : float
        Sampling Frequency. Defaults to 1.0.

    Returns
    -------
    float
        The computed TOI
    np.ndarray
        The powers contained in the two fundamental sinusoids of the signal
    np.ndarray
        The power contained in the lower and upper intermodulation products of the signal
    """
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = _remove_dc_component(signal)
    f, pxx = periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return toi_power_spectral_density(pxx, f)


def toi_power_spectral_density(pxx, frequencies):
    """TOI from input signal.

    This function computes the TOI for an input signal from its density-periodogram.
    The function assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    pxx : numpy ndarray
        The power spectral density of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density

    Returns
    -------
    float
        The computed TOI
    np.ndarray
        The powers contained in the two fundamental sinusoids of the signal
    np.ndarray
        The power contained in the lower and upper intermodulation products of the signal
    """
    pxx_dataCheck, pxx = _check_type_and_shape(pxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not pxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectral Density data and Frequency List must be 1-D arrays")
    if len(f) != len(pxx):
        raise AssertionError("Power Spectral Density data and Frequency List must be of same length")

    # Remove DC component
    pxx[0] = 2 * pxx[0]
    iDCHarm, iDCLeft, iDCRight = _get_tone_indices_from_psd(pxx, frequencies, 0)
    pxx[iDCLeft:iDCRight+1] = 0

    # Dominant Frequency
    fh_idx = np.argmax(pxx)
    dominant1 = f[fh_idx]
    d1iHarm, d1iLeft, d1iRight = _get_tone_indices_from_psd(pxx, frequencies, dominant1)
    dominant1_pxx = np.copy(pxx[d1iLeft:d1iRight + 1])
    pxx[d1iLeft:d1iRight + 1] = 0.0
    # Second Dominant Frequency
    fh_idx = np.argmax(pxx)
    dominant2 = f[fh_idx]
    d2iHarm, d2iLeft, d2iRight = _get_tone_indices_from_psd(pxx, frequencies, dominant2)
    # Restore Dominant
    pxx[d1iLeft:d1iRight + 1] = dominant1_pxx

    # Flip order if new dominant less than old dominant
    if d2iHarm < d1iHarm:
        d1iHarm, d2iHarm = d2iHarm, d1iHarm
        d1iLeft, d2iLeft = d2iLeft, d1iLeft
        d1iRight, d2iRight = d2iRight, d1iRight

    dominant1_pxx = np.copy(pxx[d1iLeft:d1iRight + 1])
    dominant1_f = np.copy(f[d1iLeft:d1iRight + 1])
    dominant2_pxx = np.copy(pxx[d2iLeft:d2iRight + 1])
    dominant2_f = np.copy(f[d2iLeft:d2iRight + 1])

    # Lower Third IMOD
    lower_third_imod = (2 * f[d1iHarm]) - f[d2iHarm]
    ltiIndices = _get_tone_indices_from_psd(pxx, frequencies, lower_third_imod)
    ltiPower = pxx[ltiIndices[1]: ltiIndices[2]+1]
    ltiF = f[ltiIndices[1]: ltiIndices[2]+1]

    # Upper Third IMOD
    upper_third_imod = (2 * f[d2iHarm]) - f[d1iHarm]
    utiIndices = _get_tone_indices_from_psd(pxx, frequencies, upper_third_imod)
    utiPower = pxx[utiIndices[1]: utiIndices[2]+1]
    utiF = f[utiIndices[1]: utiIndices[2]+1]

    oip3 = np.nan
    # Compute fundamental power and imod power
    fund_power = np.array([bandpower(dominant1_pxx, dominant1_f), bandpower(dominant2_pxx, dominant2_f)])
    imod_power = np.array([bandpower(ltiPower, ltiF), bandpower(utiPower, utiF)])
    fund_power = mag2db(fund_power)
    imod_power = mag2db(imod_power)

    # Compute TOI
    if not np.isnan(imod_power).any() and not np.isnan(imod_power).any():
        oip3 = np.mean(fund_power) + ((np.mean(fund_power) - np.mean(imod_power)) / 2)

    return oip3, fund_power, imod_power


def toi_power_spectrum(sxx, frequencies, rbw):
    """TOI from input signal.

    This function computes the TOI for an input signal from its spectrum-periodogram.
    The function assumes the fundamental frequency to be the desired signal.

    Parameters
    ----------
    sxx : numpy ndarray
        The power spectrum of the signal
    frequencies : numpy ndarray
        The frequencies corresponding to the power spectral density
    rbw : float
        Resolution Bandwidth computed from the window and the sampling frequency

    Returns
    -------
    float
        The computed TOI
    np.ndarray
        The powers contained in the two fundamental sinusoids of the signal
    np.ndarray
        The power contained in the lower and upper intermodulation products of the signal
    """
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return toi_power_spectral_density(pxx, f)
