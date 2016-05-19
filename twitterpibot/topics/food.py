from twitterpibot.topics.Topic import GoodTopic


class GoodFood(GoodTopic):
    def __init__(self):
        super(GoodFood, self).__init__({
            "peanut butter",
            "cookies?",
            "ice cream",
            "realbread",
            "pizza",

        })


def get():
    return [
        GoodFood(),

    ]
