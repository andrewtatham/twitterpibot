import logging

from twitterpibot.responses.Response import Response
from twitterpibot.twitter import TwitterHelper

logger = logging.getLogger(__name__)


class RetweetResponse(Response):
    def condition(self, inbox_item):
        return super(RetweetResponse, self).retweet_condition(inbox_item)

    def respond(self, inbox_item):
        logger.info("retweeting status id %s", inbox_item.status_id)
        TwitterHelper.retweet(inbox_item.status_id)
