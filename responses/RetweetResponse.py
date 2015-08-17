from Response import Response
import random

from OutgoingTweet import OutgoingTweet
from MyTwitter import MyTwitter
class RetweetResponse(Response):
    def Condition(args, inboxItem):
        return inboxItem.isTweet and not inboxItem.from_me and random.randint(0,50) == 0

    def Favourite(args, inboxItem):
        return False

    def Respond(args, inboxItem):

        
        with MyTwitter() as twitter:
            twitter.retweet(id = inboxItem.status_id)
            