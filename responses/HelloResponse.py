import re
from Response import Response
import random
class HelloResponse(Response):

    def __init__(self, *args, **kwargs):

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

    def Condition(args, inboxItem):
        return not inboxItem.from_me \
            and (inboxItem.isDirectMessage or inboxItem.isTweet) \
                and inboxItem.to_me \
                and bool(args.rx.match(inboxItem.text))

    def Respond(args, inboxItem):
        args.ReplyWith(inboxItem, random.choice(args.HelloWords))



