import numpy as np
from pysnr.utils import mag2db, remove_dc_component, bandpower, periodogram, _get_tone_indices_from_psd
from pysnr.utils import _check_type_and_shape


def sinad_signal(signal, fs=1.0, return_power=False):
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = remove_dc_component(signal)
    f, pxx = periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return sinad_power_spectral_density(pxx, f, return_power)


def sinad_power_spectral_density(pxx, frequencies, return_power=False):

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
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return sinad_power_spectral_density(pxx, f, return_power)
