from twython.streaming.api import TwythonStreamer
import twitterpibot.MyQueues as MyQueues
import twitterpibot.twitter.Authenticator as Authenticator
import logging
# import time

logger = logging.getLogger(__name__)

_tokens = None


# _back_off_seconds = 60


class MyStreamer(TwythonStreamer):
    def __init__(self, screen_name=None, topic=None, topic_name=None):
        global _tokens
        if not _tokens:
            _tokens = Authenticator.get_tokens(screen_name)

        self._topic = topic

        if topic_name:
            self._topic_name = topic_name
        else:
            self._topic_name = topic

        super(MyStreamer, self).__init__(_tokens[0], _tokens[1], _tokens[2], _tokens[3])

    def on_success(self, data):
        # global _back_off_seconds
        if self._topic_name:
            data['tweet_source'] = "stream:" + self._topic_name
        MyQueues.inbox.put(data)
        # _back_off = 60

    def on_error(self, status_code, data):
        # global _back_off_seconds
        msg = str(status_code) + " " + str(data)
        logger.error(msg)

        # if status_code == 420:
        #     logger.warn("backing off for " + str(_back_off) + " seconds")
        #
        #     time.sleep(_back_off)
        #     _back_off *= 2

    @property
    def topic(self):
        return self._topic
