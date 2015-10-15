import math
import time
import random

from PyGlow import PyGlow
from multiprocessing import Lock

_maxbright = 255
_piglow = PyGlow()
_piglow.all(0)
_buffer = [0 for led in range(18)]
_lock = Lock()

def _getLed(arm, colour):
    return int(6 * arm + colour)

def _getBright(factor):
    return max(0, min(int(-0.5 * _maxbright + _maxbright * factor),255))


def OnInboxItemRecieved(inboxItem):
    with _lock:
        led = random.randint(0,17)
        _buffer[led] = max(0, min((_buffer[led] + 1), 255))
        _WriteLed(led)

def Fade():
    with _lock:
        for led in range(18):
            if _buffer[led] > 1:
                _buffer[led] = max(0,_buffer[led] - 5)        
        _WriteAll()

def _WriteAll():
    for led in range(18):
        _WriteLed(led)

def _WriteLed( led):
    bright = max(0, min(_buffer[led], 255))
    _piglow.led(led + 1, bright)

def CameraFlash(on):
    with _lock:
        if on:
            _piglow.color("white", brightness = 255)
        else:
            _WriteAll()

def Close():    
    with _lock:
        piglow = None