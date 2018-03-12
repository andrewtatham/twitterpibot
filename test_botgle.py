import logging
import pprint
from unittest import TestCase
from twitterpibot.logic.botgle import played_rx

from twitterpibot.logic.botgle_solver import parse_board, solve_board

__author__ = 'andrewtatham'
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

_boardtweets = [
    'Warning! Just 3 minutes left\n'
    '\u3000Ｈ\u3000\u3000Ｐ\u3000\u3000Ｅ\u3000\u3000Ｏ\u3000\n'
    '\u3000Ｉ\u3000\u3000Ｏ\u3000\u3000Ｇ\u3000\u3000Ｌ\u3000\n'
    '\u3000Ｌ\u3000\u3000Ｔ\u3000\u3000Ａ\u3000\u3000Ｗ\u3000\n'
    '\u3000Ｉ\u3000\u3000Ｒ\u3000\u3000Ｓ\u3000\u3000Ｅ\u3000\n'
    '\n'
    '🎶',
    'You see a Boggle board in the distance:\n'
    '\n'
    '\u3000Ｆ\u3000\u3000Ｅ\u3000\u3000Ｂ\u3000\u3000Ｉ\u3000\n'
    '\u3000Ｄ\u3000\u3000Ｙ\u3000\u3000Ｎ\u3000\u3000Ｅ\u3000\n'
    '\u3000Ｖ\u3000\u3000Ｔ\u3000\u3000Ｔ\u3000\u3000Ｔ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｕ\u3000\u3000Ｙ\u3000\u3000Ｓ\u3000\n'
    '\n'
    '🎀 🌈 😸',
    'The timer is started! 8 minutes to play!\n'
    '\u3000Ｆ\u3000\u3000Ｅ\u3000\u3000Ｂ\u3000\u3000Ｉ\u3000\n'
    '\u3000Ｄ\u3000\u3000Ｙ\u3000\u3000Ｎ\u3000\u3000Ｅ\u3000\n'
    '\u3000Ｖ\u3000\u3000Ｔ\u3000\u3000Ｔ\u3000\u3000Ｔ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｕ\u3000\u3000Ｙ\u3000\u3000Ｓ\u3000\n'
    '\n'
    '🎇',
    'Warning! Just 3 minutes left\n'
    '\u3000Ｆ\u3000\u3000Ｅ\u3000\u3000Ｂ\u3000\u3000Ｉ\u3000\n'
    '\u3000Ｄ\u3000\u3000Ｙ\u3000\u3000Ｎ\u3000\u3000Ｅ\u3000\n'
    '\u3000Ｖ\u3000\u3000Ｔ\u3000\u3000Ｔ\u3000\u3000Ｔ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｕ\u3000\u3000Ｙ\u3000\u3000Ｓ\u3000\n'
    '\n'
    '🎊',
    'Above you a skywriter dances the path of a Boggle board\n'
    '\n'
    '\u3000Ｅ\u3000\u3000Ｖ\u3000\u3000Ｈ\u3000\u3000Ｆ\u3000\n'
    '\u3000Ｅ\u3000\u3000Ｏ\u3000\u3000Ｗ\u3000\u3000Ｌ\u3000\n'
    '\u3000Ｈ\u3000\u3000Ｌ\u3000\u3000Ｓ\u3000\u3000Ｄ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｌ\u3000\u3000Ｉ\u3000\u3000Ｏ\u3000\n'
    '\n'
    '🐌 🌈 🐲',
    'The timer is started! 8 minutes to play!\n'
    '\u3000Ｅ\u3000\u3000Ｖ\u3000\u3000Ｈ\u3000\u3000Ｆ\u3000\n'
    '\u3000Ｅ\u3000\u3000Ｏ\u3000\u3000Ｗ\u3000\u3000Ｌ\u3000\n'
    '\u3000Ｈ\u3000\u3000Ｌ\u3000\u3000Ｓ\u3000\u3000Ｄ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｌ\u3000\u3000Ｉ\u3000\u3000Ｏ\u3000\n'
    '\n'
    '🎯',
    'Warning! Just 3 minutes left\n'
    '\u3000Ｅ\u3000\u3000Ｖ\u3000\u3000Ｈ\u3000\u3000Ｆ\u3000\n'
    '\u3000Ｅ\u3000\u3000Ｏ\u3000\u3000Ｗ\u3000\u3000Ｌ\u3000\n'
    '\u3000Ｈ\u3000\u3000Ｌ\u3000\u3000Ｓ\u3000\u3000Ｄ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｌ\u3000\u3000Ｉ\u3000\u3000Ｏ\u3000\n'
    '\n'
    '👾',
    "I love you. Let's play:\n"
    '\n'
    '\u3000Ｂ\u3000\u3000Ｓ\u3000\u3000Ｅ\u3000\u3000Ｏ\u3000\n'
    '\u3000Ｒ\u3000\u3000Ｏ\u3000\u3000Ｓ\u3000\u3000Ｗ\u3000\n'
    '\u3000Ｉ\u3000\u3000Ｓ\u3000\u3000Ａ\u3000\u3000Ｅ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｚ\u3000\u3000Ｌ\u3000\u3000Ｑｕ\n'
    '\n'
    '🎯 💯 🎊',
    'The timer is started! 8 minutes to play!\n'
    '\u3000Ｂ\u3000\u3000Ｓ\u3000\u3000Ｅ\u3000\u3000Ｏ\u3000\n'
    '\u3000Ｒ\u3000\u3000Ｏ\u3000\u3000Ｓ\u3000\u3000Ｗ\u3000\n'
    '\u3000Ｉ\u3000\u3000Ｓ\u3000\u3000Ａ\u3000\u3000Ｅ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｚ\u3000\u3000Ｌ\u3000\u3000Ｑｕ\n'
    '\n'
    '🎊',
    'Warning! Just 3 minutes left\n'
    '\u3000Ｂ\u3000\u3000Ｓ\u3000\u3000Ｅ\u3000\u3000Ｏ\u3000\n'
    '\u3000Ｒ\u3000\u3000Ｏ\u3000\u3000Ｓ\u3000\u3000Ｗ\u3000\n'
    '\u3000Ｉ\u3000\u3000Ｓ\u3000\u3000Ａ\u3000\u3000Ｅ\u3000\n'
    '\u3000Ｏ\u3000\u3000Ｚ\u3000\u3000Ｌ\u3000\u3000Ｑｕ\n'
    '\n'
    '🐉',
    "I love you. Let's play:\n"
    '\n'
    '\u3000Ｚ\u3000\u3000Ｓ\u3000\u3000Ｎ\u3000\u3000Ｂ\u3000\n'
    '\u3000Ｅ\u3000\u3000Ｑｕ\u3000Ｏ\u3000\u3000Ｒ\u3000\n'
    '\u3000Ｆ\u3000\u3000Ｘ\u3000\u3000Ｔ\u3000\u3000Ｙ\u3000\n'
    '\u3000Ｈ\u3000\u3000Ｅ\u3000\u3000Ｔ\u3000\u3000Ｏ\u3000\n'
    '\n'
    '💎 👾 🚀',
    'The timer is started! 8 minutes to play!\n'
    '\u3000Ｚ\u3000\u3000Ｓ\u3000\u3000Ｎ\u3000\u3000Ｂ\u3000\n'
    '\u3000Ｅ\u3000\u3000Ｑｕ\u3000Ｏ\u3000\u3000Ｒ\u3000\n'
    '\u3000Ｆ\u3000\u3000Ｘ\u3000\u3000Ｔ\u3000\u3000Ｙ\u3000\n'
    '\u3000Ｈ\u3000\u3000Ｅ\u3000\u3000Ｔ\u3000\u3000Ｏ\u3000\n'
    '\n'
    '☀',
    'Warning! Just 3 minutes left\n'
    '\u3000Ｚ\u3000\u3000Ｓ\u3000\u3000Ｎ\u3000\u3000Ｂ\u3000\n'
    '\u3000Ｅ\u3000\u3000Ｑｕ\u3000Ｏ\u3000\u3000Ｒ\u3000\n'
    '\u3000Ｆ\u3000\u3000Ｘ\u3000\u3000Ｔ\u3000\u3000Ｙ\u3000\n'
    '\u3000Ｈ\u3000\u3000Ｅ\u3000\u3000Ｔ\u3000\u3000Ｏ\u3000\n'
    '\n'
    '♨',
]

