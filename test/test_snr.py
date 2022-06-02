import scipy as sp
import numpy as np
import sys, os

sys.path.append(os.path.join("../pysnr"))

import unittest
import pysnr
import math


class TestSNR(unittest.TestCase):

    def test_snr_1(self):
        Fi = 2500
        Fs = 48000
        N = 15

        np.random.seed(4)
        noise = 0.001 * np.random.randn(N)

        signal = np.sin(2*np.pi*(Fi/Fs)*np.arange(1, N+1))
        self.assertTrue(np.isclose(pysnr.snr(signal, noise), 59.8082))

        signal = np.cos(2 * np.pi * (Fi / Fs) * np.arange(1, N + 1))
        self.assertTrue(np.isclose(pysnr.snr(signal, noise), 58.9217))


if __name__ == '__main__':
    unittest.main()