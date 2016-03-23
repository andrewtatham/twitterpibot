import re
import random

from twitterpibot.responses.Response import Response


class ThanksResponse(Response):
    def __init__(self, identity):
        Response.__init__(self, identity)
        self.rx = re.compile("thx|thank(s|you)", re.IGNORECASE)

    def condition(self, inbox_item):
        return mentioned_reply_condition(inbox_item) \
               and bool(self.rx.match(inbox_item.text))

    def respond(self, inbox_item):
        thanks = [
            "thx",
            "thanks",
            "thankyou",
            "thank u",
        ]
        self.identity.twitter.reply_with(inbox_item, random.choice(thanks) + " for the " + random.choice(thanks))
