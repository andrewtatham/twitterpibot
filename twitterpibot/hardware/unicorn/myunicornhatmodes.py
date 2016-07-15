import random

import time

from twitterpibot.hardware import myhardware
from twitterpibot.hardware.unicorn import directions
from twitterpibot.hardware.unicorn.canvas import Rain, ParticleMode, Fireworks, Squares, BouncingBalls
from twitterpibot.hardware.unicorn.directions import Up, Right, Left
from twitterpibot.hardware.unicorn.games import SnakeGame
from twitterpibot.logic import image_helper


class UnicornHatMode(object):
    def __init__(self, buffer):
        self._buffer = buffer

    def camera_flash(self, on):
        self._buffer.camera_flash(on)

    def fade(self):
        self._buffer.fade()

    def close(self):
        self._buffer.clear()

    def lights(self):
        _sleep(10)

    def inbox_item_received(self, inbox_item):
        pass


class RainMode(UnicornHatMode):
    def __init__(self, buffer):
        super(RainMode, self).__init__(buffer)
        self._rain = Rain(buffer, trails=True)

    def lights(self):
        self._rain.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        h, s, v = (random.uniform(3 / 6, 4 / 6), 1.0, self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._rain.add_particle(rgb)


class MatrixModeRight(UnicornHatMode):
    def __init__(self, buffer):
        super(MatrixModeRight, self).__init__(buffer)
        self._rain = Rain(buffer, direction=Right(), trails=True)

    def lights(self):
        self._rain.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        h, s, v = (1 / 3, random.uniform(0.5, 1.0), self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._rain.add_particle(rgb)


class MatrixModeLeft(UnicornHatMode):
    def __init__(self, buffer):
        super(MatrixModeLeft, self).__init__(buffer)
        self._rain = Rain(buffer, direction=Left(), trails=True)

    def lights(self):
        self._rain.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        h, s, v = (1 / 3, random.uniform(0.5, 1.0), self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._rain.add_particle(rgb)


class FireMode(UnicornHatMode):
    def __init__(self, buffer):
        super(FireMode, self).__init__(buffer)
        self._rain = Rain(buffer, direction=Up(), trails=True)

    def lights(self):
        self._rain.WriteToBuffer(True)
        _sleep(0.2)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        h, s, v = (random.uniform(0, 1 / 6) - random.uniform(0, 1 / 12), 1.0, self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._rain.add_particle(rgb)


class SnowMode(UnicornHatMode):
    def __init__(self, buffer):
        super(SnowMode, self).__init__(buffer)
        self._rain = Rain(buffer)

    def lights(self):
        self._rain.WriteToBuffer(True)
        _sleep(0.3)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (self._buffer.max_bright, self._buffer.max_bright, self._buffer.max_bright)
        self._rain.add_particle(rgb)


class RainbowRainMode(UnicornHatMode):
    def __init__(self, buffer):
        super(RainbowRainMode, self).__init__(buffer)
        self._rain = Rain(buffer, direction=random.choice(directions.DIAGONALS), trails=True)
        self.h = 0.0

    def lights(self):
        self._rain.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h = image_helper.h_delta(self.h, 0.05)
        h, s, v = (self.h, 1.0, self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._rain.add_particle(rgb)


class RainbowFireworksMode(UnicornHatMode):
    def __init__(self, buffer):
        super(RainbowFireworksMode, self).__init__(buffer)
        self._particles = Fireworks(buffer)
        self.h = 0.0

    def lights(self):
        self._particles.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h = image_helper.h_delta(self.h, 0.05)
        h, s, v = (self.h, 1.0, self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._particles.add_particle(rgb)


class RainbowSqaresMode(UnicornHatMode):
    def __init__(self, buffer):
        super(RainbowSqaresMode, self).__init__(buffer)
        self._particles = Squares(buffer)
        self.h = 0.0

    def lights(self):
        self._particles.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h = image_helper.h_delta(self.h, 0.05)
        h, s, v = (self.h, 1.0, self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._particles.add_particle(rgb)


class BouncingBallMode(UnicornHatMode):
    def __init__(self, buffer):
        super(BouncingBallMode, self).__init__(buffer)
        self._particles = BouncingBalls(buffer)
        self.h = 0.0

    def lights(self):
        self._particles.WriteToBuffer(True)
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h = image_helper.h_delta(self.h, 0.05)
        hsv = (self.h, 1.0, self._buffer.max_bright)
        rgb = image_helper.hsv_to_rgb_alt(hsv)
        self._particles.add_particle(rgb)


class SnakeMode(UnicornHatMode):
    def __init__(self, buffer):
        super(SnakeMode, self).__init__(buffer)
        self._game = SnakeGame(buffer)

    def lights(self):
        self._game.iterate()
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        if inbox_item and inbox_item.has_media or myhardware.is_andrew_macbook:
            self._game.add_food()


def _sleep(seconds):
    if myhardware.is_linux:
        time.sleep(seconds)
