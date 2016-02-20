import logging
import traceback

from colorama import Fore, Style, Back

from twython import TwythonError

import twitterpibot.Statistics
from twitterpibot.hardware import hardware

from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage

logger = logging.getLogger(__name__)


# twython.exceptions.TwythonRateLimitError: Twitter API returned a 429 (Too Many Requests), Rate limit exceeded
# TwythonError: HTTPSConnectionPool(host='http://api.twitter.com ', port=443): Read timed out. (read timeout=None)
# TwythonError: ('Connection aborted.', error(110, 'Connection timed out'))


def handle_silently(exception):
    _record_warning(exception)


def handle(identity, exception):
    if type(exception) is UnicodeEncodeError:
        _record_warning(exception)
    elif type(exception) is TwythonError:
        _record_warning(exception)
    else:
        _record_error(identity, exception)


def _record_warning(exception):
    print(Style.DIM + Fore.BLACK + Back.YELLOW + str(exception))
    logger.warn(exception)
    twitterpibot.Statistics.record_warning()


def _record_error(identity, exception):
    print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logger.exception(exception)
    twitterpibot.Statistics.record_error()
    _try_send_exception(identity)


def _try_send_exception(identity):
    try:
        if hardware.is_linux:
            identity.twitter.send(OutgoingDirectMessage(text=traceback.format_exc()))
    except Exception as e:
        logger.exception(e)
