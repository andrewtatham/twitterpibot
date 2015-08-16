from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage

class Response(object):
    def Condition(args, inboxItem):
        return (inboxItem.isTweet or inboxItem.isDirectMessage ) \
            and not inboxItem.from_me 



    def Contains(args, list, item):
        if list :
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False;

    def Respond(args, inboxItem):
        return None



    

    def ReplyWith(self, inboxItem, text, asTweet = False, asDM = False, photos = None, *args, **kwargs):    

        replyAsTweet = asTweet or not asDM and inboxItem.isTweet

        replyAsDM = asDM or not asTweet and inboxItem.isDirectMessage


        if replyAsTweet :
            tweet = OutgoingTweet(
                replyTo=inboxItem,
                text=text,                
                photos = photos)
            return tweet
           
        if replyAsDM:
            dm = OutgoingDirectMessage(   
                replyTo=inboxItem,
                text=text)
            return dm