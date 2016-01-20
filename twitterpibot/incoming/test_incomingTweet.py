from unittest import TestCase
from twitterpibot.incoming.IncomingTweet import IncomingTweet

__author__ = 'Andrew'


class TestIncomingTweet(TestCase):
    def test_ctor(self):
        self.assertIsNotNone(IncomingTweet({}))

