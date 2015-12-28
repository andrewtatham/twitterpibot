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

# "Twitter API returned a 429 (Too Many Requests), Rate limit exceeded"
# "Twitter API returned a 403 (Forbidden), There was an error sending your message: Whoops! You already said that."
# TwythonError: HTTPSConnectionPool(host='http://api.twitter.com ', port=443): Read timed out. (read timeout=None)
# TwythonError: ('Connection aborted.', error(110, 'Connection timed out'))
_back_off = 15


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
    print(Style.DIM + Fore.WHITE + Back.YELLOW + str(exception.message))
    logger.warn(exception)
    record_warning()


def _record_error(exception):
    print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logger.exception(exception)
    record_error()
    _try_send_exception()


def _try_send_exception():
    global _back_off
    try:
        if hardware.is_linux:
            send(OutgoingDirectMessage(text=traceback.format_exc()))
            _back_off = 15
    except Exception as e:
        logger.exception(e)
        time.sleep(_back_off)
        _back_off *= 2
