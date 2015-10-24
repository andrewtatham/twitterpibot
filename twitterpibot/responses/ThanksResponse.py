import re
from Response import Response
import random
from twitterpibot.twitter.TwitterHelper import ReplyWith


class ThanksResponse(Response):
    def __init__(self):
        self.rx = re.compile("thx|thank(s|you)", re.IGNORECASE)

    def Condition(self, inbox_item):
        return not inbox_item.from_me \
               and (inbox_item.isDirectMessage or inbox_item.isTweet) \
               and inbox_item.to_me \
               and bool(self.rx.match(inbox_item.text))

    def Respond(self, inbox_item):
        thanks = [
            "thx",
            "thanks",
            "thankyou",
            "thank u",
        ]
        ReplyWith(inbox_item, random.choice(thanks) + " for the " + random.choice(thanks))
