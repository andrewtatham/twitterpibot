import re
from Response import Response
import random
class ThanksResponse(Response):

    def __init__(self, *args, **kwargs):

        self.rx = re.compile("thx|thank(s|you)", re.IGNORECASE)

    def Condition(args, inboxItem):
        return not inboxItem.from_me \
            and (inboxItem.isDirectMessage or inboxItem.isTweet) \
                and inboxItem.to_me \
                and bool(args.rx.match(inboxItem.text))

    def Respond(args, inboxItem):
        thanks = [
            "thx",
            "thanks",
            "thankyou",
            "thank u",
            ]
        ReplyWith(inboxItem, random.choice(thanks) + " for the " + random.choice(thanks))



