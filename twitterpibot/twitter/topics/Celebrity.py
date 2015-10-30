from twitterpibot.twitter.topics.FiveSecondsOfSummer import FiveSecondsOfSummer
from twitterpibot.twitter.topics.Kardashians import Kardashians
from twitterpibot.twitter.topics.OneDirection import OneDirection
from twitterpibot.twitter.topics.Topic import Topic


class CelebrityOther(Topic):
    def __init__(self):
        super(CelebrityOther, self).__init__([
            "Justin Bieber",
            "Miley Cyrus",
            "Taylor Swift",
            "Britney Spears",
            "Ariana Grande"
        ])

def get():
    return [
        OneDirection(),
        FiveSecondsOfSummer(),
        Kardashians(),

        CelebrityOther()
    ]
