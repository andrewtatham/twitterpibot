import logging
from unittest import TestCase

from twitterpibot.logic import eggpuns

logging.basicConfig(level=logging.DEBUG)
__author__ = 'andrewtatham'

trigger_testcases = [
    "eg",
    "ag"
]
not_trigger_testcases = [
    "egg",
    "eggs"
]

pun_testcases = [

    ("exactly", "EGGSactly"),
    ("explosion", "EGGSplosion"),

    ("shelf", "SHELLf"),
    ("hello", "SHELLo"),
    ("there was an explosion", "there was an EGGSplosion"),
    ("very selfish", "very SHELLfish"),
    ("hello what shall i ", "SHELLo what SHELL i "),
    ("dalek", "dalEGG"),
    ("six of these", "six OEUF these"),
    ("Egypt", "EGGypt"),
    ("aggregate", "EGGrEGGate"),
    ("enough", "enoEGGh"),
    ("ignite", "EGGnite"),
    ("it was a funny joke", "it was a funny YOLK"),
    ("they were joking around", "they were YOLKing around"),
    ("listening to folk music", "listening to YOLK music"),
    ("self-aware", "SHELLf-aware"),
    ("egregious", "EGGrEGGious"),
    ("I'm a little teapot", "OMLETTEtle teapot"),
    ("I'm literally", "OMLETTEerally"),
    ("I'm a literary", "OMLETTEerary"),
    ("corrected", "corrEGGted"),
    ("over and out", "OVUM and out"),
    ("eccentric", "EGGcentric"),
    ("I'm selling a", "I'm SHELLing a"),

]

pun_with_mask_testcases = [
    (
        "@imagebot explosion http://blagh.com #joke",
        "          explosion                  #joke",
        "@imagebot EGGSplosion http://blagh.com #YOLK"

    )
]

is_egg_pun_testcases = [
    "eggsplosion",
    "egg-splosion",
]

is_not_egg_pun_testcases = [
    "egg",
    "eggs",
    "eggbox",
    "eggshell",
]

class TestsEggPuns(TestCase):
    def test_is_egg_pun_trigger(self):
        for testcase in trigger_testcases:
            with self.subTest(testcase):
                self.assertTrue(eggpuns.is_egg_pun_trigger(testcase))

    def test_is_not_egg_pun_trigger(self):
        for testcase in not_trigger_testcases:
            with self.subTest(testcase):
                self.assertFalse(eggpuns.is_egg_pun_trigger(testcase))

    def test_make_egg_pun(self):
        for testcase in pun_testcases:
            with self.subTest(testcase):
                self.assertEqual(testcase[1], eggpuns.make_egg_pun(testcase[0]))
        for testcase in is_not_egg_pun_testcases:
            with self.subTest(testcase):
                self.assertIsNone(eggpuns.make_egg_pun(testcase))

    def test_make_egg_pun_with_mask(self):
        for testcase in pun_with_mask_testcases:
            with self.subTest(testcase):
                self.assertEqual(testcase[2], eggpuns.make_egg_pun(testcase[0], testcase[1]))

    def test_is_egg_pun(self):
        for testcase in is_egg_pun_testcases:
            with self.subTest(testcase):
                self.assertTrue(eggpuns.is_egg_pun(testcase))

    def test_is_not_egg_pun(self):
        for testcase in is_not_egg_pun_testcases:
            with self.subTest(testcase):
                self.assertFalse(eggpuns.is_egg_pun(testcase))