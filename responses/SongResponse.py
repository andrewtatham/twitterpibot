from Response import Response
from OutgoingTweet import OutgoingTweet
import os
from Songs import Songs
import random
from TwitterHelper import Send


class SongResponse(Response):
    def __init__(self):
        self.songs = Songs()
        self.songnames = self.songs.AllKeys()

    def Condition(self, inboxItem):
        return super(SongResponse,self).Condition(inboxItem) \
            and inboxItem.to_me \
            and self.Contains(inboxItem.words, self.songnames)

    def Contains(self, list_a, list_b):
        for item_a in list_a:
            for item_b in list_b:
                if item_a.lower() == item_b.lower():
                    return True
        return False

    def Respond(self, inboxItem):
        for word in inboxItem.words:
            for songname in self.songnames:
                if word.lower() == songname.lower():
                    self.songs.Send(
                        songKey = songname,
                        inboxItem = inboxItem, 
                        response = self)



