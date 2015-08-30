from Response import Response
from OutgoingTweet import OutgoingTweet
import os
class SongResponse(Response):
    def __init__(self, *args, **kwargs):
        songsfolder = "songs/"
        self.songNames = []
        self.songs = {}
        songfiles = os.listdir(songsfolder)
        for songfile in songfiles:
            songname = songfile.lower()
            if songname.endswith('.txt'):
                songname = songname[:-4]
            self.songNames.append(songname)
            self.songs[songname] = open(songsfolder + songfile, "rb").readlines()

    def Condition(args, inboxItem):
        return super(SongResponse,args).Condition(inboxItem) \
            and inboxItem.to_me \
            and args.Contains(inboxItem.words, args.songNames)

    def Contains(args, list_a, list_b):
        for item_a in list_a:
            for item_b in list_b:
                if item_a.lower() == item_b.lower():
                    return True
        return False

    def Respond(args, inboxItem):

        for word in inboxItem.words:
            for songname in args.songNames:
                if word.lower() == songname.lower():
                    lyrics = args.songs[songname.lower()]
                    lastlyric = ""
                    for lyric in lyrics:
                        lyric = lyric.strip()
                        if lyric and lyric != lastlyric:
                            
                            tweet = args.ReplyWith(inboxItem=inboxItem, 
                                text=lyric)
                            args.context.song.put(tweet)
                            lastlyric = lyric

