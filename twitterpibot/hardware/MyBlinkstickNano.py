import itertools
import time

from blinkstick import blinkstick

from twitterpibot.logic import image_helper

_leds = itertools.cycle(range(2))
_led = next(_leds)


class BlinkstickNanoMode(object):
    def camera_flash(self, on):

        for led in range(2):
            if on:
                _blinkstick.set_color(channel=0, index=led, red=255, green=255, blue=255)
            else:
                _blinkstick.set_color(channel=0, index=led, red=0, green=0, blue=0)

    def fade(self):

        for led in range(2):
            r, g, b = _blinkstick.get_color(led)
            r, g, b = image_helper.fade_rgb(r, g, b)

            _blinkstick.set_color(channel=0, index=led, red=r, green=g, blue=b)

    def close(self):

        for led in range(2):
            _blinkstick.set_color(channel=0, index=led, red=0, green=0, blue=0)
        _blinkstick.turn_off()

    def lights(self):
        time.sleep(1)

    def inbox_item_received(self, inbox_item):
        pass


class AlternateMode(BlinkstickNanoMode):
    def lights(self):
        global _led
        r, g, b = image_helper.get_random_rgb()

        _blinkstick.set_color(channel=0, index=_led, red=r, green=g, blue=b)
        _led = next(_leds)
        time.sleep(1)

    def inbox_item_received(self, inbox_item):
        global _led
        r, g, b = image_helper.get_random_rgb()
        _blinkstick.set_color(channel=0, index=_led, red=r, green=g, blue=b)
        _led = next(_leds)


class BothMode(BlinkstickNanoMode):
    def inbox_item_received(self, inbox_item):
        r, g, b = image_helper.get_random_rgb()

        for led in range(2):
            _blinkstick.set_color(channel=0, index=led, red=r, green=g, blue=b)

    def lights(self):
        r, g, b = image_helper.get_random_rgb()

        for led in range(2):
            _blinkstick.set_color(channel=0, index=led, red=r, green=g, blue=b)
        time.sleep(1)


_blinkstick = blinkstick.find_first()

for led in range(2):
    _blinkstick.set_color(channel=0, index=led, red=0, green=0, blue=0)

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
    global _mode
    _mode = next(_modes)


def fade():
    _mode.fade()


def close():
    _mode.close()


if __name__ == '__main__':
    lights()
    for i in range(60):
        if i % 4 == 0:
            lights()
        if i % 15 == 0:
            inbox_item_received(None)
        if i % 20 == 0:
            on_lights_scheduled_task()
        fade()

        print(i)

    close()
