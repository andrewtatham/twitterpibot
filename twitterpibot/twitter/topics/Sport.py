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
            "#WHUFC",

            "FA Cup",
            "Wembley",
            "Premier League",
            "Soccer"

        ], ["Football", "rangers", "celtic", r"\bHib"])


class Rugby(Topic):
    def __init__(self):
        teams = {"All Blacks"}
        super(Rugby, self).__init__({"Rugby", "#RWC"} | teams)


class Cricket(Topic):
    def __init__(self):
        teams = ["England", "Pakistan", "India", "Australia"]
        ["%s to (bat|field|bowl)".format(team) for team in teams]
        super(Cricket, self).__init__(
            {"Cricket", "wicket", "the toss"} | set(["%s to (bat|field|bowl)".format(team) for team in teams]))


class Golf(Topic):
    def __init__(self):
        super(Golf, self).__init__({"Golf", "Tiger Woods", "PGA Tour"})


class Tennis(Topic):
    def __init__(self):
        super(Tennis, self).__init__({"Tennis", "Federer", "Nadal"})


class SportOther(Topic):
    def __init__(self):
        super(SportOther, self).__init__([
            r"#(?P<hometeam>[\w]{2,4}) ?vs?#? ?(?P<awayteam>[\w]{2,4})\b"

        ])


def get():
    return [

        FootballUK(),
        Rugby(),
        Cricket(),
        Golf(),
        Tennis(),
        SportOther()
    ]
