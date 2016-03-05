import logging
import random
import time

from twython.streaming.api import TwythonStreamer

import twitterpibot.hardware
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingEvent import IncomingEvent
from twitterpibot.incoming.IncomingTweet import IncomingTweet
import twitterpibot.twitter.Authenticator as Authenticator

logger = logging.getLogger(__name__)

default_backoff = 30
max_backoff = 300


class MyStreamer(TwythonStreamer):
    def __init__(self, identity, topic=None, topic_name=None):
        self.backoff = default_backoff
        self.identity = identity
        self.responses = identity.get_responses()
        if not self.identity.tokens:
            self.identity.tokens = Authenticator.get_tokens(identity.screen_name)
        self._topic = topic
        if topic_name:
            self._topic_name = topic_name
        else:
            self._topic_name = topic
        super(MyStreamer, self).__init__(
            self.identity.tokens[0],
            self.identity.tokens[1],
            self.identity.tokens[2],
            self.identity.tokens[3]
        )

    def on_success(self, data):
        self.backoff = default_backoff
        if self._topic_name:
            data['tweet_source'] = "stream:" + self._topic_name
        inbox_item = self.create_inbox_item(data)
        if inbox_item:
            twitterpibot.hardware.on_inbox_item_received(inbox_item)
            responded = self.create_response(inbox_item)
            if not responded and random.randint(0, 9) == 0:
                inbox_item.display()

    def on_error(self, status_code, data):
        msg = "[%s] Error: %s %s" % (self.identity.screen_name, status_code, data)
        logger.error(msg)
        if status_code == 420:
            if self.connected:
                logger.info("[%s] disconnecting" % self.identity.screen_name)
                self.disconnect()
            logger.info("[%s] sleeping for %s" % (self.identity.screen_name, self.backoff))
            time.sleep(self.backoff)
            self.backoff = min(self.backoff * 2, max_backoff)

    def create_inbox_item(self, data):

        if "text" in data:
            tweet = IncomingTweet(data, self.identity)
            self.identity.statistics.record_incoming_tweet(tweet)
            return tweet
        elif "direct_message" in data:
            dm = IncomingDirectMessage(data, self.identity)
            self.identity.statistics.record_incoming_direct_message(dm)
            return dm
        elif "event" in data:
            event = IncomingEvent(data, self.identity)
            self.identity.statistics.record_incoming_event(event)
            return event
        elif "friends" in data:
            logger.debug("[%s] Following %s" % (self.identity.screen_name, data["friends"]))
            self.identity.following = set([str(f) for f in data["friends"]])
            self.identity.statistics.record_connection()
            logger.info("[%s] Connected" % self.identity.screen_name)
        else:
            logger.debug(data)

    def create_response(self, inbox_item):
        if inbox_item and self.responses:
            for response in self.responses:
                if response.condition(inbox_item):
                    self.identity.statistics.increment("Responses")
                    inbox_item.display()
                    response.respond(inbox_item)
                    return True
        return False
