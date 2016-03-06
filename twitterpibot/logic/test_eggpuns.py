from unittest import TestCase

from twitterpibot.logic import eggpuns

__author__ = 'andrewtatham'

trigger_testcases = ["egg"]

pun_testcases = [

    ("exactly", "eggsactly"),
    ("explosion", "eggsplosion"),

    ("shelf", "shellf"),
    ("hello", "shello")
]


class TestsEggPuns(TestCase):
    def test_is_egg_pun_trigger(self):
        for testcase in trigger_testcases:
            self.assertTrue(eggpuns.is_egg_pun_trigger(testcase))

    def test_make_egg_pun(self):
        for testcase in pun_testcases:
            self.assertEqual(testcase[1], eggpuns.make_egg_pun(testcase[0]))

    def test_make_egg_pun_phrase(self):
        phrase = eggpuns.make_egg_pun_phrase()
        print(phrase)
        self.assertTrue(phrase)
