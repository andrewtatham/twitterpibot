import logging
import random
import time

from twython.streaming.api import TwythonStreamer

from twitterpibot import hardware
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingEvent import IncomingEvent
from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.twitter import authorisationhelper

logger = logging.getLogger(__name__)

default_backoff = 30
max_backoff = 600


class Streamer(TwythonStreamer):
    def __init__(self, identity, topic=None, topic_name=None, responses=None, filter_level=None):
        self.backoff = default_backoff
        self._identity = identity

        if not responses:
            self.responses = self._identity.get_responses()
        else:
            self.responses = responses
        if not self._identity.tokens:
            self._identity.tokens = authorisationhelper.get_tokens(identity.screen_name)
        self._topic = topic
        if topic_name:
            self._topic_name = topic_name
        else:
            self._topic_name = topic
        self._filter_level = filter_level
        super(Streamer, self).__init__(
            self._identity.tokens[0],
            self._identity.tokens[1],
            self._identity.tokens[2],
            self._identity.tokens[3]
        )

    def on_success(self, data):
        self.backoff = default_backoff
        if self._topic_name:
            data['tweet_source'] = "stream:" + self._topic_name
        inbox_item = self._create_inbox_item(data)
        if inbox_item:
            hardware.on_inbox_item_received(inbox_item)
            response = self._determine_response(inbox_item)
            if response:
                inbox_item.display()
            elif random.randint(0, 9) == 0:
                inbox_item.display()
            else:
                inbox_item.display()
            if response:
                self._respond(inbox_item=inbox_item, response=response)

    def on_error(self, status_code, data):
        msg = "[%s] Error: %s %s" % (self._identity.screen_name, status_code, data)
        logger.error(msg)
        if status_code == 420:
            if self.connected:
                logger.info("[%s] disconnecting" % self._identity.screen_name)
                self.disconnect()
            logger.info("[%s] sleeping for %s" % (self._identity.screen_name, self.backoff))
            time.sleep(self.backoff)
            self.backoff = min(self.backoff * 2, max_backoff)

    def _create_inbox_item(self, data):

        if "text" in data:
            tweet = IncomingTweet(data, self._identity)
            self._identity.statistics.record_incoming_tweet(tweet)
            return tweet
        elif "direct_message" in data:
            dm = IncomingDirectMessage(data, self._identity)
            self._identity.statistics.record_incoming_direct_message(dm)
            return dm
        elif "event" in data:
            event = IncomingEvent(data, self._identity)
            self._identity.statistics.record_incoming_event(event)
            return event
        elif "friends" in data:
            logger.debug("[%s] Following %s" % (self._identity.screen_name, data["friends"]))
            self._identity.following = set([str(f) for f in data["friends"]])
            self._identity.statistics.record_connection()
            logger.info("[%s] Connected" % self._identity.screen_name)
        else:
            logger.debug(data)

    def _determine_response(self, inbox_item):
        if inbox_item and self.responses:
            for response in self.responses:
                if response.condition(inbox_item):
                    return response
        return None

    def _respond(self, inbox_item, response):
        self._identity.statistics.increment("Responses")
        response.respond(inbox_item)
        return True
