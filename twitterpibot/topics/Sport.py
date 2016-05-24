from twitterpibot.topics.Topic import IgnoreTopic, NewsTopic


class FootballUK(IgnoreTopic):
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
            "Soccer",
            "Leeds United"

        ], ["Football", "rangers", "celtic", "Hib(ernian)"])


class Rugby(IgnoreTopic):
    def __init__(self):
        teams = {"All Blacks"}
        super(Rugby, self).__init__({"Rugby", "#RWC"} | teams)


class Cricket(IgnoreTopic):
    def __init__(self):
        teams = ["England", "Pakistan", "India", "Australia"]
        ["%s to (bat|field|bowl)".format(team) for team in teams]
        super(Cricket, self).__init__(
            {
                "Cricket", "wicket", "the toss", "ODIs?", "batsman", "bowler", "field(ing|er)"
            } | set(["%s to (bat|field|bowl)".format(team) for team in teams]),
            [
                "field", "bowl(ing)?"
            ]
        )


class Golf(IgnoreTopic):
    def __init__(self):
        super(Golf, self).__init__({"Golf", "Tiger Woods", "PGA Tour"})


class Tennis(IgnoreTopic):
    def __init__(self):
        super(Tennis, self).__init__({"Tennis", "Federer", "Nadal"})


class SportOther(IgnoreTopic):
    def __init__(self):
        super(SportOther, self).__init__([
            "#(?P<hometeam>[\w]{2,4}) ?vs?#? ?(?P<awayteam>[\w]{2,4})"

        ])


class FormulaOne(NewsTopic):
    def __init__(self):
        super(FormulaOne, self).__init__({"F1", "Formula One"})


class Boxing(IgnoreTopic):
    def __init__(self):
        super(Boxing, self).__init__({"IBF", "(heavy)weight"})


def get():
    return [

        FootballUK(),
        Rugby(),
        Cricket(),
        Golf(),
        Tennis(),
        FormulaOne(),
        Boxing(),
        SportOther()
    ]
