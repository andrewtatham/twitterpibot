import re
import random
from twitterpibot.processing.Conversational import HelloWords

from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class HelloResponse(Response):
    def __init__(self):

        self.rx = re.compile("|".join(HelloWords), re.IGNORECASE)

    def condition(self, inbox_item):
        return super(HelloResponse, self).reply_condition(inbox_item) \
               and bool(self.rx.match(inbox_item.text))

    def respond(self, inbox_item):
        reply_with(inbox_item, random.choice(HelloWords))
