from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage

class Response(object):
    def Condition(args, inboxItem):
        return ( 
            (inboxItem.IsTweet() or inboxItem.IsDirectMessage() ) 
            and not inboxItem.from_me and inboxItem.to_me
            )



    def Contains(args, list, item):
        if list is not None:
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False;

    def Respond(args, inboxItem):
        return None



    

    def ReplyWith(args, inboxItem, replyText):    
        if inboxItem.IsTweet():
            tweet = OutgoingTweet(inboxItem, replyText)
            return tweet
           
        if inboxItem.IsDirectMessage():
            dm = OutgoingDirectMessage(inboxItem, replyText)
            return dm