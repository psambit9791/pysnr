# PySNR

[![Build Status](https://app.travis-ci.com/psambit9791/pysnr.svg?branch=master)](https://app.travis-ci.com/psambit9791/pysnr)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?)](https://github.com/psambit9791/jdsp/blob/master/LICENSE)

PySNR is a Python library which provides a suite of tools to users for performing various types of noise analysis on 
a signal. PySNR aims to provide four main functionalities:
- [x] SNR (Signal to Noise Ratio)
- [x] THD (Total Harmonic Distortion)
- [x] SINAD (Signal to Noise and Distortion Ratio)
- [ ] SFDR (Spurious Free Dynamic Range)
- [ ] TOI (Third Order Intercept)

The following sections elaborate on each of these utilities further.


### <u>Signal to Noise Ratio</u> (SNR)

This calculates the signal-to-noise ratio for a input signal. Signal-to-Noise ratio is defined as the ratio 
between the power of the desired signal to the power of the background noise.

If the noise magnitude is provided along with the signal, the SNR is calculated using the following formula: 
$$20 \log_{10}\left({\frac{\sqrt{\sum signal^2}}{\sqrt{\sum noise^2}}}\right)$$

If the noise magnitude is not provided, a modified periodogram is computed using a Kaiser window with $\beta = 38$
and the SNR is computed using the power of fundamental frequency and the power of the signal after removing the top 6 
harmonics. The formula used in this case is:
$$10 \log_{10}\left({\frac{\sqrt{\sum signal^2}}{\sqrt{\sum noise^2}}}\right)$$

The SNR value can also be computed by providing the periodograms of *power spectral density* $(V^{2}/Hz)$ or 
*power spectrum* $(V^{2})$. In case of power spectrum periodograms,the resolution bandwidth needs to be provided 
as well. Utilities provide the ```enbw()``` function which computes the estimated noise bandwidth for assessing 
the resolution bandwidth.


### <u>Total Harmonic Distortion</u> (THD)

This calculates the total harmonic distortion for a signal. Total harmonic distortion is defined as the ratio
of the power of the harmonics to the power of the fundamental frequency.

A modified periodogram is computed using a Kaiser window with $\beta = 38$ and this information is then used to 
determine the fundamental frequency and its harmonics. The formula used for computing the THD is:
$$\frac{\sqrt{V^2_{H_1} + V^2_{H_2} + V^2_{H_3} + ...}}{V_{H_0}}$$

The THD value can also be computed by providing the periodograms of *power spectral density $(V^{2}/Hz)$* or 
*power spectrum $(V^{2})$*. In case of power spectrum periodograms, the resolution bandwidth needs to be provided 
as well. Utilities provide the ```enbw()``` function which computes the estimated noise bandwidth for assessing 
the resolution bandwidth.


### <u>Signal to Noise and Distortion Ratio</u> (SINAD)

This calculates the signal-to-noise-and-distortion ratio for a signal. SINAD is defined as the ratio between the 
power of the signal's fundamental frequency to the power of the background noise and harmonics.

A modified periodogram is computed using a Kaiser window with $\beta = 38$ and this information is then used to 
determine the fundamental frequency and its harmonics. The formula used for computing the SINAD is:
$$\frac{P_{fundamental}}{P_{noise} + P_{harmonics}}$$

The SINAD value can also be computed by providing the periodograms of *power spectral density $(V^{2}/Hz)$* or 
*power spectrum $(V^{2})$*. In case of power spectrum periodograms, the resolution bandwidth needs to be provided 
as well. Utilities provide the ```enbw()``` function which computes the estimated noise bandwidth for assessing 
the resolution bandwidth.

### <u>Third Order Intercept</u> (TOI)

This calculates the third order intercept point for a signal. There are six third-order intermodulation points from the 
top two dominant frequencies $F_1$ and $F_2$ (fundamental signals) &mdash; $3F_1$, $3F_2$, $2F_1 + F_2$, $2F_2 + F_1$, 
$2F_1 - F_2$ and $2F_2 - F_1$. Amongst these, the hardest to handle are $2F_1 - F_2$ and $2F_2 - F_1$ because of how c
lose they are to the fundamental signals. TOI helps us compute the point at which the power of the third order products 
intercepts the power of the fundamental signals. In real world devices, this does not happen because the output power is 
limited; hence, the TOI is a theoretical value. TOI helps evaluate the linearity of the signal source. The higher the 
TOI, the better the linearity with lower levels of intermodulation distortion.

A modified periodogram is computed using a Kaiser window with $\beta = 38$ and this information is then used to identify
the two dominant frequencies $F_1$ and $F_2$ which is considered the fundamental signal. The formula used for computing the SINAD is:
$$\overline{P_{fundamental}} + \frac{\overline{P_{fundamental}} - \overline{P_{intermodulation}}}{2}$$

The TOI value can also be computed by providing the periodograms of *power spectral density $(V^{2}/Hz)$* or 
*power spectrum $(V^{2})$*. In case of power spectrum periodograms, the resolution bandwidth needs to be provided 
as well. Utilities provide the ```enbw()``` function which computes the estimated noise bandwidth for assessing 
the resolution bandwidth.

### <u>Spurious Free Dynamic Range</u> (SFDR)
