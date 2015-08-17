from InboxItem import InboxItem
from itertools import cycle
from colorama import Fore, Style
import os
import logging


eventcolours = cycle([
            Fore.MAGENTA,
            Fore.CYAN
                   ])



class IncomingEvent(InboxItem):
    def __init__(self, data, context):
        
        super(IncomingEvent, self).__init__(data)

        self.isEvent = True

        # https://dev.twitter.com/streaming/overview/messages-types#Events_event
        self.event = data["event"]
        self.sourceID = data["source"]["id_str"]
        self.sourceName = data["source"]["name"]
        self.sourceScreenName = data["source"]["screen_name"]

        self.targetID = data["target"]["id_str"]
        self.targetName = data["target"]["name"]
        self.targetScreenName = data["target"]["screen_name"]

        self.targetObject = None
        self.targetObjectID = None
        self.targetObjectText = None
        if "target_object" in data:
            self.targetObject = data["target_object"]

            if "id_str" in self.targetObject:
                self.targetObjectID = self.targetObject["id_str"]

            if "text" in self.targetObject:
                self.targetObjectText = self.targetObject["text"]

        self.isFavorite = self.event == "favorite"
        self.isFollow = self.event == "follow"
        self.isRetweet = self.event == "quoted_tweet"
        
        # favorited_retweet
        # retweeted_retweet

        self.from_me = self.sourceID == context.users.me["id"]
        self.to_me = self.targetID == context.users.me["id"]
 

        if self.isFavorite:
            pass
        elif self.isFollow:
            pass
        elif self.isRetweet:
            pass

        
  

    def Display(args):
        
        colour = eventcolours.next()

        if args.to_me:
            colour += Style.BRIGHT
        elif args.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM

        
        text = "* EVENT: Type: " + args.event + os.linesep \
                    + " Source: " + args.sourceName + " [@" + args.sourceScreenName + "]" + os.linesep \
                    + " Target: " + args.targetName + " [@" + args.targetScreenName + "]"

        if args.targetObjectText:
            text += os.linesep + " TargetObject: " + args.targetObjectText

        print(colour + text)

        logging.info(text)
        logging.info(args.targetObject)
