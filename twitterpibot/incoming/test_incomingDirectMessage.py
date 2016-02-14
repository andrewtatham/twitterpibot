from unittest import TestCase
from twitterpibot.incoming.IncomingDirectMessage import IncomingDirectMessage

__author__ = 'Andrew'


class TestIncomingDirectMessage(TestCase):
    def test_ctor(self):
        self.assertIsNotNone(IncomingDirectMessage({}, None))
