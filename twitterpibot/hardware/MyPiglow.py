import time
import random
from multiprocessing import Lock
import itertools

from PyGlow import PyGlow


def _get_led(arm, colour):
    return int(6 * arm + colour)


def _get_bright(factor):
    return max(0, min(int(-0.5 * _maxbright + _maxbright * factor), 255))


def _write_all():
    for led in range(18):
        _write_led(led)


def _write_led(led):
    bright = max(0, min(_buffer[led], 255))
    _piglow.led(led + 1, bright)


class PiglowMode(object):
    def camera_flash(self, on):
        with _lock:
            if on:
                _piglow.color("white", brightness=255)
            else:
                _write_all()

    def fade(self):
        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    _buffer[led] = max(0, _buffer[led] - 5)
            _write_all()

    def close(self):
        with _lock:
            for led in range(18):
                _buffer[led] = 0
            _write_all()

    def lights(self):
        time.sleep(1)


    def inbox_item_received(self, inbox_item):
        pass


class DotsMode(PiglowMode):
    def lights(self):
        with _lock:
            led = random.randint(0, 17)
            _buffer[led] = max(0, min((_buffer[led] + 1), 255))
            _write_led(led)

        time.sleep(2)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        with _lock:
            led = random.randint(0, 17)
            _buffer[led] = max(0, min((_buffer[led] + 1), 255))
            _write_led(led)


class FlashMode(PiglowMode):
    def lights(self):

        with _lock:
            for led in range(18):
                if _buffer[led] > 1:
                    if random.randint(0, 1) == 0:
                        _buffer[led] = 255
                    else:
                        _buffer[led] = 0
            _write_all()

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
            _write_all()


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


def lights():
    _mode.lights()


def camera_flash(on):
    _mode.camera_flash(on)


def inbox_item_received(inbox_item):
    _mode.inbox_item_received(inbox_item)


def on_lights_scheduled_task():
    with _lock:
        global _mode
        _mode = next(_modes)


def fade():
    _mode.fade()


def close():
    _mode.close()
