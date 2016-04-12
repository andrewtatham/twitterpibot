from twitterpibot.topics.Topic import GoodTopic, IgnoreTopic


class Leeds(GoodTopic):
    def __init__(self):
        super(Leeds, self).__init__(
            ["Leeds"]
        )


class Yorkshire(GoodTopic):
    def __init__(self):
        super(Yorkshire, self).__init__(
            ["Yorkshire"]
        )


class London(IgnoreTopic):
    def __init__(self):
        super(London, self).__init__(
            ["London", "LDN"]
        )


class Europe(IgnoreTopic):
    def __init__(self):
        super(Europe, self).__init__(
            ["Europe", "European", "EU"]
        )


def get():
    return [
        Leeds(),
        Yorkshire(),
        London(),
        Europe()
    ]
