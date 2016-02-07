import logging

from twitterpibot.logic import markovhelper
from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with

logger = logging.getLogger(__name__)


class MarkovResponse(Response):
    def __init__(self, text):
        self.markov = markovhelper.train(text)
        for i in range(5):
            logger.info(self.markov.speak())

    def condition(self, inbox_item):
        return super(MarkovResponse, self).reply_condition(inbox_item)

    def respond(self, inbox_item):
        reply_with(inbox_item=inbox_item, text=self.markov.speak())
