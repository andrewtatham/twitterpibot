from twitterpibot.twitter.topics.Topic import Topic


class Halloween(Topic):
    def __init__(self):
        super(Halloween, self).__init__(
            ["Halloween", "trick or treat"],
            ["ghost", "fright", "spook", "trick", "treat", "pumpkin"],
            from_date="25/10",
            to_date="01/11")
class BonfireNight(Topic):
    def __init__(self):
        super(BonfireNight, self).__init__(
            ["Bonfire", "Firework", "Guy Fawkes"],
            ["sparkler","rocket"],
            on_date="25/10",
            on_date_range = 7
            )

def get():
    return [
        Halloween(),
        BonfireNight()
    ]
