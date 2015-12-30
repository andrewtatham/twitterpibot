import logging

from colorama import Fore, Style, Back
from twython import TwythonError

from twitterpibot.Statistics import record_warning, record_error
from twitterpibot.twitter.TwitterHelper import send
from twitterpibot.hardware import hardware
import time
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
import traceback

logger = logging.getLogger(__name__)

# twython.exceptions.TwythonRateLimitError: Twitter API returned a 429 (Too Many Requests), Rate limit exceeded
# TwythonError: HTTPSConnectionPool(host='http://api.twitter.com ', port=443): Read timed out. (read timeout=None)
# TwythonError: ('Connection aborted.', error(110, 'Connection timed out'))

_back_off_default = 2
_back_off_seconds = _back_off_default


def handle_silently(exception):
    _record_warning(exception)


def handle(exception):
    if type(exception) is UnicodeEncodeError:
        _record_warning(exception)
    elif type(exception) is TwythonError:
        _record_warning(exception)
    else:
        _record_error(exception)


def _record_warning(exception):
    print(Style.DIM + Fore.BLACK + Back.YELLOW + str(exception))
    logger.warn(exception)
    record_warning()


def _record_error(exception):
    print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logger.exception(exception)
    record_error()
    _try_send_exception()


def _try_send_exception():
    global _back_off_seconds
    try:
        if hardware.is_linux:
            send(OutgoingDirectMessage(text=traceback.format_exc()))
            _back_off_seconds = _back_off_default
    except Exception as e:
        logger.exception(e)
        _back_off_seconds()


def _back_off():
    global _back_off_seconds
    time.sleep(_back_off_seconds)
    _back_off_seconds = min(9000, _back_off_seconds * 2)
