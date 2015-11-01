from twitterpibot.twitter.topics.Topic import Topic


class PoliticsUK(Topic):
    def __init__(self):
        super(PoliticsUK, self).__init__([
            "David Cameron",
            "George Osborne",
            "Jeremy Hunt",
            "Conservative",
            r"\bTory\b",

            "Jeremy Corbyn",
            "Labour",

            "Nigel Farage",
            "UKIP",

            "PMQ",
            "Prime Minister",
            "Westminster",
            "Downing"
        ], ["politic", r"\bPM\b"])


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

        ], ["politic"])


def get():
    return [PoliticsUK(), PoliticsUS()]
