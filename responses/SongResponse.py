from Response import Response
from OutgoingTweet import OutgoingTweet
import os
from Songs import Songs
import random
from TwitterHelper import Send


class SongResponse(Response):
    def __init__(self, *args, **kwargs):
        self.songs = Songs()
        self.songnames = self.songs.ViewKeys()

    def Condition(args, inboxItem):
        return super(SongResponse,args).Condition(inboxItem) \
            and inboxItem.to_me \
            and args.Contains(inboxItem.words, args.songnames)

    def Contains(args, list_a, list_b):
        for item_a in list_a:
            for item_b in list_b:
                if item_a.lower() == item_b.lower():
                    return True
        return False

    def Respond(args, inboxItem):
        for word in inboxItem.words:
            for songname in args.songnames:
                if word.lower() == songname.lower():
                    args.songs.Send(
                        songKey = songname,
                        inboxItem = inboxItem, 
                        response = args)



