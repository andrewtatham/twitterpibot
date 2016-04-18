from twitterpibot.topics.Topic import NewsTopic, IgnoreTopic


class BadThings(IgnoreTopic):
    def __init__(self):
        super(BadThings, self).__init__(
            [
                "Shooting",
                "Gunman",
                "Fatal(y|ites)?",
                "wound(ed)?",
                "victims?",
                "murder(s|er|ed)?",
                "suicide",
                "peadophil(e|es|ic)?",
                "terror(ist|ism)?",
                "stab(bed|bing)?",
                "bomb(s)?",
                "explosion(s)?",
                "crash",
                "taliban",
                "isil",
                "isis",
                "jihad(ist)?s?"
                "knife(d)?",
                "arson",
                "(child|sex) abuse",
                "rap(e|ed|ist|ing)'",
                "RIP",
                "drone strike",
                "hitler",
                "holocaust",
                "nazi",
                "injure(s|ed|ies)",
                "miscarriage",
                "trafficking",
                "abortion",
                "died"

            ], [
                "fire",
                "dea(d|th)",
                "suspect(s|ed)?",
                "abuse",
                "Adolf",
                "arrest",
                "attack",
                "violen(t|ce)"
            ]
        )


class CivilRights(NewsTopic):
    def __init__(self):
        super(CivilRights, self).__init__(
            [
                "BlackLivesMatter",
                "LGBT?",
                "(gay|Black) people",
                "homophobi(a|c)"

            ])


class Weather(IgnoreTopic):
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
