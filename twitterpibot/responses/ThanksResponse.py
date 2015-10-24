import re
from Response import Response
import random
from twitterpibot.twitter.TwitterHelper import ReplyWith


class ThanksResponse(Response):
    def __init__(self):
        self.rx = re.compile("thx|thank(s|you)", re.IGNORECASE)

    def Condition(self, inboxItem):
        return not inboxItem.from_me \
               and (inboxItem.isDirectMessage or inboxItem.isTweet) \
               and inboxItem.to_me \
               and bool(self.rx.match(inboxItem.text))

    def Respond(self, inboxItem):
        thanks = [
            "thx",
            "thanks",
            "thankyou",
            "thank u",
        ]
        ReplyWith(inboxItem, random.choice(thanks) + " for the " + random.choice(thanks))
