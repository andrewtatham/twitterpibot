from unittest import TestCase

from twitterpibot.twitter.topics.News import Weather


class TestWeather(TestCase):
    def test_condition(self):

        topic = Weather()
        testcases = [
            ("rain", "definite_matches"),
            ("raining", "definite_matches"),
            ("train", None),
            ("training", None)
        ]
        for testcase in testcases:
            actual = topic.condition(testcase[0])

            print("testcase actual", testcase, actual)
            if testcase[1]:
                self.assertIsNotNone(actual)
                self.assertTrue(testcase[0] in actual[testcase[1]])
            else:
                self.assertIsNone(actual)
