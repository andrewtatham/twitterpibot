import itertools
import random
import time

from twitterpibot.hardware import myhardware
from twitterpibot.logic import image_helper, astronomy

if myhardware.is_linux:
    import unicornhat
else:
    from twitterpibot.hardware import unicornhat_viz as unicornhat

max_bright = 255


def _write_pixel(x, y):
    pixel = _buffer[x][y]
    r = int(pixel[0])
    g = int(pixel[1])
    b = int(pixel[2])
    unicornhat.set_pixel(x, y, r, g, b)


def _write_all():
    for y in range(8):
        for x in range(8):
            _write_pixel(x, y)
    unicornhat.show()


def _sleep(seconds):
    if myhardware.is_linux:
        time.sleep(seconds)


class UnicornHatMode(object):
    def camera_flash(self, on):

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

        for y in range(8):
            for x in range(8):
                r, g, b = _buffer[x][y]
                r, g, b = image_helper.fade_rgb(r, g, b)
                _buffer[x][y] = (r, g, b)
                unicornhat.set_pixel(x, y, r, g, b)
        unicornhat.show()

    def close(self):

        r = 0
        g = 0
        b = 0
        for y in range(8):
            for x in range(8):
                unicornhat.set_pixel(x, y, r, g, b)
        unicornhat.show()

    def lights(self):
        _sleep(10)

    def inbox_item_received(self, inbox_item):
        pass


class DotsMode(UnicornHatMode):
    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        x = random.randint(0, 7)
        y = random.randint(0, 7)
        r, g, b = image_helper.get_random_rgb()
        _buffer[x][y] = (r, g, b)
        unicornhat.set_pixel(x, y, r, g, b)
        unicornhat.show()


class FlashMode(UnicornHatMode):
    def __init__(self):
        self.h = 0

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h = image_helper.h_delta(self.h, 1 / 16)
        for y in range(8):
            for x in range(8):
                rgb = image_helper.hsv_to_rgb(image_helper.h_delta(self.h, x / 16 + y / 32), 1.0, max_bright)
                _buffer[x][y] = rgb
        _write_all()


class RainMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain()

    def lights(self):
        self._rain.WriteToBuffer(True)
        _write_all()
        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (0, 0, max_bright)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _write_all()


class MatrixMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain(direction="right")

    def lights(self):
        self._rain.WriteToBuffer(True)
        _write_all()

        _sleep(0.1)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (0, max_bright, 0)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _write_all()


class FireMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain(direction="up")

    def lights(self):
        self._rain.WriteToBuffer(True)
        _write_all()
        _sleep(0.4)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        r = random.randint(max_bright, 2 * max_bright)
        g = random.randint(0, max_bright)
        b = 0
        rgb = (r, g, b)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _write_all()


class SnowMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain()

    def lights(self):
        self._rain.WriteToBuffer(True)
        _write_all()
        _sleep(0.5)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        rgb = (max_bright, max_bright, max_bright)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _write_all()


class Rain(object):
    def __init__(self, direction="down"):
        self._direction = direction
        self._raindrops = []

    def AddRaindrop(self, rgb):
        if self._direction == "up":
            x = 0
            y = random.randint(0, 7)
        elif self._direction == "right":
            x = random.randint(0, 7)
            y = 0
        elif self._direction == "down":
            x = 7
            y = random.randint(0, 7)
        elif self._direction == "left":
            x = random.randint(0, 7)
            y = 7
        else:
            raise Exception("Invalid direction")
        self._raindrops.append(Raindrop(x, y, rgb))

    def WriteToBuffer(self, iterate):
        if iterate:
            # for r in self._raindrops:
            #     _buffer[r.x][r.y] = (0, 0, 0)
            self.Iterate()

        for r in self._raindrops:
            _buffer[r.x][r.y] = r.rgb

    def Iterate(self):
        for r in self._raindrops:
            if self._direction == "up":
                r.x += 1
            elif self._direction == "right":
                r.y += 1
            elif self._direction == "down":
                r.x -= 1
            elif self._direction == "left":
                r.y -= 1

            if self._direction == "up" and r.x > 7 \
                    or self._direction == "right" and r.y > 7 \
                    or self._direction == "down" and r.x < 0 \
                    or self._direction == "left" and r.y < 0:
                self._raindrops.remove(r)


class Raindrop(object):
    def __init__(self, x, y, rgb):
        self.x = x
        self.y = y
        self.rgb = rgb


class RainbowMode(UnicornHatMode):
    def __init__(self):
        self.h = 0

    def lights(self):
        self.h = image_helper.h_delta(self.h, 0.05)

        for y in range(8):
            for x in range(8):
                h, s, v = (image_helper.h_delta(self.h, 0.1 * x / 8 + 0.2 * y / 8), 1.0, max_bright)
                rgb = image_helper.hsv_to_rgb(h, s, v)
                _buffer[x][y] = rgb

        _write_all()
        _sleep(0.25)


class RainbowRainMode(UnicornHatMode):
    def __init__(self):
        self._rain = Rain()
        self.h = 0.0

    def lights(self):
        self._rain.WriteToBuffer(True)
        _write_all()
        _sleep(0.5)

    # noinspection PyUnusedLocal
    def inbox_item_received(self, inbox_item):
        self.h = image_helper.h_delta(self.h, 0.05)
        h, s, v = (self.h, 1.0, max_bright)
        rgb = image_helper.hsv_to_rgb(h, s, v)
        self._rain.AddRaindrop(rgb)
        self._rain.WriteToBuffer(False)
        _write_all()


_buffer = [[(0, 0, 0) for x in range(8)] for y in range(8)]
_modes = itertools.cycle([
    DotsMode(),
    FlashMode(),
    SnowMode(),
    RainMode(),
    FireMode(),
    MatrixMode(),
    RainbowMode(),
    RainbowRainMode(),

    # TODO unicorn hat patterns
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


def lights():
    _mode.lights()


def camera_flash(on):
    _mode.camera_flash(on)


def inbox_item_received(inbox_item):
    _mode.inbox_item_received(inbox_item)

day_bright = 255
night_bright = 8
def on_lights_scheduled_task():
    global max_bright
    max_bright = night_bright + (day_bright - night_bright) * astronomy.get_daytimeness_factor()

    global _mode
    _mode = next(_modes)




def fade():
    _mode.fade()


def close():
    _mode.close()


if __name__ == '__main__':

    lights()
    for i in range(1000):
        print(i)
        if i % 4 == 0:
            fade()
        lights()
        if i % 15 == 0 or random.randint(0, 3) == 0:
            inbox_item_received(None)
        if i % 100 == 0:
            on_lights_scheduled_task()

    close()
    if not myhardware.is_linux:
        unicornhat.display()
