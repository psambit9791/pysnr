import sys
import os
sys.path.append(os.path.join("../pysnr"))

import numpy as np
import unittest
import pysnr
import scipy.signal


class TestSNR(unittest.TestCase):

    def test_snr_signal_noise(self):
        Fi = 2500
        Fs = 48000
        N = 1024

        np.random.seed(4)
        noise = 0.001 * np.random.randn(N)

        signal = np.sin(2*np.pi*(Fi/Fs) * np.arange(1, N+1))
        self.assertTrue(np.isclose(pysnr.snr_signal_noise(signal, noise), 57.3851))

        signal = np.cos(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1))
        self.assertTrue(np.isclose(pysnr.snr_signal_noise(signal, noise), 57.3679))

    def test_snr_signal(self):
        Fi = 2500
        Fs = 48000
        N = 1024

        np.random.seed(4)
        noise = np.round(0.001 * np.random.randn(N), 4)

        signal = np.round(np.sin(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1)), 4)
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs), 57.4232, rtol=0.005))

        signal = np.cos(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1))
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs), 57.4282, rtol=0.005))

    def test_snr_psd(self):
        Fi = 2500
        Fs = 48000
        N = 1024

        np.random.seed(4)
        noise = np.round(0.001 * np.random.randn(N), 4)

        signal = np.round(np.sin(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1)), 4) + noise
        f, pxx = scipy.signal.periodogram(signal, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.snr_power_spectral_density(pxx, f), 57.4232, rtol=0.005))

        signal = np.cos(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1)) + noise
        f, pxx = scipy.signal.periodogram(signal, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.snr_power_spectral_density(pxx, f), 57.4282, rtol=0.005))

    def test_snr_power(self):
        Fi = 2500
        Fs = 48000
        N = 1024

        np.random.seed(4)
        noise = np.round(0.001 * np.random.randn(N), 4)

        signal = np.round(np.sin(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1)), 4) + noise
        f, sxx = scipy.signal.periodogram(signal, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38, False)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.snr_power_spectrum(sxx, f, rbw), 57.4232, rtol=0.005))

        signal = np.cos(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1)) + noise
        f, sxx = scipy.signal.periodogram(signal, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.snr_power_spectrum(sxx, f, rbw), 57.4282, rtol=0.005))


if __name__ == '__main__':
    unittest.main()