from twitterpibot.incoming.InboxItem import InboxItem
from itertools import cycle
from colorama import Fore, Style
import os
import twitterpibot.users.Users as Users

eventcolours = cycle([Fore.MAGENTA, Fore.CYAN])


class IncomingEvent(InboxItem):
    def __init__(self, data):

        super(IncomingEvent, self).__init__()

        self.isEvent = True

        # https://dev.twitter.com/streaming/overview/messages-types#Events_event

        self.source = Users.getUser(data=data["source"])
        self.target = Users.getUser(data=data["target"])

        self.from_me = self.source.isMe
        self.to_me = self.target.isMe

        self.event = data["event"]
        self.isFavorite = self.event == "favorite"
        self.isFollow = self.event == "follow"
        self.isRetweet = self.event == "quoted_tweet"

        self.targetObject = None
        self.targetObjectID = None
        self.targetObjectText = None
        if "target_object" in data:
            self.targetObject = data["target_object"]

            if "id_str" in self.targetObject:
                self.targetObjectID = self.targetObject["id_str"]

            if "text" in self.targetObject:
                self.targetObjectText = self.targetObject["text"]

    def Display(self):

        colour = next(eventcolours)

        if self.to_me:
            colour += Style.BRIGHT
        elif self.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM

        text = "* EVENT: Type: " + self.event + os.linesep \
               + " Source: " + self.source.name + " [@" + self.source.screen_name + "]" + os.linesep \
               + " Target: " + self.target.name + " [@" + self.target.screen_name + "]"

        if self.targetObjectText:
            text += os.linesep + " TargetObject: " + self.targetObjectText

        print(colour + text)
