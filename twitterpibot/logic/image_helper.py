import colorsys
import random

__author__ = 'andrewtatham'
_maxbright = 255


def rectangle(origin, size):
    return origin + tuple(map(sum, zip(origin, size)))


def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    return h, s, v


def limit(min_val, val, max_val):
    return max(min_val, min(val, max_val))


def hsv_to_rgb(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = limit(0, int(r), 255)
    g = limit(0, int(g), 255)
    b = limit(0, int(b), 255)
    return r, g, b


def get_random_hsv():
    h, s, v = (random.uniform(0.0, 1.0), 1.0, _maxbright)
    return h, s, v


def get_random_rgb():
    h, s, v = get_random_hsv()
    r, g, b = hsv_to_rgb(h, s, v)
    return r, g, b


if __name__ == '__main__':
    print(rgb_to_hsv(255, 0, 0))
    print(rgb_to_hsv(0, 255, 0))
    print(rgb_to_hsv(0, 0, 255))


def h_delta(h, delta):
    return (h + delta) % 1.0


def fade_rgb(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    # print("before fade: h = %s, s = %s, v = %s, r = %s, g = %s, b = %s" % (h, s, v, r, g, b))
    v = max(0, v / 3)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r, g, b = (int(round(x)) for x in (r, g, b))
    # print("after fade: h = %s, s = %s, v = %s, r = %s, g = %s, b = %s" % (h, s, v, r, g, b))
    return r, g, b
