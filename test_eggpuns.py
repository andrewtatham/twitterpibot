from unittest import TestCase

from twitterpibot.logic import eggpuns

__author__ = 'andrewtatham'

trigger_testcases = ["egg"]

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
    ("aggregate", "EGGgrEGGate"),
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
    ("eggbox", "eggbox"),
    ("eggshell", "eggshell")

]

pun_with_mask_testcases = [
    (
        " @imagebot explosion http://blah.com #joke",
        "           explosion                 #joke",
        " @imagebot EGGSplosion http://blah.com #YOLK"

    )
]


class TestsEggPuns(TestCase):
    def test_is_egg_pun_trigger(self):
        for testcase in trigger_testcases:
            with self.subTest(testcase):
                self.assertTrue(eggpuns.is_egg_pun_trigger(testcase))

    def test_make_egg_pun(self):
        for testcase in pun_testcases:
            with self.subTest(testcase):
                self.assertEqual(testcase[1], eggpuns.make_egg_pun(testcase[0]))

    def test_make_egg_pun_with_mask(self):
        for testcase in pun_with_mask_testcases:
            with self.subTest(testcase):
                self.assertEqual(testcase[2], eggpuns.make_egg_pun(testcase[0], testcase[1]))

    # def test_make_egg_pun_phrase(self):
    #     phrase = eggpuns.make_egg_pun_phrase()
    #     print(phrase)
    #     self.assertTrue(phrase)
