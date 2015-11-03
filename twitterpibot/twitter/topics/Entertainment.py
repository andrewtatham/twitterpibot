from twitterpibot.twitter.topics.Topic import Topic

__author__ = 'andrewtatham'


class XFactor(Topic):
    def __init__(self):
        super(XFactor, self).__init__([
            "XFactor"
        ])


class StrictlyComeDancing(Topic):
    def __init__(self):
        super(StrictlyComeDancing, self).__init__([
            "#Strictly",
            "strictly come dancing"
        ], [
            "Strictly"
        ])


class DrWho(Topic):
    def __init__(self):
        super(DrWho, self).__init__([
            "(Dr|Doctor) Who",
        ], [
            "The (Dr|Doctor)"
        ])


class MostHaunted(Topic):
    def __init__(self):
        super(MostHaunted, self).__init__([
            "Most Haunted"
        ])


class MatchOfTheDay(Topic):
    def __init__(self):
        super(MatchOfTheDay, self).__init__([
            "Match of the Day", "MOTD"
        ])


class AndrewMarrShow(Topic):
    def __init__(self):
        super(AndrewMarrShow, self).__init__([
            "Andrew Marr", r"\bmarr\b"
        ])


class TheArchers(Topic):
    def __init__(self):
        super(TheArchers, self).__init__([
            "#TheArchers"
        ])


def get():
    return [
        XFactor(),
        StrictlyComeDancing(),
        DrWho(),
        MostHaunted(),
        MatchOfTheDay(),
        AndrewMarrShow(),
        TheArchers()
    ]
