from twitterpibot.topics.Topic import GoodTopic


class Swearing(GoodTopic):
    def __init__(self):
        super(Swearing, self).__init__({
            "shite?", "crap", "bollocks?", "bugger", "arse", "wankers?", "minge", "tossers?", "bastards?", "dickheads?",
            "fuck", "cunt", "twat"
        })


def get():
    return [
        Swearing()

    ]
