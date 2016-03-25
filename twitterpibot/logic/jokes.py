import random

from pyjokes import pyjokes

from twitterpibot.logic import urlhelper

__author__ = 'andrewtatham'


def _get_chuck_norris_joke():
    response = urlhelper.get_response("http://api.icndb.com/jokes/random")
    if response["type"] == "success":
        return response["value"]["joke"]


if __name__ == '__main__':
    print(_get_chuck_norris_joke())


def get_joke():
    if random.randint(0, 1) == 0:
        return pyjokes.get_joke()
    else:
        _get_chuck_norris_joke()
