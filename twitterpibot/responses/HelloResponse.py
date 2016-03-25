import re
import random

from twitterpibot.logic.conversation import HelloWords
from twitterpibot.responses.Response import Response, mentioned_reply_condition


class HelloResponse(Response):
    def __init__(self, identity):
        Response.__init__(self, identity)
        self.rx = re.compile("|".join(HelloWords), re.IGNORECASE)

    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item) \
               and bool(self.rx.match(inbox_item.text))

    def respond(self, inbox_item):
        self.identity.twitter.reply_with(inbox_item, random.choice(HelloWords))
