import sys
import os
import numpy as np
import unittest
import scipy.signal
import scipy.io

sys.path.append(os.path.join("../pysnr"))
import pysnr


class TestSNR(unittest.TestCase):

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

    def test_snr_signal_noise(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        self.assertTrue(np.isclose(pysnr.snr_signal_noise(signal, noise), 57.0343, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        self.assertTrue(np.isclose(pysnr.snr_signal_noise(signal, noise), 57.0172, rtol=0.025))

    def test_snr_signal(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs), 57.7103, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs), 57.7142, rtol=0.025))

    def test_snr_psd(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.snr_power_spectral_density(pxx, f), 57.7103, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        self.assertTrue(np.isclose(pysnr.snr_power_spectral_density(pxx, f), 57.7142, rtol=0.025))

    def test_snr_power(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38, False)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.snr_power_spectrum(sxx, f, rbw), 57.7438, rtol=0.025))

        Fi, Fs, N, noise, signal = self.get_signal_data(self.cosine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        self.assertTrue(np.isclose(pysnr.snr_power_spectrum(sxx, f, rbw), 57.7449, rtol=0.025))

    def test_snr_aliased(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs, aliased=False), 23.6189, rtol=0.025))
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs, aliased=True), 55.0423, rtol=0.025))


if __name__ == '__main__':
    unittest.main()