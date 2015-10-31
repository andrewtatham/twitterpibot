from unittest import TestCase
from twitterpibot.twitter.topics.Sport import SportOther

__author__ = 'Andrew'


class TestSportOther(TestCase):
    def test_condition(self):
        topic = SportOther()
        self.assertTrue(topic.condition("#TMAvsTMB"))
