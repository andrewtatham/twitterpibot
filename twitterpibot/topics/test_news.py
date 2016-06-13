from unittest import TestCase

from twitterpibot.topics.News import BadThings


class TestBadThings(TestCase):
    def test_condition(self):

        topic = BadThings()
        testcases = [
            ("ISIS", "definite_matches"),
            ("Shooting", "definite_matches"),
            ("Shooter", "definite_matches"),
            ("AR-15", "definite_matches"),
            ("M16", "definite_matches"),
        ]
        for testcase in testcases:
            with self.subTest(testcase):
                actual = topic.condition(testcase[0])

                print("testcase actual", testcase, actual)
                if testcase[1]:
                    self.assertIsNotNone(actual)
                    print(actual["definite_matches"])
                    self.assertTrue(testcase[0] in actual[testcase[1]])
                else:
                    self.assertIsNone(actual)
