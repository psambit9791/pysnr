Quick Start
=============

------------------
What is PySNR?
------------------

PySNR is a suite of tools to analyse noise properties in signals in a variety of ways. The features available are
listed as follows:

1. SNR or Signal-to-Noise Ratio
2. THD or Total Harmonic Distortion
3. SINAD or Signal to Noise and Distortion Ratio
4. SFDR or Spurious Fre Dynamic Range
5. TOI or Third Order Intercept point


------------------
Installing PySNR
------------------

From the shell of your python environment type:

.. code-block:: bash

    $ pip install pysnr


------------------------------
MATLAB Equivalent Functions
------------------------------

.. list-table:: Signal-to-Noise Ratio (SNR)
   :widths: 50 50
   :header-rows: 1

   * - MATLAB
     - PySNR
   * - snr(signal, noise)
     - snr_signal_noise(signal, noise)
   * - snr(signal,Fs,n)
     - snr_signal(signal, Fs, n)
   * - snr(pxx,frequencies,n,'psd')
     - snr_power_spectral_density(pxx, frequencies, n)
   * - snr(sxx,frequencies,rbw,'power')
     - snr_power_spectrum(sxx, frequencies, n)
   * - snr(signal,Fs,n,'aliased')
     - snr_signal(signal, Fs, n, aliased=True)
   * - snr(pxx,frequencies,n,'psd','aliased')
     - snr_power_spectral_density(pxx, frequencies, n, aliased=True)
   * - snr(sxx,frequencies,rbw,'power','aliased')
     - snr_power_spectrum(sxx, frequencies, n, aliased=True)

.. list-table:: Total Harmonic Distortion (THD)
   :widths: 50 50
   :header-rows: 1

   * - MATLAB
     - PySNR
   * - thd(signal,Fs,n)
     - thd_signal(signal, Fs, n)
   * - thd(pxx,frequencies,n,'psd')
     - thd_power_spectral_density(pxx, frequencies, n)
   * - thd(sxx,frequencies,rbw,'power')
     - thd_power_spectrum(sxx, frequencies, n)
   * - thd(signal,Fs,n,'aliased')
     - thd_signal(signal, Fs, n, aliased=True)
   * - thd(pxx,frequencies,n,'psd','aliased')
     - thd_power_spectral_density(pxx, frequencies, n, aliased=True)
   * - thd(sxx,frequencies,rbw,'power','aliased')
     - thd_power_spectrum(sxx, frequencies, n, aliased=True)


.. list-table:: Signal to Noise and Distortion Ratio (SINAD)
   :widths: 50 50
   :header-rows: 1

   * - MATLAB
     - PySNR
   * - sinad(signal,Fs,n)
     - sinad_signal(signal, Fs, n)
   * - sinad(pxx,frequencies,n,'psd')
     - sinad_power_spectral_density(pxx, frequencies, n)
   * - sinad(sxx,frequencies,rbw,'power')
     - sinad_power_spectrum(sxx, frequencies, n)