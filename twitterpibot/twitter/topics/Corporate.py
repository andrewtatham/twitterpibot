from twitterpibot.twitter.topics.Topic import Topic


class DecsAndLondon(Topic):
    def __init__(self):
        super(DecsAndLondon, self).__init__({"DecsAndLondon", "#DoItLikeItsLegal"})


class Starbucks(Topic):
    def __init__(self):
        super(Starbucks, self).__init__(
            {"Pumpkin Spice(d) Latte", "PSL", "Red Cups", "(Eggnog|Gingerbread) Latte", "Eggnog Latte"})


def get():
    return [
        Starbucks(),
        DecsAndLondon()
    ]
