Usage
========

Generating a Signal
--------------------

.. code-block:: python

    import numpy as np
    import pysnr

    Fi = 2500
    Fs = 48000
    N = 1000

    noise = 0.001 * np.random.randn(N)
    signal = np.sin(2*np.pi*(Fi/Fs)*np.arange(1, N+1))


Performing SNR
---------------

Using signal and noise
***********************

.. code-block:: python

    snr_value, noise_power = pysnr.snr_signal(signal, noise)

Using only signal
******************

.. code-block:: python

    snr_value, noise_power = pysnr.snr_signal(signal+noise, Fs)

Using only density periodogram
*******************************

.. code-block:: python

    f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
    snr_value, noise_power = pysnr.snr_power_spectral_density(pxx, f)

Using only spectrum periodogram
*******************************

.. code-block:: python

    f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
    w = scipy.signal.windows.kaiser(len(signal), 38, False)
    rbw = pysnr.utils.enbw(w, Fs)
    snr_value, noise_power = pysnr.snr_power_spectrum(sxx, f, rbw)


Performing THD
---------------

Using only signal
******************

.. code-block:: python

    thd_value, harmonic_power = pysnr.thd_signal(signal+noise, Fs)

Using only density periodogram
*******************************

.. code-block:: python

    f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
    thd_value, harmonic_power = pysnr.thd_power_spectral_density(pxx, f)

Using only spectrum periodogram
*******************************

.. code-block:: python

    f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
    w = scipy.signal.windows.kaiser(len(signal), 38, False)
    rbw = pysnr.utils.enbw(w, Fs)
    thd_value, harmonic_power = pysnr.thd_power_spectrum(sxx, f, rbw)


Performing SINAD
------------------

Using only signal
******************

.. code-block:: python

    sinad_value, noise_harmonic_power = pysnr.sinad_signal(signal+noise, Fs)

Using only density periodogram
*******************************

.. code-block:: python

    f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
    sinad_value, noise_harmonic_power = pysnr.sinad_power_spectral_density(pxx, f)

Using only spectrum periodogram
*******************************

.. code-block:: python

    f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
    w = scipy.signal.windows.kaiser(len(signal), 38, False)
    rbw = pysnr.utils.enbw(w, Fs)
    sinad_value, noise_harmonic_power = pysnr.sinad_power_spectrum(sxx, f, rbw)


Performing TOI
----------------

Using only signal
******************

.. code-block:: python

    toi_value, signal_power, imod_power = pysnr.toi_signal(signal+noise, Fs)

Using only density periodogram
*******************************

.. code-block:: python

    f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
    toi_value, signal_power, imod_power = pysnr.toi_power_spectral_density(pxx, f)

Using only spectrum periodogram
*******************************

.. code-block:: python

    f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
    w = scipy.signal.windows.kaiser(len(signal), 38, False)
    rbw = pysnr.utils.enbw(w, Fs)
    toi_value, signal_power, imod_power = pysnr.toi_power_spectrum(sxx, f, rbw)


Performing SFDR
----------------

Using only signal
******************

.. code-block:: python

    sfdr_value, spur_power = pysnr.sfdr_signal(signal+noise, Fs)

Using only density periodogram
*******************************

.. code-block:: python

    f, pxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38))
    sfdr_value, spur_power = pysnr.sfdr_power_spectral_density(pxx, f)

Using only spectrum periodogram
*******************************

.. code-block:: python

    f, sxx = pysnr.periodogram(signal+noise, Fs, window=('kaiser', 38), scaling="spectrum")
    w = scipy.signal.windows.kaiser(len(signal), 38, False)
    rbw = pysnr.utils.enbw(w, Fs)
    sfdr_value, spur_power = pysnr.sfdr_power_spectrum(sxx, f, rbw)