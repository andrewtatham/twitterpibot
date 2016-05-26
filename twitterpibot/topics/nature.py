from twitterpibot.topics.Topic import GoodTopic


class Goats(GoodTopic):
    def __init__(self):
        super(Goats, self).__init__({
            "goats?",

        })


def get():
    return [
        Goats()
    ]
