import re
from twitterpibot.responses.Response import Response
import random
from twitterpibot.twitter.TwitterHelper import ReplyWith


class HelloResponse(Response):
    def __init__(self):
        self.HelloWords = [
            "Hi",
            "Hiya",
            "Hey",
            "Hello",
            "Howdy",
            "Yo",
            "Bonjour",
            "G'day"

        ]

        self.rx = re.compile("|".join(self.HelloWords), re.IGNORECASE)

    def Condition(self, inbox_item):
        return not inbox_item.from_me \
               and (inbox_item.isDirectMessage or inbox_item.isTweet) \
               and inbox_item.to_me \
               and bool(self.rx.match(inbox_item.text))

    def Respond(self, inbox_item):
        ReplyWith(inbox_item, random.choice(self.HelloWords))
