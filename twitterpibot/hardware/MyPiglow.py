import time
import random
from multiprocessing import Lock
import itertools

from PyGlow import PyGlow


def _getLed(arm, colour):
    return int(6 * arm + colour)


def _getBright(factor):
    return max(0, min(int(-0.5 * _maxbright + _maxbright * factor), 255))


def _WriteAll():
    for led in range(18):
        _WriteLed(led)


def _WriteLed(led):
    bright = max(0, min(_buffer[led], 255))
    _piglow.led(led + 1, bright)


class PiglowMode(object):
    def CameraFlash(self, on):
        with _lock:
            if on:
                _piglow.color("white", brightness=255)
            else:
                _WriteAll()

    def Fade(self):
        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    _buffer[led] = max(0, _buffer[led] - 5)
            _WriteAll()

    def Close(self):
        with _lock:
            for led in range(18):
                _buffer[led] = 0
            _WriteAll()


class DotsMode(PiglowMode):
    def Lights(self):
        with _lock:
            led = random.randint(0, 17)
            _buffer[led] = max(0, min((_buffer[led] + 1), 255))
            _WriteLed(led)

        time.sleep(2)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        with _lock:
            led = random.randint(0, 17)
            _buffer[led] = max(0, min((_buffer[led] + 1), 255))
            _WriteLed(led)


class FlashMode(PiglowMode):
    def Lights(self):

        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    if random.randint(0, 1) == 0:
                        _buffer[led] = 255
                    else:
                        _buffer[led] = 0
            _WriteAll()

        time.sleep(0.25)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    if random.randint(0, 1) == 0:
                        _buffer[led] = 255
                    else:
                        _buffer[led] = 0
            _WriteAll()


_maxbright = 255
_piglow = PyGlow()
_piglow.all(0)
_buffer = [0 for led in range(18)]
_lock = Lock()

_modes = itertools.cycle([
    DotsMode(),
    FlashMode()
])
_mode = next(_modes)


def Lights():
    _mode.lights()


def CameraFlash(on):
    _mode.camera_flash(on)


def Oninbox_itemRecieved(inbox_item):
    _mode.inbox_item_received(inbox_item)


def OnLightsScheduledTask():
    with _lock:
        global _mode
        _mode = next(_modes)


def Fade():
    _mode.fade()


def Close():
    _mode.close()
