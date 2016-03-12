import random

from twitterpibot.processing import FatherTed
from twitterpibot.responses.Response import Response


class FatherTedResponse(Response):
    def condition(self, inbox_item):
        return super(FatherTedResponse, self).mentioned_reply_condition(inbox_item)

    def respond(self, inbox_item):
        response = random.choice(FatherTed.responses)
        self.identity.twitter.reply_with(inbox_item, response)
