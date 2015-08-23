from Response import Response
import random

from OutgoingTweet import OutgoingTweet
from MyTwitter import MyTwitter
class RetweetResponse(Response):
    def Condition(args, inboxItem):
        return super(RetweetResponse, args).Condition(inboxItem) and inboxItem.isTweet


    def Favourite(args, inboxItem):
        return False

    def Respond(args, inboxItem):

        
        with MyTwitter() as twitter:
            twitter.retweet(id = inboxItem.status_id)
            