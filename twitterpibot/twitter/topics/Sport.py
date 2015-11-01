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


class Rugby(Topic):
    def __init__(self):
        teams = set(["All Blacks"])
        super(Rugby, self).__init__(set(["Rugby", "#RWC"]) | teams)


class Cricket(Topic):
    def __init__(self):
        teams = ["England", "Pakistan", "India", "Australia"]
        ["%s to (bat|field|bowl)".format(team) for team in teams]
        super(Cricket, self).__init__(
            set(["Cricket", "wicket", "the toss"]) | set(["%s to (bat|field|bowl)".format(team) for team in teams]),
            ["bowl", "bat"])


class SportOther(Topic):
    def __init__(self):
        super(SportOther, self).__init__([
            "#(?P<hometeam>[\w]{2,4}) ?vs?#? ?(?P<awayteam>[\w]{2,4})"

        ])


def get():
    return [
        # TODO More Sports
        FootballUK(),
        Rugby(),
        Cricket(),
        SportOther()
    ]
