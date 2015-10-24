from OutgoingTweet import OutgoingTweet
from OutgoingDirectMessage import OutgoingDirectMessage
import random
from TwitterHelper import Send, ReplyWith

class Response(object):   
    
    def Condition(self, inboxItem):
        return not inboxItem.from_me \
            and (inboxItem.isDirectMessage or inboxItem.isTweet
                 and (
                    inboxItem.to_me and (not inboxItem.sender.isReplyLess or random.randint(0,9) == 0)
                    or (inboxItem.sender.isBot and random.randint(0,3) == 0)
                    or (inboxItem.sender.isFriend and random.randint(0,1) == 0)
                    or (inboxItem.sender.isRetweetMore and random.randint(0,9) == 0)
                    or random.randint(0,99) == 0))



    def Favourite(self, inboxItem):
        return False


    def Contains(self, list, item):
        if list :
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False

    def Respond(self, inboxItem):
        return None



    

