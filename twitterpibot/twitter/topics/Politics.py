from twitterpibot.twitter.topics.Topic import NewsTopic


class PoliticsUK(NewsTopic):
    def __init__(self):
        super(PoliticsUK, self).__init__([
            "(David)? Cameron",
            "(George)? Osborne",
            "Jeremy Hunt",
            "(Margret|Maggie)? Thatcher",
            "Conservative",
            "Tor(y|ies)",

            "(Jeremy)? Corbyn",
            "(Ed)? Milliband",
            "(Tony)? Blair",
            "Gordon Brown",
            "Labour",

            "(Nigel)? Farage",
            "UKIP",

            "PMQ",
            "Prime Minister",
            "Westminster",
            "parliament",
            "Downing S(ree)?t"
        ], ["politic", "PM", "Ministers", "tax"])


class PoliticsUS(NewsTopic):
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
            "Kerry",

            "Senate",
            "House of Representatives"

        ], ["politic"])


def get():
    return [PoliticsUK(), PoliticsUS()]
