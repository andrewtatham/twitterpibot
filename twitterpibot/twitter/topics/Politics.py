from twitterpibot.twitter.topics.Topic import Topic


class PoliticsUK(Topic):
    def __init__(self):
        super(PoliticsUK, self).__init__([
            "David", "Cameron",
            "George", "Osbourne",
            "Conservative",
            "Tory",

            "Jeremy", "Corbyn",
            "Labour",

            "Nigel", "Farage",
            "UKIP",

            "PM", "PMQ",
            "Prime Minister",
            "Westminster",
            "Downing"
        ])


class PoliticsUS(Topic):
    def __init__(self):
        super(PoliticsUS, self).__init__([

            "President",
            "POTUS",
            "Barack", "Obama",

            "Hilary", "Clinton",
            "Bernie", "Sanders",
            "Democrat",

            "Donald", "Trump",
            "Jeb", "Bush",
            "Marco", "Rubio",
            "Republican",
            "GOP",
            "Tea Party",

            "Senate",
            "House of Representatives"

        ])


def get():
    return [PoliticsUK(), PoliticsUS()]
