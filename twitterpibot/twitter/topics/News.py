from twitterpibot.twitter.topics.Topic import Topic


class BadThings(Topic):
    def __init__(self):
        super(BadThings, self).__init__(
            [
                "Shooting",
                "Gunman",
                "Fatal",
                "wound",
                "victim",
                "murder",
                "suicide",
                "peadophile",
                "terror",
                "stab",
                "bomb",
                "explosion",
                "fire",
                "crash",
                "isil",
                "isis",
                "kninfed",
                "dead",
                "suspect"

            ], retweet=True
        )


class Weather(Topic):
    def __init__(self):
        super(Weather, self).__init__(
            ["Sun(ny)?", "rain(ing)?", "Snow(ing)?", "Fog(gy)", "Sleet(ing)?"], retweet=True
        )


class Geology(Topic):
    def __init__(self):
        super(Geology, self).__init__(
            ["Earthquake", "Volcano", "landslide"], retweet=True
        )


def get():
    return [
        BadThings(),
        Weather(),
        Geology()
    ]
