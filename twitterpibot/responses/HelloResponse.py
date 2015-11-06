import re
from twitterpibot.responses.Response import Response
import random
from twitterpibot.twitter.TwitterHelper import reply_with


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

    def condition(self, inbox_item):
        return not inbox_item.from_me \
               and (inbox_item.isDirectMessage or inbox_item.isTweet) \
               and inbox_item.to_me \
               and bool(self.rx.match(inbox_item.text))

    def respond(self, inbox_item):
        reply_with(inbox_item, random.choice(self.HelloWords))
