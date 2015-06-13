from IncomingTweet import IncomingTweet
from IncomingDirectMessage import IncomingDirectMessage
from IncomingEvent import IncomingEvent
import logging


class InboxItemFactory():
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
            print("other...")
            logging.info(data)