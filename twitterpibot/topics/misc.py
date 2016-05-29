from twitterpibot.topics.Topic import GoodTopic, IgnoreTopic


class Swearing(GoodTopic):
    def __init__(self):
        super(Swearing, self).__init__({
            "shite?", "crap", "bollocks?", "bugger", "arse", "wankers?", "minge", "tossers?", "bastards?", "dickheads?",
            "fuck", "cunt", "twat"
        })


class Racism(IgnoreTopic):
    # todo https://en.wikipedia.org/wiki/List_of_ethnic_slurs
    def __init__(self):
        super(Racism, self).__init__({
            "niggers?"
        })

class Hippies(IgnoreTopic):
    def __init__(self):
        super(Hippies, self).__init__({
            "Psychic",
            "Spiritual Healer"
        })


def get():
    return [
        Swearing(),
        Racism(),
        Hippies()
    ]
