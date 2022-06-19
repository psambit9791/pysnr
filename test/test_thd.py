import sys
import os
sys.path.append(os.path.join("../pysnr"))

import numpy as np
import unittest
import pysnr
import scipy.signal
import scipy.io


class TestTHD(unittest.TestCase):

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

    def test_thd_signal(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        self.assertTrue(np.isclose(pysnr.thd_signal(signal + noise, Fs)[0], -86.1283, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        self.assertTrue(np.isclose(pysnr.thd_signal(signal + noise, Fs)[0], -86.1291, rtol=0.025))

    def test_thd_psd(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.thd_power_spectral_density(pxx, f)[0], -86.1283, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.thd_power_spectral_density(pxx, f)[0], -86.1291, rtol=0.025))

    def test_thd_power(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38, False)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.thd_power_spectrum(sxx, f, rbw)[0], -86.1283, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.thd_power_spectrum(sxx, f, rbw)[0], -86.1291, rtol=0.025))

    def test_thd_aliased(self):
        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        self.assertTrue(np.isclose(pysnr.thd_signal(signal + noise, Fs, aliased=False)[0], -29.1114, rtol=0.025))
        self.assertTrue(np.isclose(pysnr.thd_signal(signal + noise, Fs, aliased=True)[0], -22.5413, rtol=0.025))


if __name__ == '__main__':
    unittest.main()