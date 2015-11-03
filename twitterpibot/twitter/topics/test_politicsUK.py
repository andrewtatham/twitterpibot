from unittest import TestCase
from twitterpibot.twitter.topics.Politics import PoliticsUK

__author__ = 'andrewtatham'


class TestPoliticsUK(TestCase):
    def test_condition(self):

        topic = PoliticsUK()
        testcases = [
            ("Prime Minister", "definite_matches"),
            ("Prime Number", None)
        ]
        for testcase in testcases:
            actual = topic.condition(testcase[0])

            print("testcase actual", testcase, actual)
            if testcase[1]:
                self.assertTrue(testcase[0] in actual[testcase[1]])
            else:
                self.assertIsNone(actual)
