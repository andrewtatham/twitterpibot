import logging
import random

from colorama import Fore, Style, Back
from twython import TwythonError

from twitterpibot.data_access import dal
import twitterpibot.hardware
from twitterpibot.logic import textonanimage, imagemanager
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet

logger = logging.getLogger(__name__)


# twython.exceptions.TwythonRateLimitError: Twitter API returned a 429 (Too Many Requests), Rate limit exceeded
# TwythonError: HTTPSConnectionPool(host='http://api.twitter.com ', port=443): Read timed out. (read timeout=None)
# TwythonError: ('Connection aborted.', error(110, 'Connection timed out'))


def handle_silently(exception):
    _record_warning(None, exception)


def handle(identity, exception, label=None):
    if type(exception) is UnicodeEncodeError:
        _record_warning(identity, exception, label)
    elif type(exception) is TwythonError:
        _record_warning(identity, exception, label)
    else:
        _record_error(identity, exception, label)


def _record_warning(identity, exception):
    logger.warning(Style.DIM + Fore.BLACK + Back.YELLOW + str(exception))
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
        _try_send_exception(identity, exception)


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
        if identity and twitterpibot.hardware.is_linux:
            image = imagemanager.get_image(topics=topics)
            path = textonanimage.put_text_on_an_image(image, exception=exception)
            identity.twitter.send(OutgoingTweet(
                text="@" + identity.admin_screen_name + " " + str(exception),
                file_paths=[path]))
            # identity.twitter.send(OutgoingDirectMessage(text=traceback.format_exc()))
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
