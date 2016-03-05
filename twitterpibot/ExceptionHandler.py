import logging
import traceback

from colorama import Fore, Style, Back
from twython import TwythonError

import twitterpibot.Statistics
import twitterpibot.hardware
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage

logger = logging.getLogger(__name__)


# twython.exceptions.TwythonRateLimitError: Twitter API returned a 429 (Too Many Requests), Rate limit exceeded
# TwythonError: HTTPSConnectionPool(host='http://api.twitter.com ', port=443): Read timed out. (read timeout=None)
# TwythonError: ('Connection aborted.', error(110, 'Connection timed out'))


def handle_silently(exception):
    _record_warning(None, exception)


def handle(identity, exception):
    if type(exception) is UnicodeEncodeError:
        _record_warning(identity, exception)
    elif type(exception) is TwythonError:
        _record_warning(identity, exception)
    else:
        _record_error(identity, exception)


def _record_warning(identity, exception):
    print(Style.DIM + Fore.BLACK + Back.YELLOW + str(exception))
    logger.warn(exception)
    if identity:
        identity.statistics.record_warning()


def _record_error(identity, exception):
    print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logger.exception(exception)
    if identity:
        identity.statistics.record_error()
        _try_send_exception(identity)


def _try_send_exception(identity):
    try:
        if identity and twitterpibot.hardware.is_linux:
            identity.twitter.send(OutgoingDirectMessage(text=traceback.format_exc()))
    except Exception as e:
        logger.exception(e)
