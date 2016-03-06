import os
import random
import itertools

from twitterpibot.logic import FileSystemHelper
from twitterpibot.processing import christmas


class Songs(object):
    def __init__(self):
        self.songsfolder = FileSystemHelper.get_root() + "twitterpibot" + os.sep + "songs" + os.sep
        self._songs = CaseInsensitiveDict(
            {
                "500miles": {
                    "artist": "The Proclaimers",
                    "screen_name": "@The_Proclaimers",
                    "title": "I'm Gonna Be (500 Miles)",
                    "lyrics_file": "500miles.txt",
                    "video": "https://youtu.be/tM0sTNtWDiI"
                },
                "dontstopbelieving": {
                    "artist": "Journey",
                    "screen_name": "@JourneyOfficial",
                    "title": "Don't Stop Believin'",
                    "lyrics_file": "believin.txt",
                    "video": "https://youtu.be/KCy7lLQwToI"
                },
                "surfinbird": {
                    "artist": "The Trashmen",
                    "screen_name": "@TheTrashmenBand",
                    "title": "Surfin' Bird",
                    "lyrics_file": "bird.txt",
                    "video": "https://youtu.be/9Gc4QTqslN4",
                    "hashtag": "#PapaOohmowmow"
                },
                "bluemonday": {
                    "artist": "New Order",
                    "screen_name": "@neworder",
                    "title": "Blue Monday",
                    "lyrics_file": "bluemonday.txt",
                    "video": "https://youtu.be/FYH8DsU2WCk"
                },
                "bohrap": {
                    "artist": "Queen ",
                    "screen_name": "@QueenRockBand",
                    "title": "Bohemian Rhapsody ",
                    "lyrics_file": "bohrap.txt",
                    "video": "https://youtu.be/fJ9rUzIMcZQ"
                },
                "boomshackalack": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "boomshackalack.txt",
                    "video": "https://youtu.be/kZzBd41NuZw"
                },
                "commonpeople": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "common.txt",
                    "video": "https://youtu.be/yuTMWgOduFM"
                },
                "compton": {
                    "artist": "N.W.A.",
                    "screen_name": "@mcrencpt @icecube @drdre",
                    "title": "",
                    "lyrics_file": "compton.txt",
                    "video": "https://youtu.be/TMZi25Pq3T8"

                },
                "endoftheworld": {
                    "artist": "R.E.M.",
                    "screen_name": None,
                    "title": "It's The End Of The World As We Know It (And I Feel Fine)",
                    "lyrics_file": "endoftheworld.txt",
                    "video": "https://youtu.be/Z0GFRcFm-aY"
                },
                "forgotaboutdre": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "forgot.txt",
                    "video": "https://youtu.be/QFcv5Ma8u8k"
                },
                "freshprince": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "freshprince.txt",
                    "video": "https://youtu.be/hBe0VCso0qs"
                },
                "gangstersparadise": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "gangsters.txt",
                    "video": "https://youtu.be/cpGbzYlnz7c"
                },
                "hammertime": {
                    "artist": "MC Hammer",
                    "screen_name": "@MCHammer",
                    "title": "U Can't Touch This",
                    "lyrics_file": "hammertime.txt",
                    "video": "https://youtu.be/otCpCn0l4Wo"
                },
                "icebaby": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "ice.txt",
                    "video": "https://youtu.be/rog8ou-ZepE"
                },
                "incredible": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "incredible.txt",
                    "video": "https://youtu.be/mL2Bgj-za5k"
                },
                "informer": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "informer.txt",
                    "video": "https://youtu.be/StlMdNcvCJo"
                },
                "japanese": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "japanese.txt",
                    "video": "https://youtu.be/mgekmOqCFTU"
                },
                "jinglebells": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "jingle.txt",
                    "video": "https://youtu.be/FVJskPa2a3s",
                    "christmas": "true"
                },
                "welcometothejungle": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics_file": "jungle.txt",
                    "video": "https://youtu.be/o1tj2zJ2Wvg"
                },
                "nighttrain": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics_file": "nighttrain.txt",
                    "video": "https://youtu.be/Qyf8oRF6Trg"
                },
                "novemberrain": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics_file": "novemberrain.txt",
                    "video": "https://youtu.be/8SbUC-UaAxE"
                },
                "paradisecity": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics_file": "paradise.txt",
                    "video": "https://youtu.be/Rbm6GXllBiw"
                },
                "fuckthepolice": {
                    "artist": "N.W.A.",
                    "screen_name": "@mcrencpt @icecube @drdre",
                    "title": "",
                    "lyrics_file": "police.txt",
                    "video": "https://youtu.be/Z7-TTWgiYL4"
                },
                "rickroll": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "rickroll.txt",
                    "video": "https://youtu.be/dQw4w9WgXcQ"
                },
                "rocklobster": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "rocklobster.txt",
                    "video": "https://youtu.be/tDZy6-fMCw4"
                },
                "toosexy": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "sexy.txt",
                    "video": "https://youtu.be/YFmsgHfuXpA"
                },
                "spinmeround": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "spinmeround.txt",
                    "video": "https://youtu.be/PGNiXGX2nLU"
                },
                "stilldre": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "stilldre.txt",
                    "video": "https://youtu.be/_CL6n0FJZpk"
                },
                "stuckinthemiddle": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "stuckinthemiddle.txt",
                    "video": "https://youtu.be/DohRa9lsx0Q"
                },
                "sweetchildomine": {
                    "artist": "Guns N' Roses",
                    "screen_name": "@gunsnroses",
                    "title": "",
                    "lyrics_file": "sweet.txt",
                    "video": "https://youtu.be/1w7OgIMMRc4"
                },
                "wonderwall": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "wonderwall.txt",
                    "video": "https://youtu.be/6hzrDeceEKc"
                },
                "wedidntstartthefire": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "wedidntstartthefire.txt",
                    "video": "https://youtu.be/eFTLKWw542g"
                },
                "gangnamstyle": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "gangnamstyle.txt",
                    "video": "https://youtu.be/9bZkp7q19f0"
                },
                "americafuckyeah": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "americafuckyeah.txt",
                    "video": "https://youtu.be/7R5A0pg4oN8"
                },
                "ronery": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "ronery.txt",
                    "video": "https://youtu.be/UEaKX9YYHiQ"
                },
                "aids": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "aids.txt",
                    "video": "https://youtu.be/StPTCo5qk8E"
                },
                "jumparound": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "jumparound.txt",
                    "video": "https://youtu.be/KZaz7OqyTHQ"
                },
                "jump": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "jump.txt",
                    "video": "https://youtu.be/010KyIQjkTk"
                },
                "tribute": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "tribute.txt",
                    "video": "https://youtu.be/_lK4cX5xGiQ"
                },
                "rhumble": {
                    "artist": "",
                    "screen_name": None,
                    "title": "Let's Get Ready To Rhumble",
                    "lyrics_file": "rhumble.txt",
                    "video": "https://youtu.be/m_sJmIQrH54"
                },

                # Birthday songs
                "indaclub": {
                    "artist": "50 Cent",
                    "screen_name": None,
                    "title": "In Da Club",
                    "lyrics_file": "indaclub.txt",
                    "video": "https://youtu.be/5qm8PH4xAss",
                    "birthday": "true"

                },
                "jollygoodfellow": {
                    "artist": "",
                    "screen_name": None,
                    "title": "For He's a Jolly Good Fellow",
                    "lyrics_file": "jollygoodfellow.txt",
                    "video": "https://youtu.be/RYLtBFQDAGE",
                    "birthday": "true"
                },
                "happybirthdaytoya": {
                    "artist": "Stevie Wonder",
                    "screen_name": None,
                    "title": "Happy Birthday",
                    "lyrics_file": "happybirthdaytoya.txt",
                    "video": "https://youtu.be/inS9gAgSENE",
                    "birthday": "true"
                },
                "happybirthdaytoyou_minions": {
                    "artist": "",
                    "screen_name": None,
                    "title": "",
                    "lyrics_file": "happybirthdaytoyou.txt",
                    "video": "https://youtu.be/xxOviBI-8fc",
                    "birthday": "true"
                },
                "happybirthdayhendrix": {
                    "artist": "Jimmi Hendrix",
                    "screen_name": None,
                    "title": "Happy Birthday",
                    "lyrics_file": "happybirthdayhendrix.txt",
                    "video": "https://youtu.be/USip2Phpy60",
                    "birthday": "true"
                },
                "happybirthdaybeatles": {
                    "artist": "The Beatles",
                    "screen_name": None,
                    "title": "Happy Birthday",
                    "lyrics_file": "happybirthdaybeatles.txt",
                    "video": "https://youtu.be/wNcJ3jYOQGg",
                    "birthday": "true"
                },
                "birthdaykatyperry": {
                    "artist": "Katy Perry",
                    "screen_name": None,
                    "title": "Birthday",
                    "lyrics_file": "birthdaykatyperry.txt",
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

    def all_keys(self):
        # always returns all keys
        return self._songs.keys()

    def keys(self):
        is_christmas = christmas.is_christmas()
        keys = [k for k, v in self._songs.items() if "birthday" not in v and (is_christmas or "christmas" not in v)]
        return keys

    def birthday_song_keys(self):
        return self._birthdaySongKeys

    def get_song(self, song_key):
        song = self._songs[song_key]
        lyrics_path = self.songsfolder + song["lyrics_file"]
        lyrics_file = open(lyrics_path, "r")
        lyrics = lyrics_file.readlines()
        lyrics_file.close()
        song["lyrics"] = lyrics
        return song


class CaseInsensitiveDict(dict):
    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(key.lower(), value)

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(key.lower())
