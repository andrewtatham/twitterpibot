import re
import random

from twitterpibot.responses.Response import Response
from twitterpibot.twitter.TwitterHelper import reply_with


class ThanksResponse(Response):
    def __init__(self):
        self.rx = re.compile("thx|thank(s|you)", re.IGNORECASE)

    def condition(self, inbox_item):
        return super(ThanksResponse, self).condition(inbox_item) \
               and bool(self.rx.match(inbox_item.text))

    def respond(self, inbox_item):
        thanks = [
            "thx",
            "thanks",
            "thankyou",
            "thank u",
        ]
        reply_with(inbox_item, random.choice(thanks) + " for the " + random.choice(thanks))
