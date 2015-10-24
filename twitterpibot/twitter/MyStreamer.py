from twython.streaming.api import TwythonStreamer
import twitterpibot.MyQueues as MyQueues
import Authenticator
import logging

logger = logging.getLogger(__name__)

_tokens = None


class MyStreamer(TwythonStreamer):
    def __init__(self, screen_name=None):
        global _tokens
        if not _tokens:
            _tokens = Authenticator.GetTokens(screen_name)
        super(MyStreamer, self).__init__(_tokens[0], _tokens[1], _tokens[2], _tokens[3])

    def on_success(self, data):
        MyQueues.inbox.put(data)

    def on_error(self, status_code, data):
        msg = str(status_code) + " " + str(data)
        logger.error(msg)
        print(msg)