from numpy import sin, linspace, pi, arange, fft

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def plotSpectrum(y,Fs):
    """
    Plots a Single-Sided Amplitude Spectrum of y(t)
    """
    n = len(y) # length of the signal
    k = arange(n)
    T = n/Fs
    frq = k/T # two sides frequency range
    midpoint = int(n/2)
    frq = frq[range(midpoint)] # one side frequency range

    Y = fft.fft(y)/n # fft computing and normalization
    Y = Y[range(midpoint)]
    return frq, abs(Y)

Fs = 150.0;  # sampling rate
Ts = 1.0/Fs; # sampling interval
t = arange(0,1,Ts) # time vector

ff = 5;   # frequency of the signal
y = sin(2*pi*ff*t)

freq, Y  = plotSpectrum(y,Fs)
plt.plot(freq,Y)
plt.show()