game_over_tweets = [
    'GAME OVER! SCORES:\n'
    '@keybeingkey: 56 🌟\n'
    '@ahsoftware: 39 🌟\n'
    '@borisonr: 37 🎇\n'
    '@dubey44: 13 🏆\n'
    '@tedeverson: 2 🎆',
    'GAME OVER! SCORES:\n'
    '@isemann: 21 🐲\n'
    '@borisonr: 17 🎶\n'
    '@snailwash: 8 🎶\n'
    '@Braisco: 7 🔥\n'
    '@guyphipps: 1 🐲',
    'Next game in 6 hours! 💎',
    'GAME OVER! SCORES:\n'
    '@ahsoftware: 52 🎀\n'
    '@joe_newlin: 25 🌈\n'
    '@dubey44: 10 🎀\n'
    '@muffinista: 3 🏁\n'
    '@Braisco: 1 💥',
    'GAME OVER! SCORES:\n@beedudebg: 23 🎯\n@joe_newlin: 17 💥',
    'GAME OVER! SCORES:\n'
    '@keybeingkey: 46 🎇\n'
    '@borisonr: 18 🌈\n'
    '@dubey44: 9 🎀\n'
    '@coleseadubs: 1 🎊\n'
    '@phil94SR: 1 🏆',
    'Next game in 6 hours! 🎊'

]
next_game_tweets = [
    'Next game in 6 hours! ♨',
    'Hey there! Boggle in 10 minutes! 🎶',
    'Next game in 6 hours! 🏁',
    'Hey there! Boggle in 10 minutes! 💯',
    'Next game in 6 hours! 🐲',
    'Hey there! Boggle in 10 minutes! 👾',
    'Hey there! Boggle in 10 minutes! 🌟',

]

