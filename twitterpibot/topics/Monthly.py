from twitterpibot.topics.Topic import NewsTopic

_months = [
    "Jan(uary)",
    "Feb(ruary)",
    "Mar(ch)",
    "Apr(il)",
    "May",
    "Jun(e)",
    "Jul(y)",
    "Aug(ust)",
    "Nov(ember)",
    "Dec(ember)"
]


class FirstOfMonth(NewsTopic):
    def __init__(self):
        super(FirstOfMonth, self).__init__(
            ["Happy New Month", "(first|1(st)) of (%s)".format("|".join(_months))]
        )


class Movember(NewsTopic):
    def __init__(self):
        super(Movember, self).__init__(
            ["Movember"]
        )


def get():
    return [
        FirstOfMonth(),
        Movember()
    ]
