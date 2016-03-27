import pprint
from unittest import TestCase

from twitterpibot.logic.botgle import parse_board, solve_board

__author__ = 'andrewtatham'


class Test_Parse_Board(TestCase):
    def test_parse_board(self):
        testcase = """blah:
                    　Ｘ　　Ｅ　　Ｉ　　Ｕ　
                    　Ｑｕ　Ｔ　　Ｄ　　Ｊ　
                    　Ｓ　　Ｎ　　Ｏ　　Ｅ　
                    　Ｏ　　Ｆ　　Ｒ　　Ｄ　
                    blah"""
        expected = [
            ['X', 'E', 'I', 'U'],
            ['QU', 'T', 'D', 'J'],
            ['S', 'N', 'O', 'E'],
            ['O', 'F', 'R', 'D']]

        actual = parse_board(testcase)
        self.assertEqual(actual, expected)


class Test_Solve_Board(TestCase):
    def test_solve_board(self):
        board = [
            ['X', 'E', 'I', 'U'],
            ['QU', 'T', 'D', 'J'],
            ['S', 'N', 'O', 'E'],
            ['O', 'F', 'R', 'D']]
        expected_words = [
            "NOD",
        ]
        unexpected_words = [
            "UNFREQUENTEDNESS",  # adjacency
            "TOROTORO"  # duplicate
        ]
        actual = solve_board(board)
        self.assertTrue(actual)
        # print("%s words found..." % len(actual))
        # pprint.pprint(actual)
        for expected_word in expected_words:
            with self.subTest(expected_word=expected_word):
                self.assertIn(expected_word, actual)
        for unexpected_word in unexpected_words:
            with self.subTest(unexpected_word=unexpected_word):
                self.assertNotIn(unexpected_word, actual)
