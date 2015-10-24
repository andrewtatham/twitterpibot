from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage
from twitterpibot.incoming.IncomingEvent import IncomingEvent


class InboxItemFactory(object):
    def Create(self, data):
        if "text" in data:
            return IncomingTweet(data)
        elif "direct_message" in data:
            return IncomingDirectMessage(data)
        elif "event" in data:
            return IncomingEvent(data)
        elif "friends" in data:
            print("Connected...")
        elif "delete" in data:
            pass
        else:
            pass
