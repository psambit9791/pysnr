import sys
import os
sys.path.append(os.path.join("../pysnr"))

import numpy as np
import unittest
import pysnr
import scipy.signal
import scipy.io


class TestTOI(unittest.TestCase):

    def setUp(self):
        self.sine = scipy.io.loadmat("test/data/sine_data.mat")
        self.aliased = scipy.io.loadmat("test/data/alias_data.mat")
        self.toi = scipy.io.loadmat("test/data/toi_data.mat")

    def get_signal_data(self, struct):
        Fi = struct["Fi"].flatten()
        Fs = struct["Fs"].flatten()
        N = struct["N"].flatten()
        noise = struct["noise"].flatten()
        x = struct["x"].flatten()

        return Fi, Fs, N, noise, x

    def test_toi_signal(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        output = pysnr.toi_signal(signal + noise, Fs)
        self.assertTrue(np.isclose(output[0], np.nan, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-81.2741, -3.0109]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([np.nan, -88.2758]), rtol=0.025, equal_nan=True).any())

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        output = pysnr.toi_signal(signal + noise, Fs)
        self.assertTrue(np.isclose(output[0], np.nan, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-4.8695, -28.5440]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([-50.4182, np.nan]), rtol=0.025, equal_nan=True).any())

        Fi, Fs, N, noise, signal = self.get_signal_data(self.toi)
        output = pysnr.toi_signal(signal + noise, Fs)
        self.assertTrue(np.isclose(output[0], 1.3951, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-22.9131, -22.9131]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([-71.5297, -71.5297]), rtol=0.025, equal_nan=True).any())

    def test_toi_psd(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
        output = pysnr.toi_power_spectral_density(pxx, f)
        self.assertTrue(np.isclose(output[0], np.nan, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-81.2741, -3.0109]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([np.nan, -88.2758]), rtol=0.025, equal_nan=True).any())

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        f, pxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38))
        output = pysnr.toi_power_spectral_density(pxx, f)
        self.assertTrue(np.isclose(output[0], np.nan, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-4.8695, -28.5440]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([-50.4182, np.nan]), rtol=0.025, equal_nan=True).any())

        Fi, Fs, N, noise, signal = self.get_signal_data(self.toi)
        f, pxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38))
        output = pysnr.toi_power_spectral_density(pxx, f)
        self.assertTrue(np.isclose(output[0], 1.3951, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-22.9131, -22.9131]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([-71.5297, -71.5297]), rtol=0.025, equal_nan=True).any())


    def test_toi_power(self):

        Fi, Fs, N, noise, signal = self.get_signal_data(self.sine)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38, False)
        rbw = pysnr.utils.enbw(w, Fs)
        output = pysnr.toi_power_spectrum(sxx, f, rbw)
        self.assertTrue(np.isclose(output[0], np.nan, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-81.2741, -3.0109]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([np.nan, -88.2758]), rtol=0.025, equal_nan=True).any())

        Fi, Fs, N, noise, signal = self.get_signal_data(self.aliased)
        f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        output = pysnr.toi_power_spectrum(sxx, f, rbw)
        self.assertTrue(np.isclose(output[0], np.nan, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-4.8695, -28.5440]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([-50.4182, np.nan]), rtol=0.025, equal_nan=True).any())

        Fi, Fs, N, noise, signal = self.get_signal_data(self.toi)
        f, sxx = pysnr.periodogram(signal + noise, Fs, window=('kaiser', 38), scaling="spectrum")
        w = scipy.signal.windows.kaiser(len(signal), 38)
        rbw = pysnr.utils.enbw(w, Fs)
        output = pysnr.toi_power_spectrum(sxx, f, rbw)
        self.assertTrue(np.isclose(output[0], 1.3844, rtol=0.025, equal_nan=True))
        self.assertTrue(np.isclose(output[1], np.array([-22.9133, -22.9132]), rtol=0.025, equal_nan=True).any())
        self.assertTrue(np.isclose(output[2], np.array([-71.4868, -71.5299]), rtol=0.025, equal_nan=True).any())


if __name__ == '__main__':
    unittest.main()