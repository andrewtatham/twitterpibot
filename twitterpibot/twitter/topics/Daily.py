from twitterpibot.twitter.topics.Topic import DontCareTopic

__author__ = 'Andrew'


class MondayMotivation(DontCareTopic):
    def __init__(self):
        super(MondayMotivation, self).__init__(["Monday Motivation"])


class TuesdayTreats(DontCareTopic):
    def __init__(self):
        super(TuesdayTreats, self).__init__(["Tuesday Treats?"])


class WednesdayWisdom(DontCareTopic):
    def __init__(self):
        super(WednesdayWisdom, self).__init__(["Wednesday Wisdom"])


class ThursdayThoughts(DontCareTopic):
    def __init__(self):
        super(ThursdayThoughts, self).__init__(["Thursday Thoughts?"])


class FollowFriday(DontCareTopic):
    def __init__(self):
        super(FollowFriday, self).__init__(["#FF", "Follow Friday"])


class FridayFeeling(DontCareTopic):
    def __init__(self):
        super(FridayFeeling, self).__init__(["#FridayFeeling"])


class SuperSunday(DontCareTopic):
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
