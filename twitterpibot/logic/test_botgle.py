import pprint
from unittest import TestCase

from twitterpibot.logic.botgle import solve_board
from twitterpibot.logic.botgle_solver import parse_board, solve_board

__author__ = 'andrewtatham'


class Test_Parse_Board(TestCase):
    def test_parse_board(self):
        testcases = [
            {
                "tweet": """blah:
                    　Ｘ　　Ｅ　　Ｉ　　Ｕ　
                    　Ｑｕ　Ｔ　　Ｄ　　Ｊ　
                    　Ｓ　　Ｎ　　Ｏ　　Ｅ　
                    　Ｏ　　Ｆ　　Ｒ　　Ｄ　
                    blah""",
                "board": [
                    ['X', 'E', 'I', 'U'],
                    ['QU', 'T', 'D', 'J'],
                    ['S', 'N', 'O', 'E'],
                    ['O', 'F', 'R', 'D']
                ]
            },
            {
                "tweet": """The only thing blocking you from total victory is this Boggle board:

                    　Ｙ　　Ｂ　　Ｎ　　Ｏ　
                    　Ｔ　　Ｅ　　Ｈ　　Ｉ　
                    　Ｆ　　Ｏ　　Ａ　　Ｒ　
                    　Ｒ　　Ｒ　　Ａ　　Ｎ　

                    """,
                "board": [
                    ['Y', 'B', 'N', 'O'],
                    ['T', 'E', 'H', 'I'],
                    ['F', 'O', 'A', 'R'],
                    ['R', 'R', 'A', 'N']
                ]
            }
        ]

        for testcase in testcases:
            with self.subTest(testcase=testcase):
                actual = parse_board(testcase["tweet"])
                self.assertEqual(actual, testcase["board"])


class Test_Solve_Board(TestCase):
    def test_solve_board(self):

        testcases = [
            dict(board=[
                ['X', 'E', 'I', 'U'],
                ['QU', 'T', 'D', 'J'],
                ['S', 'N', 'O', 'E'],
                ['O', 'F', 'R', 'D']],
                expected_words=[
                    "NOD",
                ], unexpected_words=[
                    "UNFREQUENTEDNESS",  # adjacency
                    "TOROTORO"  # duplicate
                ]),
            dict(board=[
                ['Y', 'B', 'N', 'O'],
                ['T', 'E', 'H', 'I'],
                ['F', 'O', 'A', 'R'],
                ['R', 'R', 'A', 'N']
            ])
        ]
        for testcase in testcases:
            with self.subTest(testcase=testcase):
                self._solve(testcase)

    def _solve(self, testcase):
        solutions = solve_board(testcase["board"])
        pprint.pprint(solutions)
        self.assertTrue(solutions)

        words = list(solutions)
        print("%s words found..." % len(words))
        words.sort(key = len)
        words = words[-12:]
        words.reverse()
        pprint.pprint(words)


        if "expected_words" in testcase:
            for expected_word in testcase["expected_words"]:
                with self.subTest(expected_word=expected_word):
                    self.assertIn(expected_word, solutions)
        if "unexpected_words" in testcase:
            for unexpected_word in testcase["unexpected_words"]:
                with self.subTest(unexpected_word=unexpected_word):
                    self.assertNotIn(unexpected_word, solutions)
