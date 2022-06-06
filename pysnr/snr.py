import numpy as np
import scipy.signal
from pysnr.utils import rssq, mag2db, remove_dc_component, bandpower
from pysnr.utils import _check_type_and_shape, _find_range


def snr_signal_noise(signal, noise):
    signalCheck, signal = _check_type_and_shape(signal)
    noiseCheck, noise = _check_type_and_shape(noise)
    if not signalCheck or not noiseCheck:
        raise TypeError("Signal and Noise must be 1-D arrays")
    return mag2db(rssq(signal) / rssq(noise))


def snr_signal(signal, fs=1.0, n=6):
    signalCheck, signal = _check_type_and_shape(signal)
    if not signalCheck:
        raise TypeError("Signal must be a 1-D array")
    signal_no_dc = remove_dc_component(signal)
    f, pxx = scipy.signal.periodogram(signal_no_dc, fs, window=('kaiser', 38))
    return snr_power_spectral_density(pxx, f, n)


def snr_power_spectral_density(pxx, frequencies, n=6):

    def _remove_inconsistent_values(data):
        threshold = np.median(data) * 10
        updated = data[np.where(data < threshold)]
        return updated

    pxx_dataCheck, pxx = _check_type_and_shape(pxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not pxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectral Density data and Frequency List must be 1-D arrays")
    if len(f) != len(pxx):
        raise AssertionError("Power Spectral Density data and Frequency List must be of same length")

    freq_indices = []
    harmonics = []
    fh_idx = np.argmax(pxx)
    first_harmonic = f[fh_idx]
    freq_indices.append(fh_idx)

    for i in range(2, n + 1):
        h = first_harmonic * i
        closest_idx = np.argmin(np.abs(frequencies - h))
        idxMax = np.argmax(pxx[closest_idx-1:closest_idx+2])
        closest_idx += idxMax
        harmonics.append(frequencies[closest_idx])
        freq_indices.append(closest_idx)

    signal_power = np.empty(0)
    low_up_first_harmonic = np.empty(0)
    for idx, harmonic_idx in enumerate(freq_indices):
        low, up = _find_range(pxx, harmonic_idx)
        if idx == 0:
            signal_power = np.copy(pxx[low:up])
            low_up_first_harmonic = np.copy(f[low:up])
        pxx[low:up] = 0.0

    estimated_noise_density = np.median(pxx[pxx > 0])
    for idx in np.where(pxx == 0)[0].flatten():
        pxx[idx] = estimated_noise_density
    filtered_pxx = _remove_inconsistent_values(pxx)
    total_noise = bandpower(filtered_pxx, f)
    signal_power = bandpower(signal_power, low_up_first_harmonic)
    return mag2db(signal_power / total_noise, 10)


def snr_power_spectrum(sxx, frequencies, rbw, n=6):
    sxx_dataCheck, sxx = _check_type_and_shape(sxx)
    frequenciesCheck, f = _check_type_and_shape(frequencies)
    if not sxx_dataCheck or not frequenciesCheck:
        raise TypeError("Power Spectrum data and Frequency List must be 1-D arrays")
    if len(f) != len(sxx):
        raise AssertionError("Power Spectrum data and Frequency List must be of same length")
    pxx = sxx/rbw
    return snr_power_spectral_density(pxx, f, n)