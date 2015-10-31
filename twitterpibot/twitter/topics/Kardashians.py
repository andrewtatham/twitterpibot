from twitterpibot.twitter.topics.Topic import Topic


class Kardashians(Topic):
    def __init__(self):
        super(Kardashians, self).__init__([
            "Kardashian",
            "Kim",
            "Khloe",
            "Kourtney",
            "Kylie",
            "Kendall",
            "Caitlyn",
            "Jenner"

        ])

