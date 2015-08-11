from Response import Response
import random

from OutgoingTweet import OutgoingTweet
from MyTwitter import MyTwitter
class FavouriteResponse(Response):
    def Condition(args, inboxItem):
        return inboxItem.isTweet and not inboxItem.from_me and inboxItem.to_me

    def Respond(args, inboxItem):

        
        with MyTwitter() as twitter:
            twitter.create_favourite(id = inboxItem.status_id)
            