import logging
from MyTwitter import MyTwitter
from Authenticator import Authenticator
from twython.exceptions import TwythonError
import logging
from colorama import Fore, Style, Back
from TwitterHelper import Send
from Statistics import RecordWarning, RecordError

logging.basicConfig(filename='twitter.log',level=logging.INFO)

# "Twitter API returned a 429 (Too Many Requests), Rate limit exceeded"
# "Twitter API returned a 403 (Forbidden), There was an error sending your message: Whoops! You already said that."


def HandleSilently(exception):
    _RecordWarning(exception)

def Handle(exception):
    if type(exception) is UnicodeEncodeError:
        _RecordWarning(exception)
    else:
        _RecordError(exception)


def _RecordWarning(exception):
    print(Style.DIM + Fore.WHITE + Back.YELLOW + str(exception.message))
    logging.warn(exception) 
    RecordWarning()

def _RecordError(exception):
    print(Style.BRIGHT + Fore.WHITE + Back.RED + str(exception))
    logging.exception(exception)
    RecordError()
    _TrySendException(exception)

def _TrySendException(exception):
    try:
        Send(
            text = str(exception),
            screen_name = "andrewtatham", 
            user_id = "19201332")
    except Exception as e:
        pass
