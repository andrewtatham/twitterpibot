from Response import Response
import random

from OutgoingTweet import OutgoingTweet
from MyTwitter import MyTwitter
class RetweetResponse(Response):
    def Condition(args, inboxItem):
        return super(RetweetResponse, args).Condition(inboxItem) \
            and inboxItem.isTweet \
            and ((inboxItem.sender.isBot and random.randint(0,9) == 0) \
                or (inboxItem.sender.isFriend and random.randint(0,1) == 0) \
                or (inboxItem.sender.isRetweetMore and random.randint(0,9) == 0) \
                or random.randint(0,99) == 0)



    def Favourite(args, inboxItem):
        return False

    def Respond(args, inboxItem):

        
        with MyTwitter() as twitter:
            twitter.retweet(id = inboxItem.status_id)
            