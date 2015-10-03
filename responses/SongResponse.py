from Response import Response
from OutgoingTweet import OutgoingTweet
import os
from Songs import Songs
import random
class SongResponse(Response):
    def __init__(self, *args, **kwargs):
        self.songsfolder = "songs/"
        self.songs = Songs()
        self.songnames = self.songs.songs.keys()
        self.mutation = [",", ".", " *", " `", " ", " -", "_"]

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
                    song = args.songs.songs[songname]



                    if "video" in song and song["video"]:
                        tweet = args.ReplyWith(inboxItem=inboxItem, 
                            text=song["video"])
                        args.context.song.put(tweet)


                    lyricsfile = song["lyrics"]
                    lyrics = open(args.songsfolder + lyricsfile, "rb").readlines()
                    lastlyrics = []
                    for lyric in lyrics:
                        lyric = lyric.strip()
                        if lyric:

                            ## prevent duplicate lines
                            while lyric in lastlyrics:
                                lyric += random.choice(args.mutation)
                                print("[Songs] mutating" + lyric)
                            
                            tweet = args.ReplyWith(inboxItem=inboxItem, 
                                text=lyric)
                            args.context.song.put(tweet)
                            lastlyrics.append(lyric)

