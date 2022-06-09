# PySNR

PySNR is a Python library which provides a suite of tools to users for performing various types of noise analysis on 
a signal. PySNR aims to provide four main functionalities:
- [x] SNR (Signal to Noise Ratio)
- [ ] THD (Total Harmonic Distortion)
- [ ] SINAD (Signal to Noise and Distortion Ratio)
- [ ] SFDR (Spurious Free Dynamic Range)

The following sections elaborate on each of these utilities further.


### <u>Signal to Noise Ratio</u> (SNR)

This calculates the signal-to-noise ratio for any input signal. Signal-to-Noise ratio is defined as the ratio 
between the power of the desired signal to the power of the background noise.

If the noise magnitude is provided along with the signal, the SNR is calculated using the following formula: 
$$20 \log_{10}\left({\frac{\sqrt{\sum signal^2}}{\sqrt{\sum noise^2}}}\right)$$
If the noise magnitude is not provided, a modified periodogram is computed using a Kaiser window with $\beta = 38$
and the SNR is computed using the power of fundamental frequency and the power of the signal after removing the top 6 
harmonics. The formula used in this case is:
$$10 \log_{10}\left({\frac{\sqrt{\sum signal^2}}{\sqrt{\sum noise^2}}}\right)$$

The SNR value can also be computed by providing the periodograms of *power spectral density $(V^{2}/Hz)$* or 
*power spectrum $(V^{2})$*. In case of power spectrum periodograms,the resolution bandwidth needs to be provided 
as well. Utilities provide the ```enbw()``` function which computes the estimated noise bandwidth for assessing 
the resolution bandwidth.


### <u>Total Harmonic Distortion</u> (THD)

This calculates the total harmonic distortion for any signal. Total harmonic distortion is defined as the ratio
of the power of the harmonics to the power of the fundamental frequency.

A modified periodogram is computed using a Kaiser window with $\beta = 38$ and this information is then used to 
determine the fundamental frequency and its harmonics. The formula used for computing the THD is:
$$\frac{\sqrt{V_{H_2} + V_{H_3} + V_{H_4} + ...}}{V_{H_1}}$$

The THD value can also be computed by providing the periodograms of *power spectral density $(V^{2}/Hz)$* or 
*power spectrum $(V^{2})$*. In case of power spectrum periodograms,the resolution bandwidth needs to be provided 
as well. Utilities provide the ```enbw()``` function which computes the estimated noise bandwidth for assessing 
the resolution bandwidth.