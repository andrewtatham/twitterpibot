import re
from twitterpibot.incoming.InboxItem import InboxItem
from twitterpibot.responses.Response import Response
import random
from twitterpibot.twitter.TwitterHelper import reply_with


class ThanksResponse(Response):
    def __init__(self):
        self.rx = re.compile("thx|thank(s|you)", re.IGNORECASE)

    def condition(self, inbox_item:InboxItem):
        return not inbox_item.from_me \
               and (inbox_item.is_direct_message or inbox_item.is_tweet) \
               and inbox_item.to_me \
               and bool(self.rx.match(inbox_item.text))

    def respond(self, inbox_item):
        thanks = [
            "thx",
            "thanks",
            "thankyou",
            "thank u",
        ]
        reply_with(inbox_item, random.choice(thanks) + " for the " + random.choice(thanks))
