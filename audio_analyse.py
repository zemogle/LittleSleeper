import pyaudio
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

SAMPLE_RATE = 44100
CHUNK_SIZE = 512
AUDIO_FORMAT = pyaudio.paInt16

FORMAT = np.int16

def calculate_levels(data, chunk,sample_rate):
    # Convert raw data to numpy array
    # data = unpack("%dh"%(len(data)/2),data)
    # data = np.array(data, dtype='h')
    # Apply FFT - real data so rfft used
    fourier=np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier=np.delete(fourier,len(fourier)-1)
    # Find amplitude
    power = np.log10(np.abs(fourier))**2
    # Arrange array into 8 rows for the 8 bars on LED matrix
    print(power)
    power = np.reshape(power,(256,int(chunk/256)))
    matrix= np.int_(np.average(power,axis=1))
    return matrix


p = pyaudio.PyAudio()
stream = p.open(format=AUDIO_FORMAT, channels=2, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

signal = np.frombuffer(stream.read(CHUNK_SIZE, exception_on_overflow = False), FORMAT)

levels = calculate_levels(signal, CHUNK_SIZE, SAMPLE_RATE)
print(levels)
