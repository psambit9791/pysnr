import numpy as np
import scipy.signal
from pysnr.utils import mag2db, remove_dc_component, alias_to_nyquist, bandpower
from pysnr.utils import _check_type_and_shape, _get_tone_indices_from_psd


def thd_signal(signal, fs=1.0, n=6, aliased=False, return_power=False):
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = remove_dc_component(signal)
    f, pxx = scipy.signal.periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return thd_power_spectral_density(pxx, f, n, aliased, return_power)


def thd_power_spectral_density(pxx, frequencies, n=6, aliased=False, return_power=False):
    pxx_dataCheck, pxx = _check_type_and_shape(pxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not pxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectral Density data and Frequency List must be 1-D arrays")
    if len(f) != len(pxx):
        raise AssertionError("Power Spectral Density data and Frequency List must be of same length")

    # Remove DC component
    pxx[0] = 2 * pxx[0]
    iHarm, iLeft, iRight = _get_tone_indices_from_psd(pxx, frequencies, 0)
    pxx[0:iRight + 1] = 0

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
            h = alias_to_nyquist(h, fs)
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

    if return_power:
        return mag2db(harmonic_power / signal_power), mag2db(harmonic_power)
    return mag2db(harmonic_power / signal_power)


def thd_power_spectrum(sxx, frequencies, rbw, n=6, aliased=False, return_power=False):
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return thd_power_spectral_density(pxx, f, n, aliased, return_power)