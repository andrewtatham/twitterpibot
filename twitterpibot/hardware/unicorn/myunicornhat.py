import itertools
import random

from twitterpibot.hardware.myhardware import is_linux
from twitterpibot.hardware.unicorn.canvas import Buffer
from twitterpibot.hardware.unicorn.myunicornhatmodes import *
from twitterpibot.incoming.IncomingTweet import IncomingTweet

if is_linux:
    import unicornhat

    unicornhat.rotation(270)
else:
    from twitterpibot.hardware.unicorn import unicornhat_viz as unicornhat

_buffer = Buffer(8, 8)

# TODO unicorn hat patterns

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

_modes_list = [
    SnakeMode(_buffer),
    MultiSnakeMode(_buffer)
]
if myhardware.is_linux:
    _modes_list.extend([

        # SnowMode(_buffer),
        # MatrixModeLeft(_buffer),
        # RainMode(_buffer),
        # FireMode(_buffer),
        # MatrixModeRight(_buffer),
        RainbowRainMode(_buffer),

        RainbowFireworksMode(_buffer),
        RainbowSqaresMode(_buffer),

        BouncingBallMode(_buffer)


    ])



random.shuffle(_modes_list)
_modes = itertools.cycle(_modes_list)
_mode = next(_modes)


def lights():
    _mode.lights()


def camera_flash(on):
    _mode.camera_flash(on)


def inbox_item_received(inbox_item):
    _mode.inbox_item_received(inbox_item)


def on_lights_scheduled_task():
    _buffer._set_max_brightness()

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

        fade()
        lights()
        if i % 15 == 0 or random.randint(0, 3) == 0:
            inbox_item_received(None)
        if i % 50 == 0:
            on_lights_scheduled_task()

    close()
    if not is_linux:
        unicornhat.display()
