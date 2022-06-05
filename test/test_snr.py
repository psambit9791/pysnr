import sys
import os
sys.path.append(os.path.join("../pysnr"))

import numpy as np
import unittest
import pysnr
import scipy.signal


class TestUtils(unittest.TestCase):

    def test_mag2db(self):
        self.assertTrue(np.isclose(pysnr.mag2db(20), 26.0206))
        self.assertTrue(np.isclose(pysnr.mag2db(10), 20))
        self.assertTrue(np.isclose(pysnr.mag2db(5), 13.9794))

    def test_rssq(self):
        out = np.round(pysnr.rssq(np.array([1, 2, 3])), 4)
        self.assertTrue(np.isclose(out, 3.7417))

        out = np.round(pysnr.rssq(np.array([10, 20])), 4)
        self.assertTrue(np.isclose(out, 22.3607))

        out = np.round(pysnr.rssq(np.array([15, 22, 33, 57])), 4)
        self.assertTrue(np.isclose(out, 71.0422))

    def test_enbw(self):
        hamming = scipy.signal.get_window("hamming", 1000, fftbins=False)
        self.assertTrue(np.round(pysnr.utils.enbw(hamming), 4), 1.3638)

        flattop = scipy.signal.get_window("flattop", 1000, fftbins=False)
        self.assertTrue(np.round(pysnr.utils.enbw(flattop), 4), 3.7740)
        self.assertTrue(np.round(pysnr.utils.enbw(flattop, 44100), 4), 16.6285)


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
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs), 57.4232, rtol=0.5))

        signal = np.cos(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1))
        self.assertTrue(np.isclose(pysnr.snr_signal(signal + noise, Fs), 57.4282, rtol=0.5))


    def test_snr_psd(self):
        pass


    def test_snr_power(self):
        pass


class TestTHD(unittest.TestCase):
    pass


if __name__ == '__main__':
    unittest.main()