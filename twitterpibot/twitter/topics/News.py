from twitterpibot.twitter.topics.Topic import NewsTopic, DontCareTopic


class BadThings(NewsTopic):
    def __init__(self):
        super(BadThings, self).__init__(
            [
                "Shooting",
                "Gunman",
                "Fatal(y|ites)?",
                "wound(ed)?",
                "victims?",
                "murder(er|ed)?",
                "suicide",
                "peadophil(e|es|ic)?",
                "terror(ist|ism)?",
                "stab(bed|bing)?",
                "bomb(s)?",
                "explosion(s)?",
                "crash",
                "isil",
                "isis",
                "knife(d)?",
                "arson",
                "(child|sex) abuse",
                "rap(e|ed|ist|ing)'",
                "RIP"

            ], [
                "fire",
                "dead",
                "suspect(ed)",
                "abuse"
            ]
        )


class CivilRights(NewsTopic):
    def __init__(self):
        super(CivilRights, self).__init__(
            [
                "BlackLivesMatter",
                "LGBT?"

            ])


class Weather(DontCareTopic):
    def __init__(self):
        super(Weather, self).__init__(
            [
                "Sun(ny|shine)?",
                "rain(ing)?",
                "Snow(ing|fall)?",
                "Fog(gy)",
                "Sleet(ing)?"

            ]
        )


class ExtremeWeather(NewsTopic):
    def __init__(self):
        super(ExtremeWeather, self).__init__(
            [
                "thunder storm",
                "heat wave",
                "(tropical)? cyclone",
                "tornado",
                "hurricane",
                "flash flood",
                "drought"

            ], [
                "thunder",
                "storm",
                "flood"
            ]
        )


class Geology(NewsTopic):
    def __init__(self):
        super(Geology, self).__init__([
            "Earthquake",
            "Tsunami",
            "Volcano",
            "Avalanche",
            "landslide"
        ])


def get():
    return [
        BadThings(),
        Weather(),
        ExtremeWeather(),
        Geology(),
        CivilRights()
    ]
