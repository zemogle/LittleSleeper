import pyaudio
import numpy as np

CHUNK_SIZE = 8192
AUDIO_FORMAT = pyaudio.paInt16
SAMPLE_RATE = 44100
max = 0.

def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    while True:
        # grab audio and timestamp
        audio = np.fromstring(stream.read(CHUNK_SIZE, exception_on_overflow = False), np.int16)
        newmax = np.abs(audio).max()
        if newmax > max:
            max = newmax
            print(" Max = {}".format(max))
    return

if __name__ == '__main__':
    main()
