import colorsys

__author__ = 'andrewtatham'


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
