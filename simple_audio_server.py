import Queue
import socket
import wave

import pyaudio

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
WIDTH = 2

HOST = '127.0.0.1'     # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
conn, addr = s.accept()
print('Connected by', addr)

p = pyaudio.PyAudio()
stream = p.open(format=AUDIO_FORMAT, channels=2, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

q = Queue.Queue()

frames = []

stream.start_stream()


def calculate_levels(data):
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
    power = np.reshape(power,(256,int(CHUNK/256)))
    matrix= np.int_(np.average(power,axis=1))
    return matrix

def main():
    data = conn.recv(CHUNK)

    while data != '':
        q.put(data)
        if not q.empty():
            stream.write(q.get())

        # stream.write(data)
        data = conn.recv(CHUNK)
        frames.append(data)

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    stream.stop_stream()
    stream.close()
    p.terminate()
    conn.close()

if __name__ == '__main__':
    main()
