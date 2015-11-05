from twitterpibot.twitter.topics.Topic import Topic


class BadThings(Topic):
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
                "(child|sex) abuse"

            ], [
                "fire",
                "dead",
                "suspect(ed)",
                "abuse"
            ], retweet=True
        )


class Weather(Topic):
    def __init__(self):
        super(Weather, self).__init__(
            [
                "Sun(ny|shine)?",
                "rain(ing)?",
                "Snow(ing|fall)?",
                "Fog(gy)",
                "Sleet(ing)?"

            ], retweet=True
        )


class ExtremeWeather(Topic):
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
            ], retweet=True
        )


class Geology(Topic):
    def __init__(self):
        super(Geology, self).__init__([
            "Earthquake",
            "Tsunami",
            "Volcano",
            "Avalanche",
            "landslide"
        ],
            retweet=True
        )


def get():
    return [
        BadThings(),
        Weather(),
        ExtremeWeather(),
        Geology()
    ]
