from twitterpibot.twitter.topics.Topic import GoodTopic


class Leeds(GoodTopic):
    def __init__(self):
        super(Leeds, self).__init__(
            ["Leeds"]
        )


def get():
    return [
        Leeds()
    ]
