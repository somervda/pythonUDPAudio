# Code from https://gist.github.com/GluTbl/a0c365c00799dec27e12db52c1e2717b 
# Note pyaudio needs to be loaded before running this https://pypi.org/project/PyAudio/ 
import pyaudio
import socket
import gc
import time
import sys
import keyboard

from threading import Thread

frames = []


def udpStream(CHUNK):

    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("192.168.1.117", 7000))

    while True:
        soundData, addr = udp.recvfrom(CHUNK * CHANNELS * 2)
        frames.append(soundData)

    udp.close()


def play(stream, CHUNK):
    BUFFER = 10
    while True:
        while len(frames) >=1:
            if keyboard.is_pressed("q"):
                print("q pressed, ending loop")
                break
            stream.write(frames.pop(0), CHUNK)



if __name__ == "__main__":
# Note: pyaudio uses a different chunk metric from Arduino Audio Library
# See: https://stackoverflow.com/questions/35970282/what-are-chunks-samples-and-frames-when-using-pyaudio#:~:text=%22CHUNK%22%20is%20the%20number%20of,get_sample_size(pyaudio.
    gc. disable()
    FORMAT = pyaudio.paInt16
    CHUNK = 512
    CHANNELS = 1
    RATE = 10000

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK,
                    )

    Ts = Thread(target=udpStream, args=(CHUNK,))
    Tp = Thread(target=play, args=(stream, CHUNK,))
    Ts.setDaemon(True)
    Tp.setDaemon(True)
    Ts.start()
    Tp.start()
    Ts.join()
    Tp.join()
