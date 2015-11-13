import random
import unicornhat
import time
import itertools
from multiprocessing import Lock

import colorsys


def _WritePixel(x, y):
    pixel = _buffer[x][y]
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    unicornhat.set_pixel(x, y, r, g, b)


def _WriteAll():
    for y in range(8):
        for x in range(8):
            _WritePixel(x, y)
    unicornhat.show()


class UnicornHatMode(object):
    def camera_flash(self, on):
        with _lock:
            for y in range(8):
                for x in range(8):
                    if on:
                        r = 255
                        g = 255
                        b = 255
                    else:
                        pixel = _buffer[x][y]
                        r = pixel[0]
                        g = pixel[1]
                        b = pixel[2]
                    unicornhat.set_pixel(x, y, r, g, b)
            unicornhat.show()

    def fade(self):
        with _lock:
            for y in range(8):
                for x in range(8):
                    pixel = _buffer[x][y]
                    r = max(pixel[0] - 1, 0)
                    g = max(pixel[1] - 1, 0)
                    b = max(pixel[2] - 1, 0)
                    _buffer[x][y] = (r, g, b)
                    unicornhat.set_pixel(x, y, r, g, b)
            unicornhat.show()

    def close(self):
        with _lock:
            r = 0
            g = 0
            b = 0
            for y in range(8):
                for x in range(8):
                    unicornhat.set_pixel(x, y, r, g, b)
            unicornhat.show()

    def lights(self):
        pass

    def inbox_item_received(self, inbox_item):
        pass


class DotsMode(UnicornHatMode):
    def lights(self):
        with _lock:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            r = random.randint(1, 255)
            g = random.randint(1, 255)
            b = random.randint(1, 255)
            _buffer[x][y] = (r, g, b)
            unicornhat.set_pixel(x, y, r, g, b)
            unicornhat.show()
        time.sleep(2)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        with _lock:
            x = random.randint(0, 7)
            y = random.randint(0, 7)
            r = random.randint(1, 255)
            g = random.randint(1, 255)
            b = random.randint(1, 255)
            _buffer[x][y] = (r, g, b)
            unicornhat.set_pixel(x, y, r, g, b)
            unicornhat.show()


class FlashMode(UnicornHatMode):
    def lights(self):

        with _lock:
            r = random.randint(1, 255)
            g = random.randint(1, 255)
            b = random.randint(1, 255)
            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = (r, g, b)
            _WriteAll()
        time.sleep(2)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        with _lock:
            r = random.randint(1, 255)
            g = random.randint(1, 255)
            b = random.randint(1, 255)
            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = (r, g, b)
            _WriteAll()


class RainMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain()

    def lights(self):
        with _lock:
            self._rain.WriteToBuffer(True)
            _WriteAll()
        time.sleep(0.25)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (0, 0, 255)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _WriteAll()


class MatrixMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain(direction="right")

    def lights(self):
        with _lock:
            self._rain.WriteToBuffer(True)
            _WriteAll()
        time.sleep(0.5)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (0, 255, 0)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _WriteAll()


class FireMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain(direction="up")

    def lights(self):
        with _lock:
            self._rain.WriteToBuffer(True)
            _WriteAll()
        time.sleep(0.4)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        r = random.randint(100, 255)
        g = random.randint(0, 150)
        b = 0
        rgb = (r, g, b)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _WriteAll()


class SnowMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain()

    def lights(self):
        with _lock:
            self._rain.WriteToBuffer(True)
            _WriteAll()
        time.sleep(2)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (255, 255, 255)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _WriteAll()


class Rain(object):
    def __init__(self, direction="down"):
        self._direction = direction
        self._raindrops = []

    def AddRaindrop(self, rgb):
        if self._direction == "up":
            x = random.randint(0, 7)
            y = 0
        elif self._direction == "down":
            x = random.randint(0, 7)
            y = 7
        elif self._direction == "left":
            x = 0
            y = random.randint(0, 7)
        elif self._direction == "right":
            x = 7
            y = random.randint(0, 7)
        else:
            raise Exception("Invalid direction")
        self._raindrops.append(Raindrop(x, y, rgb))

    def WriteToBuffer(self, iterate):
        if iterate:
            for r in self._raindrops:
                _buffer[r.x][r.y] = (0, 0, 0)
            self.Iterate()

        for r in self._raindrops:
            _buffer[r.x][r.y] = r.rgb

    def Iterate(self):
        for r in self._raindrops:
            if self._direction == "up":
                r.y += 1
            elif self._direction == "down":
                r.y -= 1
            elif self._direction == "left":
                r.x += 1
            elif self._direction == "right":
                r.x -= 1

            if self._direction == "up" and r.y > 7 \
                    or self._direction == "down" and r.y < 0 \
                    or self._direction == "left" and r.x > 7 \
                    or self._direction == "right" and r.x < 0:
                self._raindrops.remove(r)


class Raindrop(object):
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb


def hsv2rgb(hsv):
    rgb = [int(x * 255) for x in colorsys.hsv_to_rgb(hsv[0], hsv[1], hsv[2])]
    return rgb


class RainbowMode(UnicornHatMode):
    def __init__(self):
        self.state = False

    def lights(self):
        self.state = not self.state
        if self.state:
            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = ((1.0 / 8) * x, (1.0 / 8) * y, 1.0)
        else:
            for y in range(8):
                for x in range(8):
                    _buffer[x][y] = ((1.0 / 8) * x, 1.0, (1.0 / 8) * y)
        _WriteAll()
        time.sleep(0.25)


class RainbowRainMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain()
        self.h = 0.0

    def lights(self):
        with _lock:
            self._rain.WriteToBuffer(True)
            _WriteAll()
        time.sleep(0.25)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h += 0.1
        if self.h > 1.0:
            self.h = 0.0
        self._rain.AddRaindrop(hsv2rgb((self.h, 1.0, 1.0)))
        self._rain.WriteToBuffer(False)
        _WriteAll()


_buffer = [[(0, 0, 0) for x in range(8)] for y in range(8)]
_modes = itertools.cycle([
    # DotsMode(),
    # FlashMode(),
    # SnowMode(),
    # RainMode(),
    # FireMode(),
    # MatrixMode(),
    RainbowMode(),
    RainbowRainMode(),

    # TODO
    # Rain
    # matrix
    # Fire
    # bubbles
    # Fireworks
    # Sin Wave
    # Swipes
    # graphic equalizer
    # starfield

    # bouncing ball/line

    # snake
    # game of life
    # battleships
    # chess/draughts

    # strobe
    # lifts?
    # text/numbers
    # emoticons
    # graphs
    # random/noise
    # images / video / gifs
])
_mode = next(_modes)

_lock = Lock()


def Lights():
    _mode.lights()


def CameraFlash(on):
    _mode.camera_flash(on)


def inbox_item_received(inbox_item):
    _mode.inbox_item_received(inbox_item)


def OnLightsScheduledTask():
    with _lock:
        global _mode
        _mode = next(_modes)


def Fade():
    _mode.fade()


def Close():
    _mode.close()
