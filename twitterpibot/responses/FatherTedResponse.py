from twitterpibot.processing import FatherTed
from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with
import random


class FatherTedResponse(Response):
    def condition(self, inbox_item):
        return super(FatherTedResponse, self).condition(inbox_item)

    def respond(self, inbox_item):
        response = random.choice(FatherTed.responses)
        reply_with(inbox_item, response)
