from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
import random

class Response(object):
    def Condition(args, inboxItem):
        return not inboxItem.from_me \
            and (inboxItem.isDirectMessage or inboxItem.isTweet \
                and (
                    inboxItem.to_me and (not args.inboxItem.sender.isReplyLess or random.randint(0,9) == 0)  \
                    or (inboxItem.sender.isBot and random.randint(0,3) == 0) \
                    or (inboxItem.sender.isFriend and random.randint(0,1) == 0) \
                    or (inboxItem.sender.isRetweetMore and random.randint(0,9) == 0) \
                    or random.randint(0,99) == 0))



    def Favourite(args, inboxItem):
        return True


    def Contains(args, list, item):
        if list :
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False

    def Respond(args, inboxItem):
        return None



    

    def ReplyWith(self, inboxItem, text, asTweet=False, asDM=False, photos=None, *args, **kwargs):    

        replyAsTweet = asTweet or not asDM and inboxItem.isTweet

        replyAsDM = asDM or not asTweet and inboxItem.isDirectMessage


        if replyAsTweet :
            tweet = OutgoingTweet(replyTo=inboxItem,
                text=text,                
                photos = photos)
            return tweet
           
        if replyAsDM:
            dm = OutgoingDirectMessage(replyTo=inboxItem,
                text=text)
            return dm