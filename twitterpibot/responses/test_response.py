from unittest import TestCase

from twitterpibot.responses.Response import favourite_condition, retweet_condition, mentioned_reply_condition, \
    unmentioned_reply_condition, one_in

__author__ = 'andrewtatham'


class TestResponse(TestCase):
    def test_mentioned_reply_condition(self):
        rate = _test_reply_rate(mentioned_reply_condition, True)
        self.assertGreaterEqual(rate, 0.99)

    def test_unmentioned_reply_condition(self):
        rate = _test_reply_rate(unmentioned_reply_condition)
        self.assertLessEqual(rate, 0.01)

    def test_retweet_condition(self):
        rate = _test_reply_rate(retweet_condition)
        self.assertLessEqual(rate, 0.01)

    def test_favourite_condition(self):
        rate = _test_reply_rate(favourite_condition)
        self.assertLessEqual(rate, 0.01)


def _get_test_data(to_me=False):
    for i in range(10000):
        inbox_item = MockInboxItem()
        inbox_item.is_direct_message = one_in(1000)
        inbox_item.is_tweet = not inbox_item.is_direct_message
        if to_me:
            inbox_item.to_me = True
        else:
            inbox_item.to_me = one_in(1000)

        inbox_item.from_me = one_in(1000)

        inbox_item.favorited = one_in(100)
        inbox_item.retweeted = one_in(100)
        inbox_item.is_retweet_of_my_status = one_in(1000)
        if inbox_item.retweeted:
            inbox_item.retweeted_status = MockInboxItem()
            inbox_item.retweeted_status.favorited = one_in(100)
            inbox_item.retweeted_status.retweeted = one_in(100)
        else:
            inbox_item.retweeted_status = None

        inbox_item.sender = MockInboxItem()
        inbox_item.sender.screen_name = ""

        inbox_item.sender.is_bot = one_in(100)
        inbox_item.sender.is_friend = one_in(100)
        inbox_item.sender.is_arsehole = one_in(100)
        inbox_item.sender.is_retweet_more = one_in(100)
        inbox_item.sender.is_do_not_retweet = one_in(100)
        inbox_item.sender.is_reply_less = one_in(100)

        inbox_item.sender.protected = one_in(100)

        inbox_item.topics = None
        inbox_item.sourceIsTrend = one_in(100)
        inbox_item.sourceIsSearch = one_in(100)
        yield inbox_item


def _test_reply_rate(condition, to_me=False):
    test_data = _get_test_data(to_me)
    results = list(map(condition, test_data))
    responses = sum(results)
    total = len(results)
    rate = responses / total
    print("{} {} of {}, {}".format(condition.__name__, responses, total, rate))
    return rate


class MockInboxItem(object):
    pass
