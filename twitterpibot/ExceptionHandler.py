import logging

from colorama import Fore, Style, Back

from twitterpibot.Statistics import RecordWarning, RecordError
from twitterpibot.twitter.TwitterHelper import Send
from twitterpibot.hardware import hardware
import time

logger = logging.getLogger(__name__)

# "Twitter API returned a 429 (Too Many Requests), Rate limit exceeded"
# "Twitter API returned a 403 (Forbidden), There was an error sending your message: Whoops! You already said that."

backoff = 15


def HandleSilently(exception):
    _RecordWarning(exception)


def Handle(exception):
    if type(exception) is UnicodeEncodeError:
        _RecordWarning(exception)
    else:
        _RecordError(exception)


def _RecordWarning(exception):
    print(Style.DIM + Fore.WHITE + Back.YELLOW + str(exception.message))
    logger.warn(exception)
    RecordWarning()


def _RecordError(exception):
    print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logger.exception(exception)
    RecordError()
    _TrySendException()


def _TrySendException():
   
    try:
        if hardware.isRaspbian:
            Send(OutgoingDirectMessage(text = traceback.format_exc()))
    except Exception as e:
        logger.exception(e) 
        global backoff
        time.sleep(backoff)
        backoff *= 2
