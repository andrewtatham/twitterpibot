from twitterpibot.topics.Topic import NewsTopic, IgnoreTopic, GoodTopic


class NewYear(NewsTopic):
    def __init__(self):
        super(NewYear, self).__init__(
            {"New Year"},
            on_date="01/01",
            on_date_range=7)


class GroundhogDay(NewsTopic):
    def __init__(self):
        super(GroundhogDay, self).__init__(
            {"Groundhog", "Punxsutawney", "Bill Murray"},
            on_date="02/02",
            on_date_range=2)


class PancakeDay(NewsTopic):
    def __init__(self):
        super(PancakeDay, self).__init__(
            ["Pancake"],
            from_date="01/02",
            to_date="15/02")


class ValentinesDay(NewsTopic):
    def __init__(self):
        super(ValentinesDay, self).__init__(
            {"Valentines?"},
            on_date="14/02",
            on_date_range=2)


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
            to_date="01/05")


class YorkshireDay(GoodTopic):
    def __init__(self):
        super(YorkshireDay, self).__init__(
            {"Yorkshire Day?"},
            on_date="01/08",
            on_date_range=2)


class Halloween(NewsTopic):
    def __init__(self):
        super(Halloween, self).__init__(
            ["Halloween", "trick or treat"],
            ["ghost", "fright", "spook", "trick", "treat", "pumpkin"],
            on_date="31/10",
            on_date_range=7
        )


class BonfireNight(GoodTopic):
    def __init__(self):
        super(BonfireNight, self).__init__(
            ["Bonfire", "Firework", "Guy Fawkes", "5th of Nov(ember)?"],
            ["sparkler", "rocket"],
            on_date="05/11",
            on_date_range=7
        )


class RemembranceSunday(GoodTopic):
    def __init__(self):
        super(RemembranceSunday, self).__init__(
            ["Remembrance Sunday"],
            on_date="11/11",
            on_date_range=7
        )


class VeteransDay(NewsTopic):
    def __init__(self):
        super(VeteransDay, self).__init__(
            ["Veterans Day"],
            on_date="11/11",
            on_date_range=7
        )


class Diwali(GoodTopic):
    def __init__(self):
        super(Diwali, self).__init__(
            {"Di(w|v)ali", "Deepavali"},
            from_date="7/10",
            to_date="21/11")


class Thanksgiving(IgnoreTopic):
    def __init__(self):
        super(Thanksgiving, self).__init__(
            {"Thanksgiving", "Turkey"},
            from_date="21/11",
            to_date="28/11")


class BlackFriday(IgnoreTopic):
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
        GroundhogDay(),
        PancakeDay(),
        ValentinesDay(),
        Easter(),

        YorkshireDay(),

        Halloween(),
        BonfireNight(),
        RemembranceSunday(),
        VeteransDay(),
        Diwali(),
        Thanksgiving(),
        BlackFriday(),
        Christmas()
    ]
