import pyaudio
import numpy as np


def main():
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    while True:
        # grab audio and timestamp
        audio = np.fromstring(stream.read(CHUNK_SIZE, exception_on_overflow = False), np.int16)
        current_time = time.time()

if __name__ == '__main__':
    main()
