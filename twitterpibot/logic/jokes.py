import html
import random

from pyjokes import pyjokes

from twitterpibot.logic import urlhelper

__author__ = 'andrewtatham'


def _get_chuck_norris_joke():
    response = urlhelper.get_response("http://api.icndb.com/jokes/random")
    if response["type"] == "success":
        return html.unescape(response["value"]["joke"])


if __name__ == '__main__':
    print(_get_chuck_norris_joke())


def get_joke():
    joke = None
    if random.randint(0, 10) == 0:
        joke = _get_chuck_norris_joke()
    if not joke:
        joke = pyjokes.get_joke()
    return joke
