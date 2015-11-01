from unittest import TestCase
from twitterpibot.twitter.topics.Sport import SportOther

__author__ = 'Andrew'


class TestSportOther(TestCase):
    def test_condition(self):
        topic = SportOther()
        testcases = [("#TMAvsTMB", True),
                     ("#TraVelodge", False)]
        for testcase in testcases:
            actual = topic.condition(testcase[0])
        if testcase[1]:
            self.assertTrue(actual)
        else:
            self.assertIsNone(actual)


