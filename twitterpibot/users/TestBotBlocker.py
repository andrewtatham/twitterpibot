from unittest import TestCase

from twitterpibot.users import BotBlocker
from twitterpibot.users.BotBlocker import _is_user_bot
from twitterpibot.users.User import User

__author__ = 'andrewtatham'


class TestBotBlocker(TestCase):
    def test_check_user(self):
        testcases = [
            ({}, [], False),
            ({"screen_name": "xxx"}, [], True),
            ({"description": "follow me"}, [], True),

            # Tweets
            ({}, [{"text": "blah"}], False),
            ({}, [{"text": "boobs"}], True)
        ]

        for testcase in testcases:
            # 'Monkey patch' function to get users tweets
            BotBlocker.get_tweets = lambda user: testcase[1]

            block, reasons = _is_user_bot(User(testcase[0]))

            self.assertEqual(block, testcase[2])
