# PySNR

PySNR is a Python library which allows users to perform various types of noise analysis on a signal.
PySNR aims to provide four main functionalities:
- [x] SNR (Signal to Noise Ratio)
- [ ] THD (Total Harmonic Distortion)
- [ ] SINAD (Signal to Noise and Distortion Ratio)
- [ ] SFDR (Spurious Free Dynamic Range)

The following sections elaborate on each of these processes further.


### <u>Signal to Noise Ratio</u> (SNR)

This calculates the signal to noise ratio for any input signal. 
If the noise magnitude is provided along with the signal, the SNR is calculated using the following formula: 
$$20 \log_{10}\left({\frac{\sqrt{\sum signal^2}}{\sqrt{\sum noise^2}}}\right)$$
If the noise magnitude is not provided, a modified periodogram is computed using a Kaiser window with $$\beta = 38$$
and the SNR is computed using the power of fundamental frequency and the power of the signal afer removing the top 6 
harmonics. The formula used in this case is:
$$10 \log_{10}\left({\frac{\sqrt{\sum signal^2}}{\sqrt{\sum noise^2}}}\right)$$