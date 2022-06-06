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


if __name__ == '__main__':
    unittest.main()