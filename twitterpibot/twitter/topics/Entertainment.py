from twitterpibot.twitter.topics.Topic import DontCareTopic

__author__ = 'andrewtatham'


class XFactor(DontCareTopic):
    def __init__(self):
        super(XFactor, self).__init__([
            "XFactor"
        ])


class StrictlyComeDancing(DontCareTopic):
    def __init__(self):
        super(StrictlyComeDancing, self).__init__([
            "#Strictly",
            "strictly come dancing"
        ], [
            "Strictly"
        ])


class DrWho(DontCareTopic):
    def __init__(self):
        super(DrWho, self).__init__([
            "(Dr|Doctor) Who",
        ], [
            "The (Dr|Doctor)"
        ])


class MostHaunted(DontCareTopic):
    def __init__(self):
        super(MostHaunted, self).__init__([
            "Most Haunted"
        ])


class MatchOfTheDay(DontCareTopic):
    def __init__(self):
        super(MatchOfTheDay, self).__init__([
            "Match of the Day", "MOTD"
        ])


class AndrewMarrShow(DontCareTopic):
    def __init__(self):
        super(AndrewMarrShow, self).__init__([
            "Andrew Marr"
        ], ["marr"])


class TheArchers(DontCareTopic):
    def __init__(self):
        super(TheArchers, self).__init__([
            "#TheArchers"
        ])


class AtMidnight(DontCareTopic):
    def __init__(self):
        super(AtMidnight, self).__init__([
            "@Midnight", "#[\w]+in[\d]+words?"
        ])


class WWE(DontCareTopic):
    def __init__(self):
        super(WWE, self).__init__([
            "WWE"
        ])


def get():
    return [
        XFactor(),
        StrictlyComeDancing(),
        DrWho(),
        MostHaunted(),
        MatchOfTheDay(),
        AndrewMarrShow(),
        TheArchers(),
        AtMidnight(),
        WWE()
    ]
