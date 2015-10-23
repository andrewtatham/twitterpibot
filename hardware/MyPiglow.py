import math
import time
import random

from PyGlow import PyGlow
from multiprocessing import Lock
from LightsMode import LightsMode

_maxbright = 255
_piglow = PyGlow()
_piglow.all(0)
_buffer = [0 for led in range(18)]
_lock = Lock()

_modes = itertools.Cycle([
    DotsMode(),
    FlashMode()
    ])
_mode = _modes.next()


def _getLed(arm, colour):
    return int(6 * arm + colour)

def _getBright(factor):
    return max(0, min(int(-0.5 * _maxbright + _maxbright * factor),255))

def _WriteAll():
    for led in range(18):
        _WriteLed(led)

def _WriteLed( led):
    bright = max(0, min(_buffer[led], 255))
    _piglow.led(led + 1, bright)



def Lights():
    _mode.Lights()

def CameraFlash(on):
    _mode.CameraFlash(on)

def OnInboxItemRecieved(inboxItem):
    _mode.OnInboxItemRecieved(inboxItem)

def OnLightsScheduledTask():
    mode = _modes.next()

def Fade():
    _mode.Fade();

def Close():
    _mode.Close()

class PiglowMode(LightsMode):
    def CameraFlash(self, on):
        with _lock:
            if on:
                _piglow.color("white", brightness = 255)
            else:
                _WriteAll()


    def Fade(self):
        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    _buffer[led] = max(0,_buffer[led] - 5)        
            _WriteAll()


    def Close(self):
        with _lock:
            for led in range(18):
                _buffer[led] = 0
            _WriteAll()


class DotsMode(PiglowMode):
    def OnInboxItemRecieved(self, inboxItem):
        with _lock:
            led = random.randint(0,17)
            _buffer[led] = max(0, min((_buffer[led] + 1), 255))
            _WriteLed(led)


class FlashMode(PiglowMode):
    def __init__(self):
        self.state = False

    def Lights(self):

        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    if state:
                        _buffer[led] = 255        
                    else:
                        _buffer[led] = 0
            _WriteAll()

        time.sleep(0.25)


   

















def CameraFlash(on):


def Close():    
    with _lock:
        _piglow.all(0)
        piglow = None