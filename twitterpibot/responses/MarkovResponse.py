import logging

from twitterpibot.logic import markovhelper
from twitterpibot.responses.Response import Response, mentioned_reply_condition

logger = logging.getLogger(__name__)


class MarkovResponse(Response):
    def __init__(self, identity, text):
        Response.__init__(self, identity)
        self.markov = markovhelper.get(" ".join(text))
        for i in range(5):
            logger.info(self.markov.speak())

    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item)

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(inbox_item=inbox_item, text=self.markov.speak())
