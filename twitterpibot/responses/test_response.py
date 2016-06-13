from unittest import TestCase

from twitterpibot.responses.Response import favourite_condition, retweet_condition, mentioned_reply_condition, \
    unmentioned_reply_condition, _one_in
from twitterpibot.topics.News import BadThings

__author__ = 'andrewtatham'


class TestResponse(TestCase):
    def test_mentioned_reply_condition(self):
        test_data = _get_test_data(to_me=True)
        # noinspection PyTypeChecker
        rate = _test_reply_rate(mentioned_reply_condition, test_data=test_data)
        self.assertGreaterEqual(rate, 0.99)

    def test_unmentioned_reply_condition(self):
        test_data = _get_test_data()
        # noinspection PyTypeChecker
        rate = _test_reply_rate(unmentioned_reply_condition, test_data=test_data)
        self.assertLessEqual(rate, 0.01)

    def test_retweet_condition(self):
        test_data = _get_test_data()
        # noinspection PyTypeChecker
        rate = _test_reply_rate(retweet_condition, test_data=test_data)
        self.assertLessEqual(rate, 0.01)

    def test_favourite_condition(self):
        test_data = _get_test_data()
        # noinspection PyTypeChecker
        rate = _test_reply_rate(favourite_condition, test_data=test_data)
        self.assertLessEqual(rate, 0.01)


class TestResponseBadThings(TestCase):
    def test_mentioned_reply_condition(self):
        test_data = _get_test_data(to_me=True, topic=BadThings())
        # noinspection PyTypeChecker
        rate = _test_reply_rate(mentioned_reply_condition, test_data=test_data)
        self.assertEqual(rate, 0)

    def test_unmentioned_reply_condition(self):
        test_data = _get_test_data(topic=BadThings())
        # noinspection PyTypeChecker
        rate = _test_reply_rate(unmentioned_reply_condition, test_data=test_data)
        self.assertEqual(rate, 0)

    def test_retweet_condition(self):
        test_data = _get_test_data(topic=BadThings())
        # noinspection PyTypeChecker
        rate = _test_reply_rate(retweet_condition, test_data=test_data)
        self.assertEqual(rate, 0)

    def test_favourite_condition(self):
        test_data = _get_test_data(topic=BadThings())
        # noinspection PyTypeChecker
        rate = _test_reply_rate(favourite_condition, test_data=test_data)
        self.assertEqual(rate, 0)


def _get_test_data(to_me=False, topic=None):
    for i in range(10000):
        inbox_item = MockInboxItem()
        inbox_item.is_direct_message = _one_in(1000)
        inbox_item.is_tweet = not inbox_item.is_direct_message
        if to_me:
            inbox_item.to_me = True
        else:
            inbox_item.to_me = _one_in(1000)

        inbox_item.from_me = _one_in(1000)

        inbox_item.favorited = _one_in(100)
        inbox_item.retweeted = _one_in(100)
        inbox_item.is_retweet_of_my_status = _one_in(1000)
        if inbox_item.retweeted:
            inbox_item.retweeted_status = MockInboxItem()
            inbox_item.retweeted_status.favorited = _one_in(100)
            inbox_item.retweeted_status.retweeted = _one_in(100)
        else:
            inbox_item.retweeted_status = None

        inbox_item.sender = MockInboxItem()
        inbox_item.sender.screen_name = ""

        inbox_item.sender.is_awesome_bot = _one_in(100)
        inbox_item.sender.is_possibly_bot = _one_in(100)
        inbox_item.sender.is_friend = _one_in(100)
        inbox_item.sender.is_arsehole = _one_in(100)
        inbox_item.sender.is_retweet_more = _one_in(100)
        inbox_item.sender.is_do_not_retweet = _one_in(100)
        inbox_item.sender.is_reply_less = _one_in(100)

        inbox_item.sender.protected = _one_in(100)

        inbox_item.topics = topic
        inbox_item.sourceIsTrend = _one_in(100)
        inbox_item.sourceIsSearch = _one_in(100)
        yield inbox_item


def _test_reply_rate(condition, test_data):
    results = list(map(condition, test_data))
    responses = sum(results)
    total = len(results)
    rate = responses / total
    print("{} {} of {}, {}".format(condition.__name__, responses, total, rate))
    return rate


class MockInboxItem(object):
    pass
