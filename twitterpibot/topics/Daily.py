from twitterpibot.topics.Topic import IgnoreTopic

__author__ = 'Andrew'


class MondayMotivation(IgnoreTopic):
    def __init__(self):
        super(MondayMotivation, self).__init__(["Monday Motivation"])


class TuesdayTreats(IgnoreTopic):
    def __init__(self):
        super(TuesdayTreats, self).__init__(["Tuesday Treats?"])


class WednesdayWisdom(IgnoreTopic):
    def __init__(self):
        super(WednesdayWisdom, self).__init__(["Wednesday Wisdom"])


class ThursdayThoughts(IgnoreTopic):
    def __init__(self):
        super(ThursdayThoughts, self).__init__(["Thursday Thoughts?"])


class FollowFriday(IgnoreTopic):
    def __init__(self):
        super(FollowFriday, self).__init__(["#FF", "Follow Friday"])


class FridayFeeling(IgnoreTopic):
    def __init__(self):
        super(FridayFeeling, self).__init__(["#FridayFeeling"])


class SuperSunday(IgnoreTopic):
    def __init__(self):
        super(SuperSunday, self).__init__(["Super Sunday"])


def get():
    return [
        MondayMotivation(),
        TuesdayTreats(),
        WednesdayWisdom(),
        ThursdayThoughts(),
        FollowFriday(), FridayFeeling(),
        SuperSunday()
    ]
