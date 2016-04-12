from unittest import TestCase

from twitterpibot.topics.Politics import PoliticsUK


class TestPoliticsUK(TestCase):
    def test_condition(self):

        topic = PoliticsUK()
        testcases = [
            ("Prime Minister", "definite_matches"),
            ("Prime Number", None),
            ("tory", "definite_matches"),
            ("conservatory", None),
            ("tories", "definite_matches")
        ]
        for testcase in testcases:
            actual = topic.condition(testcase[0])

            print("testcase actual", testcase, actual)
            if testcase[1]:
                self.assertIsNotNone(actual)
                print(actual["definite_matches"])
                self.assertTrue(testcase[0] in actual[testcase[1]])
            else:
                self.assertIsNone(actual)
