import os
import random
import time
import itertools

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.processing.christmas import is_christmas
from twitterpibot.twitter.TwitterHelper import Send, ReplyWith
from twitterpibot.users import User


class Songs(object):
    def __init__(self):
        self.songsfolder = "twitterpibot" + os.sep + "songs" + os.sep
        self.mutation = [" ,", " .", " *", " `", " -", " _"]
        self._songs = CaseInsensitiveDict(
            {
                "500miles": {
                    "artist": "The Proclaimers",
                    "screen_name": "@The_Proclaimers",
                    "title": "I'm Gonna Be (500 Miles)",
                    "lyrics": "500miles.txt",
                    "video": "https://youtu.be/tM0sTNtWDiI"
                },
                "dontstopbelieving": {
                    "artist": "Journey",
                    "screen_name": "@JourneyOfficial",
                    "title": "Don't Stop Believin'",
                    "lyrics": "believin.txt",
                    "video": "https://youtu.be/KCy7lLQwToI"
                },
                "surfinbird": {
                    "artist": "The Trashmen",
                    "screen_name": "@TheTrashmenBand",
                    "title": "Surfin' Bird",
                    "lyrics": "bird.txt",
                    "video": "https://youtu.be/9Gc4QTqslN4",
                    "hashtag": "#PapaOohmowmow"
                },
                "bluemonday": {
                    "artist": "New Order",
                    "screen_name": "@neworder",
                    "title": "Blue Monday",
                    "lyrics": "bluemonday.txt",
                    "video": "https://youtu.be/FYH8DsU2WCk"
                },
                "bohrap": {
                    "artist": "Queen ",
                    "screen_name": "@QueenRockBand",
                    "title": "Bohemian Rhapsody ",
                    "lyrics": "bohrap.txt",
                    "video": "https://youtu.be/fJ9rUzIMcZQ"
                },
                "boomshackalack": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "boomshackalack.txt",
                    "video": "https://youtu.be/kZzBd41NuZw"
                },
                "commonpeople": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "common.txt",
                    "video": "https://youtu.be/yuTMWgOduFM"
                },
                "compton": {
                    "artist": "N.W.A.",
                    "screen_name": "@mcrencpt @icecube @drdre",
                    "title": "",
                    "lyrics": "compton.txt",
                    "video": "https://youtu.be/TMZi25Pq3T8"

                },
                "endoftheworld": {
                    "artist": "R.E.M.",
                    "screen_name": None,
                    "title": "It's The End Of The World As We Know It (And I Feel Fine)",
                    "lyrics": "endoftheworld.txt",
                    "video": "https://youtu.be/Z0GFRcFm-aY"
                },
                "forgotaboutdre": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "forgot.txt",
                    "video": "https://youtu.be/QFcv5Ma8u8k"
                },
                "freshprince": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "freshprince.txt",
                    "video": "https://youtu.be/hBe0VCso0qs"
                },
                "gangstersparadise": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "gangsters.txt",
                    "video": "https://youtu.be/cpGbzYlnz7c"
                },
                "hammertime": {
                    "artist": "MC Hammer",
                    "screen_name": "@MCHammer",
                    "title": "U Can't Touch This",
                    "lyrics": "hammertime.txt",
                    "video": "https://youtu.be/otCpCn0l4Wo"
                },
                "icebaby": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "ice.txt",
                    "video": "https://youtu.be/rog8ou-ZepE"
                },
                "incredible": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "incredible.txt",
                    "video": "https://youtu.be/mL2Bgj-za5k"
                },
                "informer": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "informer.txt",
                    "video": "https://youtu.be/StlMdNcvCJo"
                },
                "japanese": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "japanese.txt",
                    "video": "https://youtu.be/mgekmOqCFTU"
                },
                "jinglebells": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "jingle.txt",
                    "video": "https://youtu.be/FVJskPa2a3s",
                    "christmas": "true"
                },
                "welcometothejungle": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics": "jungle.txt",
                    "video": "https://youtu.be/o1tj2zJ2Wvg"
                },
                "nighttrain": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics": "nighttrain.txt",
                    "video": "https://youtu.be/Qyf8oRF6Trg"
                },
                "novemberrain": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics": "novemberrain.txt",
                    "video": "https://youtu.be/8SbUC-UaAxE"
                },
                "paradisecity": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics": "paradise.txt",
                    "video": "https://youtu.be/Rbm6GXllBiw"
                },
                "fuckthepolice": {
                    "artist": "N.W.A.",
                    "screen_name": "@mcrencpt @icecube @drdre",
                    "title": "",
                    "lyrics": "police.txt",
                    "video": "https://youtu.be/Z7-TTWgiYL4"
                },
                "rickroll": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "rickroll.txt",
                    "video": "https://youtu.be/dQw4w9WgXcQ"
                },
                "rocklobster": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "rocklobster.txt",
                    "video": "https://youtu.be/tDZy6-fMCw4"
                },
                "toosexy": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "sexy.txt",
                    "video": "https://youtu.be/YFmsgHfuXpA"
                },
                "spinmeround": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "spinmeround.txt",
                    "video": "https://youtu.be/PGNiXGX2nLU"
                },
                "stilldre": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "stilldre.txt",
                    "video": "https://youtu.be/_CL6n0FJZpk"
                },
                "stuckinthemiddle": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "stuckinthemiddle.txt",
                    "video": "https://youtu.be/DohRa9lsx0Q"
                },
                "sweetchildomine": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics": "sweet.txt",
                    "video": "https://youtu.be/1w7OgIMMRc4"
                },
                "wonderwall": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "wonderwall.txt",
                    "video": "https://youtu.be/6hzrDeceEKc"
                },
                "wedidntstartthefire": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "wedidntstartthefire.txt",
                    "video": "https://youtu.be/eFTLKWw542g"
                },
                "gangnamstyle": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "gangnamstyle.txt",
                    "video": "https://youtu.be/9bZkp7q19f0"
                },
                "americafuckyeah": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "americafuckyeah.txt",
                    "video": "https://youtu.be/7R5A0pg4oN8"
                },
                "ronery": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "ronery.txt",
                    "video": "https://youtu.be/UEaKX9YYHiQ"
                },
                "aids": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "aids.txt",
                    "video": "https://youtu.be/StPTCo5qk8E"
                },
                "jumparound": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "jumparound.txt",
                    "video": "https://youtu.be/KZaz7OqyTHQ"
                },
                "jump": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "jump.txt",
                    "video": "https://youtu.be/010KyIQjkTk"
                },
                "tribute": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "tribute.txt",
                    "video": "https://youtu.be/_lK4cX5xGiQ"
                },
                "rhumble": {
                    "artist": "",
                    "screen_name": None,
                    "title": "Let's Get Ready To Rhumble",
                    "lyrics": "rhumble.txt",
                    "video": "https://youtu.be/m_sJmIQrH54"
                },



                # Birthday songs
                "indaclub": {
                    "artist": "50 Cent",
                    "screen_name": None,
                    "title": "In Da Club",
                    "lyrics": "indaclub.txt",
                    "video": "https://youtu.be/5qm8PH4xAss",
                    "birthday": "true"

                },
                "jollygoodfellow": {
                    "artist": "",
                    "screen_name": None,
                    "title": "For He's a Jolly Good Fellow",
                    "lyrics": "jollygoodfellow.txt",
                    "video": "https://youtu.be/RYLtBFQDAGE",
                    "birthday": "true"
                },
                "happybirthdaytoya": {
                    "artist": "Stevie Wonder",
                    "screen_name": None,
                    "title": "Happy Birthday",
                    "lyrics": "happybirthdaytoya.txt",
                    "video": "https://youtu.be/inS9gAgSENE",
                    "birthday": "true"
                },
                "happybirthdaytoyou_minions": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics": "happybirthdaytoyou.txt",
                    "video": "https://youtu.be/xxOviBI-8fc",
                    "birthday": "true"
                },
                "happybirthdayhendrix": {
                    "artist": "Jimmi Hendrix",
                    "screen_name": None,
                    "title": "Happy Birthday",
                    "lyrics": "happybirthdayhendrix.txt",
                    "video": "https://youtu.be/USip2Phpy60",
                    "birthday": "true"
                },
                "happybirthdaybeatles": {
                    "artist": "The Beatles",
                    "screen_name": None,
                    "title": "Happy Birthday",
                    "lyrics": "happybirthdaybeatles.txt",
                    "video": "https://youtu.be/wNcJ3jYOQGg",
                    "birthday": "true"
                },
                "birthdaykatyperry": {
                    "artist": "Katy Perry",
                    "screen_name": None,
                    "title": "Birthday",
                    "lyrics": "birthdaykatyperry.txt",
                    "video": "https://youtu.be/jqYxyd1iSNk",
                    "birthday": "true"
                },

            })

        self._birthdaySongKeys = []
        for k, v in self._songs.items():
            if "birthday" in v and v["birthday"]:
                self._birthdaySongKeys.append(k)
        random.shuffle(self._birthdaySongKeys)
        self._birthdaySongKeys = itertools.cycle(self._birthdaySongKeys)

    def AllKeys(self):
        # always returns all keys
        return self._songs.keys()

    def Keys(self):
        isChristmas = is_christmas()
        keys = [k for k, v in self._songs.items() if "birthday" not in v and (isChristmas or "christmas" not in v)]
        return keys

    def SingBirthdaySong(self, screen_name):
        songKey = self._birthdaySongKeys.next()
        self.Send(songKey, screen_name, text="Happy Birthday @" + screen_name + " !!!", hashtag="#HappyBirthday")

    def Send(self, songKey, target=None, inbox_item=None, text=None, hashtag=None):
        song = self._songs[songKey]

        if not text:
            text = random.choice(["All together now!", "Sing along!"])
        text += ' ' + song["video"]
        if hashtag:
            text += ' ' + hashtag

        in_reply_to_status_id = self._send(inbox_item, text, target, None)
        time.sleep(5)

        lyricsfile = song["lyrics"]
        lyrics = open(self.songsfolder + lyricsfile, "rb").readlines()
        lastlyrics = set([])
        for lyric in lyrics:
            lyric = lyric.strip()
            if lyric:
                if "<<screen_name>>" in lyric:
                    lyric = lyric.replace("<<screen_name>>", "@" + target)

                if hashtag:
                    lyric += ' ' + hashtag

                    # prevent duplicate lines
                while lyric in lastlyrics:
                    lyric += random.choice(self.mutation)
                lastlyrics.add(lyric)
                in_reply_to_status_id = self._send(
                    inbox_item,
                    lyric,
                    target,
                    in_reply_to_status_id)
                time.sleep(2)

    def _send(self, inbox_item, lyric, target, in_reply_to_status_id):
        if inbox_item:
            return ReplyWith(
                inbox_item=inbox_item,
                text=lyric,
                in_reply_to_status_id=in_reply_to_status_id)
        else:
            text = ""
            if target:
                # noinspection PyUnresolvedReferences
                if isinstance(target, basestring):
                    text = "@" + target
                elif isinstance(target, User.User):
                    text = "@" + target.screen_name
            text += " " + lyric
            tweet = OutgoingTweet(
                text=text,
                in_reply_to_status_id=in_reply_to_status_id)
            return Send(tweet)


class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())
