from twitterpibot.twitter.topics.Topic import Topic


class FootballUK(Topic):
    def __init__(self):
        super(FootballUK, self).__init__([
            "Man City",
            "Arsenal",
            "Chelsea",
            "Man United",
            "#[\w]{1,3}FC",
            "#AFCB",
            "#Arsenal",
            "#CFC",
            "#COYS",
            "#LCFC",
            "#LFC",
            "#MCFC",
            "#MUFC",
            "#NCFC",
            "#NUFC",
            "#SaintsFC",
            "#SCF",
            "#SAFC",
            "#Swans",
            "#WatfordFC",
            "#WBA",
            "#WHUFC"


        ])


class SportOther(Topic):
    def __init__(self):
        super(SportOther, self).__init__([
            "#(?P<hometeam>[\w]{2,4}) ?vs?#? ?(?P<awayteam>[\w]{2,4})"

        ])

def get():
    return [
        # TODO More Sports
        FootballUK(),
        SportOther()
    ]
