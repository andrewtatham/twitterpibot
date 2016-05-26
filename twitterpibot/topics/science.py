from twitterpibot.topics.Topic import GoodTopic


class Magnets(GoodTopic):
    def __init__(self):
        super(Magnets, self).__init__({
            "magnet(s|ism)?",

        })


def get():
    return [
        Magnets()
    ]
