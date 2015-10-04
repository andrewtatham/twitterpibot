from Response import Response
from OutgoingTweet import OutgoingTweet
import random
class Songs(object):
    def __init__(self, *args, **kwargs):
        self.songsfolder = "songs/"
        self.mutation = [" ,", " .", " *", " `", " -", " _"]
        self._songs = CaseInsensitiveDict(
            {
            "500miles" : {
                "artist" : "The Proclaimers",
                "screen_name" : "@The_Proclaimers",
                "title" : "I'm Gonna Be (500 Miles)",
                "lyrics" : "500miles.txt",
                "video" : "https://youtu.be/tM0sTNtWDiI"
            },
            "dontstopbelieving" : {
                "artist" : "Journey",
                "screen_name" : "@JourneyOfficial",
                "title" : "Don't Stop Believin'",
                "lyrics" : "believin.txt",
                "video" : "https://youtu.be/KCy7lLQwToI"
            },
            "surfinbird" : {
                "artist" : "The Trashmen",
                "screen_name" : "@TheTrashmenBand",
                "title" : "Surfin' Bird",
                "lyrics" : "bird.txt",
                "video" : "https://youtu.be/9Gc4QTqslN4",
                "hashtag" : "#PapaOohmowmow"
            },
            "bluemonday" : {
                "artist" : "New Order",
                "screen_name" : "@neworder",
                "title" : "Blue Monday",
                "lyrics" : "bluemonday.txt",
                "video" : "https://youtu.be/FYH8DsU2WCk"
            },
            "bohrap" : {
                "artist" : "Queen ",
                "screen_name" : "@QueenRockBand",
                "title" : "Bohemian Rhapsody ",
                "lyrics" : "bohrap.txt",
                "video" : "https://youtu.be/fJ9rUzIMcZQ"
            },
            "boomshackalack" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "boomshackalack.txt",
                "video" : "https://youtu.be/kZzBd41NuZw"
            },
            "commonpeople" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "common.txt",
                "video" : "https://youtu.be/yuTMWgOduFM"
            },
            "compton" : {
                "artist" : "N.W.A.",
                "screen_name" : "@mcrencpt @icecube @drdre",
                "title" : "",
                "lyrics" : "compton.txt",
                "video" : "https://youtu.be/TMZi25Pq3T8"

            },
            ##"dodgeball" : {
            ##    "artist" : "",
            ##    "title" : "",
            ##    "lyrics" : "dodgeball.txt",
            ##    "video" : ""
            ##},
            "forgotaboutdre" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "forgot.txt",
                "video" : "https://youtu.be/QFcv5Ma8u8k"
            },
            "freshprince" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "freshprince.txt",
                "video" : "https://youtu.be/hBe0VCso0qs"
            },
            "gangstersparadise" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "gangsters.txt",
                "video" : "https://youtu.be/cpGbzYlnz7c"
            },
            "hammertime" : {
                "artist" : "MC Hammer",
                "screen_name" : "@MCHammer",
                "title" : "U Can't Touch This",
                "lyrics" : "hammertime.txt",
                "video" : "https://youtu.be/otCpCn0l4Wo"
            },
            "icebaby" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "ice.txt",
                "video" : "https://youtu.be/rog8ou-ZepE"
            },
            "incredible" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "incredible.txt",
                "video" : "https://youtu.be/mL2Bgj-za5k"
            },
            "informer" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "informer.txt",
                "video" : "https://youtu.be/StlMdNcvCJo"
            },
            "japanese" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "japanese.txt",
                "video" : "https://youtu.be/mgekmOqCFTU"
            },
            "jinglebells" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "jingle.txt",
                "video" : "https://youtu.be/FVJskPa2a3s"
            },
            "welcometothejungle" : {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title" : "",
                "lyrics" : "jungle.txt",
                "video" : "https://youtu.be/o1tj2zJ2Wvg"
            },
            "nighttrain" : {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title" : "",
                "lyrics" : "nighttrain.txt",
                "video" : "https://youtu.be/Qyf8oRF6Trg"
            },
            "novemberrain" : {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title" : "",
                "lyrics" : "novemberrain.txt",
                "video" : "https://youtu.be/8SbUC-UaAxE"
            },
            "paradisecity" : {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title" : "",
                "lyrics" : "paradise.txt",
                "video" : "https://youtu.be/Rbm6GXllBiw"
            },
            "fuckthepolice" : {
                "artist" : "N.W.A.",
                "screen_name" : "@mcrencpt @icecube @drdre",
                "title" : "",
                "lyrics" : "police.txt",
                "video" : "https://youtu.be/Z7-TTWgiYL4"
            },
            "rickroll" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "rickroll.txt",
                "video" : "https://youtu.be/dQw4w9WgXcQ"
            },
            "rocklobster" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "rocklobster.txt",
                "video" : "https://youtu.be/tDZy6-fMCw4"
            },
            "toosexy" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "sexy.txt",
                "video" : "https://youtu.be/YFmsgHfuXpA"
            },
            "spinmeround" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "spinmeround.txt",
                "video" : "https://youtu.be/PGNiXGX2nLU"
            },
            "stilldre" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "stilldre.txt",
                "video" : "https://youtu.be/_CL6n0FJZpk"
            },
            "stuckinthemiddle" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "stuckinthemiddle.txt",
                "video" : "https://youtu.be/DohRa9lsx0Q"
            },
            "sweetchildomine" : {
                "artist" : "Guns N' Roses",
                "screen_name" : "@gunsnroses",
                "title" : "",
                "lyrics" : "sweet.txt",
                "video" : "https://youtu.be/1w7OgIMMRc4"
            },
            "wonderwall" : {
                "artist" : "",
                "screen_name" : None,
                "title" : "",
                "lyrics" : "wonderwall.txt",
                "video" : "https://youtu.be/6hzrDeceEKc"
            }
        }
    )

    def Keys(args):
        return args._songs.keys()   
    def ViewKeys(args):
        return args._songs.viewkeys()


    def Send(args, context, songKey, target = None, inboxItem = None, response = None ):
        song = args._songs[songKey]

        if "video" in song and song["video"]:
            text = "Sing along! " + song["video"]
            args._send(inboxItem, text, response, target)

        lyricsfile = song["lyrics"]
        lyrics = open(args.songsfolder + lyricsfile, "rb").readlines()
        lastlyrics = set([])
        for lyric in lyrics:
            lyric = lyric.strip()
            if lyric:
                ## prevent duplicate lines
                while lyric in lastlyrics:
                    lyric += random.choice(args.mutation)
                lastlyrics.add(lyric)
                args._send(inboxItem, lyric, response, target)

  
                   
                    

      
              
    def _send(args, inboxItem, lyric, response, target):
        if response and inboxItem:
            Response.ReplyWith(response,
                inboxItem=inboxItem, 
                text=lyric)
        else:
            text = ""
            if target:
                text = "@" + target.screen_name + " "
            text += lyric
            tweet = OutgoingTweet(text = text)
            args.context.send(tweet)
       



class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())