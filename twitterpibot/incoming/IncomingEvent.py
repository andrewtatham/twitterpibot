from itertools import cycle
import os
import logging

from colorama import Fore, Style

from twitterpibot.incoming.InboxItem import InboxItem

logger = logging.getLogger(__name__)

eventcolours = cycle([Fore.MAGENTA, Fore.CYAN])


class IncomingEvent(InboxItem):
    def __init__(self, data, identity):

        super(IncomingEvent, self).__init__(data, identity)

        self.is_event = True
        self.data = data

        # https://dev.twitter.com/streaming/overview/messages-types#Events_event

        self.source = identity.users.get_user(user_data=data.get("source"))
        self.target = identity.users.get_user(user_data=data.get("target"))

        self.from_me = self.source and self.source.is_me
        self.to_me = self.target and self.target.is_me

        self.event = data.get("event")
        self.is_block = self.event and self.event == "block"
        self.is_unblock = self.event and self.event == "unblock"
        self.is_favorite = self.event and self.event == "favorite"
        self.is_unfavorite = self.event and self.event == "unfavorite"
        self.is_follow = self.event and self.event == "follow"
        self.is_unfollow = self.event and self.event == "unfollow"
        self.is_retweet = self.event and self.event == "quoted_tweet"

        self.targetObject = None
        self.targetObjectID = None
        self.targetObjectText = None
        if "target_object" in data:
            self.targetObject = data["target_object"]

            if "id_str" in self.targetObject:
                self.targetObjectID = self.targetObject["id_str"]

            if "text" in self.targetObject:
                self.targetObjectText = self.targetObject["text"]

    def display(self):

        colour = self.identity.colour

        if self.to_me or self.from_me:
            colour += Style.BRIGHT
        else:
            colour += Style.NORMAL

        text = "* EVENT: Type: " + self.event + os.linesep \
               + " Source: " + self.source.short_description() + os.linesep \
               + " Target: " + self.target.short_description()

        if self.targetObjectText:
            text += os.linesep + " TargetObject: " + self.targetObjectText

        return colour + text
