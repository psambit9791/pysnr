import sys
import os
sys.path.append(os.path.join("../pysnr"))

import numpy as np
import unittest
import pysnr
import scipy.signal
import scipy.io


class TestSINAD(unittest.TestCase):

    def setUp(self):
        self.sine = scipy.io.loadmat("test/data/sine_data.mat")
        self.cosine = scipy.io.loadmat("test/data/cosine_data.mat")
        self.aliased = scipy.io.loadmat("test/data/alias_data.mat")

    def get_signal_data(self, struct):
        Fi = struct["Fi"].flatten()[0]
        Fs = struct["Fs"].flatten()[0]
        N = struct["N"].flatten()[0]
        noise = struct["noise"].flatten()
        x = struct["x"].flatten()

        return Fi, Fs, N, noise, x

    def test_sinad_signal(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        self.assertTrue(np.isclose(pysnr.sinad_signal(signal + noise, Fs), 57.0571, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        self.assertTrue(np.isclose(pysnr.sinad_signal(signal + noise, Fs), 57.0566, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        self.assertTrue(np.isclose(pysnr.sinad_signal(signal + noise, Fs), 22.5389, rtol=0.025))

    def test_sinad_psd(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.sinad_power_spectral_density(pxx, f), 57.0571, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.sinad_power_spectral_density(pxx, f), 57.0566, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        f, pxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.sinad_power_spectral_density(pxx, f), 22.5389, rtol=0.025))

    def test_sinad_power(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38, False)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.sinad_power_spectrum(sxx, f, rbw), 57.0542, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.sinad_power_spectrum(sxx, f, rbw), 57.0550, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        f, sxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.sinad_power_spectrum(sxx, f, rbw), 22.5389, rtol=0.025))


if __name__ == '__main__':
    unittest.main()