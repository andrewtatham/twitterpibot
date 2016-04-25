from http.client import IncompleteRead
import logging
import random
import traceback

from colorama import Fore, Style, Back
from requests.exceptions import ChunkedEncodingError

from twython import TwythonError

import twitterpibot.hardware.myhardware
from twitterpibot.data_access import dal
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage

logger = logging.getLogger(__name__)


def handle_silently(exception, label=None):
    _record_warning(None, exception, label)


def is_timeout(exception):
    """Return True if we should retry"""
    return "timed out" in str(exception) \
           or "Connection broken: IncompleteRead" in str(exception)


def handle(identity, exception, label=None):
    if type(exception) is UnicodeEncodeError or type(exception) is TwythonError \
            or type(exception) is IncompleteRead or type(exception) is ChunkedEncodingError:
        _record_warning(identity, exception, label)
    else:
        _record_error(identity, exception, label)


def _record_warning(identity, exception, label):
    logger.warning(Fore.BLACK + Back.YELLOW + str(exception))
    logger.exception(Style.RESET_ALL)
    dal.warning(identity, exception, label)
    if identity:
        identity.statistics.record_warning()


def _record_error(identity, exception, label):
    logger.exception(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logger.exception(Style.RESET_ALL)
    dal.exception(identity, exception, label)
    if identity:
        identity.statistics.record_error()
        # _try_send_exception(identity, exception)


topics = [
    "sunset",
    "beach",
    "forest",
    "desert",
    "jungle",
    "kitten",
    "kittens",
    "puppy",
    "puppies",
    "goat",
    "goats"
]


def _try_send_exception(identity, exception):
    try:
        # if identity and twitterpibot.hardware.is_mac_osx:
        if identity and twitterpibot.hardware.myhardware.is_linux:
            # image = imagemanager.get_image(topics=topics)
            # path = textonanimage.put_text_on_an_image(image, exception=exception)
            # identity.twitter.send(OutgoingTweet(
            #     text="@" + identity.admin_screen_name + " " + str(exception),
            #     file_paths=[path]))

            identity.twitter.send(OutgoingDirectMessage(text=traceback.format_exc()))
    except Exception as e:
        logger.exception(e)


def _foo(levels, level):
    if level <= levels:
        _foo(levels, level + 1)
    else:
        raise Exception("bar")


def raise_test_exception(levels=None):
    if not levels:
        levels = random.randint(2, 12)
    _foo(levels, 0)


def test_exception_handling():
    try:
        raise_test_exception()
    except Exception as ex:
        handle(None, ex, label="test_exception_handling")


if __name__ == '__main__':
    test_exception_handling()
