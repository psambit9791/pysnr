import sys
import os
import numpy as np
import unittest
import scipy.signal
import scipy.io

sys.path.append(os.path.join("../pysnr"))
import pysnr


class TestSFDR(unittest.TestCase):

    def setUp(self):
        self.sine = scipy.io.loadmat("test/data/sine_data.mat")
        self.aliased = scipy.io.loadmat("test/data/alias_data.mat")
        self.cosine = scipy.io.loadmat("test/data/cosine_data.mat")

    def get_signal_data(self, struct):
        Fi = struct["Fi"].flatten()
        Fs = struct["Fs"].flatten()
        N = struct["N"].flatten()
        noise = struct["noise"].flatten()
        x = struct["x"].flatten()

        return Fi, Fs, N, noise, x

    def test_sfdr_signal(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        output = pysnr.sfdr_signal(signal + noise, Fs)
        self.assertTrue(np.isclose(output[0], 78.2632, rtol=0.025, equal_nan=True))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        output = pysnr.sfdr_signal(signal + noise, Fs, 100)
        self.assertTrue(np.isclose(output[0], 23.6745, rtol=0.025, equal_nan=True))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        output = pysnr.sfdr_signal(signal + noise, Fs)
        self.assertTrue(np.isclose(output[0], 78.2640, rtol=0.025, equal_nan=True))

    def test_sfdr_psd(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        output = pysnr.sfdr_power_spectral_density(pxx, f)
        self.assertTrue(np.isclose(output[0], 78.2632, rtol=0.025, equal_nan=True))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        f, pxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38))
        output = pysnr.sfdr_power_spectral_density(pxx, f)
        self.assertTrue(np.isclose(output[0], 23.6745, rtol=0.025, equal_nan=True))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, pxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38))
        output = pysnr.sfdr_power_spectral_density(pxx, f)
        self.assertTrue(np.isclose(output[0], 78.2640, rtol=0.025, equal_nan=True))

    def test_sfdr_power(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        output = pysnr.sfdr_power_spectrum(sxx, f, 0)
        self.assertTrue(np.isclose(output[0], 78.7755, rtol=0.025, equal_nan=True))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        output = pysnr.sfdr_power_spectrum(sxx, f, 100)
        self.assertTrue(np.isclose(output[0], 23.7732, rtol=0.025, equal_nan=True))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, sxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38), scaling="spectrum")
        output = pysnr.sfdr_power_spectrum(sxx, f, 10)
        self.assertTrue(np.isclose(output[0], 78.7762, rtol=0.025, equal_nan=True))


if __name__ == '__main__':
    unittest.main()