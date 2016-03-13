from unittest import TestCase

from twitterpibot.responses import x_or_y_response

__author__ = 'andrewtatham'


class TestX_Or_Y_Response(TestCase):
    def x_or_y_test(self):
        self._test("x or y?", "x", "y")
        self._test("x or y ?", "x", "y")
        self._test("x vs y?", "x", "y")
        self._test("x x x or y y y?", "x x x", "y y y")
        self._test("rather x x x or y y y?", "x x x", "y y y")
        self._test("? x x x or y y y?", "x x x", "y y y")
        self._test(": x x x or y y y?", "x x x", "y y y")
        self._test(", x x x or y y y?", "x x x", "y y y")

        self._test("team x or team y?", "team x", "team y")
        self._test("option x or option y?", "option x", "option y")

        self._test("Lionel Messi vs Luis Suarez. Which goal do you like the most? #MessiFCB or #SuarezFCB",
                   "Lionel Messi",
                   "Luis Suarez")

        self._test(
            "Cameron Diaz’s Shockingly Youthful Look On ‘Women’s Health’: Photoshop Or Plastic Surgery? http://bit.ly/1Umkj77",
            "Photoshop",
            "Plastic Surgery")
        self._test(
                "Would you rather rest a diaphragm or decontaminate a grade?",
                "rest a diaphragm",
                "decontaminate a grade")



        # x too long
        self._test(
            "@BattlefieldCTE @tiggr_ @_jjju_ Am i missing some thing here not seeing the full picture are they leaving dice moving on or some thing?")

    def _test(self, text, expected_x=None, expected_y=None):
        pairs = x_or_y_response._parse(text)
        with(self.subTest(text)):
            if expected_x or expected_y:

                for pair in pairs:
                    actual_x = pair[0]
                    actual_y = pair[1]

                    self.assertEqual(actual_x, expected_x)
                    self.assertEqual(actual_y, expected_y)
            else:
                self.assertListEqual([], pairs)
