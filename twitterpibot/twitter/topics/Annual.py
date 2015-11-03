from twitterpibot.twitter.topics.Topic import Topic


class NewYear(Topic):
    def __init__(self):
        super(NewYear, self).__init__({"New Year"},
                                      on_date="01/01",
                                      on_date_range=7)


class Easter(Topic):
    def __init__(self):
        super(Easter, self).__init__({"Easter", "Maundy Thursday", "Good Friday", "Holy Saturday", "Palm Sunday"},
                                     from_date="01/03",
                                     to_date="31/04")


class Halloween(Topic):
    def __init__(self):
        super(Halloween, self).__init__(
            ["Halloween", "trick or treat"],
            ["ghost", "fright", "spook", "trick", "treat", "pumpkin"],
            on_date="31/10",
            on_date_range=7
        )


class AllSaintsDay(Topic):
    def __init__(self):
        super(AllSaintsDay, self).__init__(
            ["All Saints Day"],
            on_date="01/11"
        )


class BonfireNight(Topic):
    def __init__(self):
        super(BonfireNight, self).__init__(
            ["Bonfire", "Firework", "Guy Fawkes"],
            ["sparkler", "rocket"],
            on_date="25/10",
            on_date_range=7
        )


class Christmas(Topic):
    def __init__(self):
        super(Christmas, self).__init__({"Christmas", "Xmas"})


def get():
    return [
        NewYear(),
        Easter(),
        Halloween(),
        BonfireNight(),
        Christmas()
    ]
