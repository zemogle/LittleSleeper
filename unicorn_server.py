import pyaudio
import numpy as np
import sys
import time
import asyncio
import websockets
import json

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
    power = np.reshape(power,(256,int(chunk/256)))
    matrix= np.int_(np.average(power,axis=1))
    return matrix

def colourise(val):
    # loud is red, quiessent is blue, green is in the middle
    if val > 255:
        val = 255

    if val > 190:
        colour = (val, 0, 0)
    elif val >=85 and val <= 190:
        colour = (0, val, 0)
    else:
        colour = (0, 0, val)
    return colour


async def display(stream, websocket, path):
    while True:
        rgb = []
        signal = np.frombuffer(stream.read(CHUNK_SIZE, exception_on_overflow = False), FORMAT)

        levels = calculate_levels(signal, CHUNK_SIZE, SAMPLE_RATE)
        for i in range(0,256):
            val = levels[i]
            rgb.append(colourise(val*10.))
        await websocket.send(json.dumps(rgb))

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    stream = p.open(format=AUDIO_FORMAT, channels=2, rate=SAMPLE_RATE, input=True, frames_per_buffer=CHUNK_SIZE)

    start_server = websockets.serve(display, stream, '127.0.0.1', 5678)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
