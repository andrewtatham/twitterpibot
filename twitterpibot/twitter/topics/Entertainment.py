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
            "D(octo)?r Who",
        ], [
            "The Doctor"
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
def get():
    return [
        XFactor(),
        StrictlyComeDancing(),
        DrWho(),
        MostHaunted(),
        MatchOfTheDay()
    ]
