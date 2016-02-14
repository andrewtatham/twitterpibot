import logging

from twython.streaming.api import TwythonStreamer

from twitterpibot.Statistics import record_incoming_direct_message, record_incoming_tweet
from twitterpibot.hardware import hardware
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingEvent import IncomingEvent
from twitterpibot.incoming.IncomingTweet import IncomingTweet
import twitterpibot.twitter.Authenticator as Authenticator

logger = logging.getLogger(__name__)


class MyStreamer(TwythonStreamer):
    def __init__(self, identity, topic=None, topic_name=None):
        self.identity = identity
        self.responses = identity.get_responses()
        if not self.identity.tokens:
            self.identity.tokens = Authenticator.get_tokens(identity.screen_name)
        self._topic = topic
        if topic_name:
            self._topic_name = topic_name
        else:
            self._topic_name = topic
        super(MyStreamer, self).__init__(self.identity.tokens[0], self.identity.tokens[1], self.identity.tokens[2],
                                         self.identity.tokens[3])

    def on_success(self, data):
        if self._topic_name:
            data['tweet_source'] = "stream:" + self._topic_name
        inbox_item = self.create_inbox_item(data)
        if inbox_item:
            inbox_item.display()
            hardware.on_inbox_item_received(inbox_item)
            self.create_response(inbox_item)

    def on_error(self, status_code, data):
        msg = str(status_code) + " " + str(data)
        logger.error(msg)

    def create_inbox_item(self, data):

        if "text" in data:
            record_incoming_tweet()
            return IncomingTweet(data, self.identity)
        elif "direct_message" in data:
            record_incoming_direct_message()
            return IncomingDirectMessage(data, self.identity)
        elif "event" in data:
            return IncomingEvent(data, self.identity)
        elif "friends" in data:
            logger.info("Connected..." + self.identity.screen_name)
        else:
            logger.debug(data)

    def create_response(self, inbox_item):
        if inbox_item and self.responses:
            for response in self.responses:
                if response.condition(inbox_item):
                    response.respond(inbox_item)
                    break
