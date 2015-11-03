from twitterpibot.twitter.topics.Topic import Topic

__author__ = 'Andrew'


class MondayMotivation(Topic):
    def __init__(self):
        super(MondayMotivation, self).__init__(["Monday Motivation"])


class FollowFriday(Topic):
    def __init__(self):
        super(FollowFriday, self).__init__(["#FF", "#FollowFriday"])


class FridayFeeling(Topic):
    def __init__(self):
        super(FridayFeeling, self).__init__(["#FridayFeeling"])


class SuperSunday(Topic):
    def __init__(self):
        super(SuperSunday, self).__init__(["Super Sunday"])


def get():
    return [
        MondayMotivation(),

        FollowFriday(), FridayFeeling(),
        SuperSunday()
    ]
