from twitterpibot.twitter.topics.Topic import NewsTopic, DontCareTopic


class NewYear(NewsTopic):
    def __init__(self):
        super(NewYear, self).__init__({"New Year"},
                                      on_date="01/01",
                                      on_date_range=7)


class Easter(NewsTopic):
    def __init__(self):
        super(Easter, self).__init__({
            "Easter",
            "Maundy Thursday",
            "Good Friday",
            "Holy Saturday",
            "Palm Sunday"
        },
            from_date="01/03",
            to_date="31/04")


class Halloween(NewsTopic):
    def __init__(self):
        super(Halloween, self).__init__(
            ["Halloween", "trick or treat"],
            ["ghost", "fright", "spook", "trick", "treat", "pumpkin"],
            on_date="31/10",
            on_date_range=7
        )


class BonfireNight(NewsTopic):
    def __init__(self):
        super(BonfireNight, self).__init__(
            ["Bonfire", "Firework", "Guy Fawkes", "5th of Nov(ember)?"],
            ["sparkler", "rocket"],
            on_date="05/11",
            on_date_range=7
        )


class RemembranceSunday(NewsTopic):
    def __init__(self):
        super(RemembranceSunday, self).__init__(
            ["Remembrance Sunday"],
            on_date="11/11",
            on_date_range=7
        )


class Thanksgiving(DontCareTopic):
    def __init__(self):
        super(Thanksgiving, self).__init__(
            {"Thanksgiving", "Turkey"},
            from_date="21/11",
            to_date="28/11")


class BlackFriday(DontCareTopic):
    def __init__(self):
        super(BlackFriday, self).__init__(
            {"Black Friday"},
            from_date="21/11",
            to_date="01/12")


class Christmas(NewsTopic):
    def __init__(self):
        super(Christmas, self).__init__({"Christmas", "Xmas"},
                                        from_date="21/12",
                                        to_date="31/12")


def get():
    return [
        NewYear(),
        Easter(),
        Halloween(),
        BonfireNight(),
        RemembranceSunday(),
        Thanksgiving(),
        BlackFriday(),
        Christmas()
    ]
