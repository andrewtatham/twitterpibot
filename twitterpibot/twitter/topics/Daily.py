from twitterpibot.twitter.topics.Topic import Topic

__author__ = 'Andrew'


class FollowFriday(Topic):
    def __init__(self):
        super(FollowFriday, self).__init__(["#FF", "#FollowFriday"])


class FridayFeeling(Topic):
    def __init__(self):
        super(FridayFeeling, self).__init__(["#FridayFeeling"])


def get():
    return [FollowFriday(), FridayFeeling()]