played_word_tweets = [
    "@lmaomaxi plays UDOS LUDS ADOS ILKA GULA SIDA LUGS LUDO AXIL KADI 🚀",
    "@ahsoftware plays SODA 🚀",
    "@joe_newlin plays ALL LUX 🐉",
    "@ahsoftware plays ADIOS 👾",
    "@joe_newlin plays TUX 🎊",
    "@joe_newlin plays DOS ADS ☀",
    "@joe_newlin plays TUGS TUG BUDO 🎊",
    "@ahsoftware plays ALB DUB 🐉",
    "@ahsoftware plays SOD 💥",
    "@joe_newlin plays SULK 💎",
    "@joe_newlin plays DIS IDS 💯"
]


class Test_Parse_Board(TestCase):
    def test_parse_board_from_tweets(self):
        for tweet in _boardtweets:
            with self.subTest(tweet=tweet):
                board = parse_board(tweet)
                print(board)
                self.assertTrue(board)
                self.assertEquals(4, len(board), "rows")
                for row in board:
                    self.assertEquals(4, len(row), "cols")

    def test_parse_board(self):
        testcases = [
            {
                "tweet": """
                    　Ｘ　　Ｅ　　Ｉ　　Ｕ　
                    　Ｑｕ　Ｔ　　Ｄ　　Ｊ　
                    　Ｓ　　Ｎ　　Ｏ　　Ｅ　
                    　Ｏ　　Ｆ　　Ｒ　　Ｄ　
                    """,
                "board": [
                    ['X', 'E', 'I', 'U'],
                    ['QU', 'T', 'D', 'J'],
                    ['S', 'N', 'O', 'E'],
                    ['O', 'F', 'R', 'D']
                ]
            },
            {
                "tweet": """
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
            },
            {
                "tweet": """
                    　Ｚ　　Ｓ　　Ｎ　　Ｂ　
                    　Ｅ　　Ｑｕ　Ｏ　　Ｒ　
                    　Ｆ　　Ｘ　　Ｔ　　Ｙ　
                    　Ｈ　　Ｅ　　Ｔ　　Ｏ　""",
                "board": [
                    ['Z', 'S', 'N', 'B'],
                    ['E', 'QU', 'O', 'R'],
                    ['F', 'X', 'T', 'Y'],
                    ['H', 'E', 'T', 'O']
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
        words.sort(key=len)
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


class TestPlayedWords(TestCase):
    def test_played_words_rx(self):
        for tweet in played_word_tweets:
            with self.subTest(tweet=tweet):
                match = played_rx.search(tweet)
                ret = {
                    "screen_name": str(match.groupdict()["screen_name"]),
                    "words": list([word for word in match.groupdict()["words"].split(" ") if word])
                }
                print(ret)
                self.assertTrue(match)
                self.assertTrue(ret["screen_name"])
                self.assertTrue(ret["words"])
