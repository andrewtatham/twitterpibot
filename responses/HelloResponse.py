import re
from Response import Response
import random
from TwitterHelper import ReplyWith
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

    def Condition(self, inboxItem):
        return not inboxItem.from_me \
            and (inboxItem.isDirectMessage or inboxItem.isTweet) \
                and inboxItem.to_me \
                and bool(self.rx.match(inboxItem.text))

    def Respond(self, inboxItem):
        ReplyWith(inboxItem, random.choice(self.HelloWords))



