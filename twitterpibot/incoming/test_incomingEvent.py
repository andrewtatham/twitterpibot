from unittest import TestCase
from twitterpibot.incoming.IncomingEvent import IncomingEvent

__author__ = 'Andrew'


class TestIncomingEvent(TestCase):
    def test_ctor(self):
        self.assertIsNotNone(IncomingEvent({}))