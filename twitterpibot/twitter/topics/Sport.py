from twitterpibot.twitter.topics.Topic import Topic


class SportOther(Topic):
    def __init__(self):
        super(SportOther, self).__init__([
            "#[]v[]"

        ])

def get():
    return [
        # TODO

        SportOther()
    ]
