from twitterpibot.topics.Topic import IgnoreTopic


class XFactor(IgnoreTopic):
    def __init__(self):
        super(XFactor, self).__init__([
            "XFactor"
        ])


class StrictlyComeDancing(IgnoreTopic):
    def __init__(self):
        super(StrictlyComeDancing, self).__init__([
            "#Strictly",
            "strictly come dancing"
        ], [
            "Strictly"
        ])


class DrWho(IgnoreTopic):
    def __init__(self):
        super(DrWho, self).__init__([
            "(Dr|Doctor) Who",
        ], [
            "The (Dr|Doctor)"
        ])


class MostHaunted(IgnoreTopic):
    def __init__(self):
        super(MostHaunted, self).__init__([
            "Most Haunted"
        ])


class MatchOfTheDay(IgnoreTopic):
    def __init__(self):
        super(MatchOfTheDay, self).__init__([
            "Match of the Day", "MOTD"
        ])


class AndrewMarrShow(IgnoreTopic):
    def __init__(self):
        super(AndrewMarrShow, self).__init__([
            "Andrew Marr"
        ], ["marr"])


class TheArchers(IgnoreTopic):
    def __init__(self):
        super(TheArchers, self).__init__([
            "#TheArchers"
        ])


class AtMidnight(IgnoreTopic):
    def __init__(self):
        super(AtMidnight, self).__init__([
            "@Midnight", "#[\w]+in[\d]+words?"
        ])


class WWE(IgnoreTopic):
    def __init__(self):
        super(WWE, self).__init__([
            "WWE"
        ])


class ImACelbrityGetMeOutOfHere(IgnoreTopic):
    def __init__(self):
        super(ImACelbrityGetMeOutOfHere, self).__init__([
            "I'?m a celeb"
        ], [
            "jungle"
        ])


class TheApprentice(IgnoreTopic):
    def __init__(self):
        super(TheApprentice, self).__init__([
            "The Apprentice", "(lord|alan) sugar"
        ], [
            "apprentice"
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
        WWE(),
        ImACelbrityGetMeOutOfHere(),
        TheApprentice()
    ]
