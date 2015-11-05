from twitterpibot.twitter.topics.Topic import DontCareTopic

__author__ = 'Andrew'


class MondayMotivation(DontCareTopic):
    def __init__(self):
        super(MondayMotivation, self).__init__(["Monday Motivation"])


class FollowFriday(DontCareTopic):
    def __init__(self):
        super(FollowFriday, self).__init__(["#FF", "#FollowFriday"])


class FridayFeeling(DontCareTopic):
    def __init__(self):
        super(FridayFeeling, self).__init__(["#FridayFeeling"])


class SuperSunday(DontCareTopic):
    def __init__(self):
        super(SuperSunday, self).__init__(["Super Sunday"])


def get():
    return [
        MondayMotivation(),

        FollowFriday(), FridayFeeling(),
        SuperSunday()
    ]
