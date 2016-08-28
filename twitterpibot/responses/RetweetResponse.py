import logging
import random

from twitterpibot.logic import conversation
from twitterpibot.responses.Response import Response, retweet_condition, _one_in

logger = logging.getLogger(__name__)


class RetweetResponse(Response):
    def condition(self, inbox_item):
        return retweet_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("retweeting status id %s", inbox_item.id_str)
        if _one_in(10):
            self.identity.twitter.quote_tweet(inbox_item=inbox_item, text=conversation.segue())
        else:
            self.identity.twitter.retweet(inbox_item.id_str)
