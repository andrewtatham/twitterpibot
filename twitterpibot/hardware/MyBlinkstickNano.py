import random
from threading import Lock
import time
from blinkstick import blinkstick
import colorsys
import itertools

_leds = itertools.cycle(range(2))
_led = next(_leds)


class BlinkstickNanoMode(object):
    def camera_flash(self, on):
        with _lock:
            for led in range(2):
                if on:
                    _blinkstick.set_color(channel=0, index=led, red=255, green=255, blue=255)
                else:
                    _blinkstick.set_color(channel=0, index=led, red=0, green=0, blue=0)

    def fade(self):
        with _lock:
            for led in range(2):
                r, g, b = _blinkstick.get_color(led)
                h, s, v = colorsys.rgb_to_hsv(r, g, b)
                # print("before fade: h = %s, s = %s, v = %s, r = %s, g = %s, b = %s" % (h, s, v, r, g, b))
                v = max(0, v - 2)
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                r, g, b = (int(round(x)) for x in (r, g, b))
                # print("after fade: h = %s, s = %s, v = %s, r = %s, g = %s, b = %s" % (h, s, v, r, g, b))
                _blinkstick.set_color(channel=0, index=led, red=r, green=g, blue=b)

    def close(self):
        with _lock:
            for led in range(2):
                _blinkstick.set_color(channel=0, index=led, red=0, green=0, blue=0)
            _blinkstick.turn_off()

    def lights(self):
        time.sleep(1)

    def inbox_item_received(self, inbox_item):
        pass


class AlternateMode(BlinkstickNanoMode):
    def inbox_item_received(self, inbox_item):
        global _led
        r = random.randint(0, _maxbright)
        g = random.randint(0, _maxbright)
        b = random.randint(0, _maxbright)
        with _lock:
            _blinkstick.set_color(channel=0, index=_led, red=r, green=g, blue=b)
            _led = next(_leds)


class BothMode(BlinkstickNanoMode):
    def inbox_item_received(self, inbox_item):
        r = random.randint(0, _maxbright)
        g = random.randint(0, _maxbright)
        b = random.randint(0, _maxbright)
        with _lock:
            for led in range(2):
                _blinkstick.set_color(channel=0, index=led, red=r, green=g, blue=b)


_maxbright = 32
_blinkstick = blinkstick.find_first()

for led in range(2):
    _blinkstick.set_color(channel=0, index=led, red=0, green=0, blue=0)
_lock = Lock()

_modes = itertools.cycle([
    AlternateMode(),
    BothMode()
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
