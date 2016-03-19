from unittest import TestCase

from twitterpibot.responses import x_or_y_response

__author__ = 'andrewtatham'


class TestX_Or_Y_Response(TestCase):
    def x_or_y_test(self):
        self._test("x or y?", "x", "y")
        self._test("x or y ?", "x", "y")
        self._test("x vs y?", "x", "y")
        self._test("x x x or y y y?", "x x x", "y y y")
        self._test("rather x x x or y y y?", "x x x", "y y y", pre="rather")
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
            "Plastic Surgery",
            pre="Cameron Diaz’s Shockingly Youthful Look On ‘Women’s Health’:",
            post="? http://bit.ly/1Umkj77")
        self._test(
            "Would you rather rest a diaphragm or decontaminate a grade?",
            "rest a diaphragm",
            "decontaminate a grade",
            pre="Would you rather")
        self._test(
            "RT @BBCSport: #WouldYouRather #LCFC win the PL or #MCFC win the Champions League? Here's Mancini's answer",
            "#LCFC win the PL",
            "#MCFC win the Champions League",
            pre="RT @BBCSport: #WouldYouRather")


        # x too long
        self._test(
            "@BattlefieldCTE @tiggr_ @_jjju_ Am i missing some thing here not seeing the full picture are they leaving dice moving on or some thing?")

    def _test(self, text, expected_x=None, expected_y=None, pre=None, post=None):
        results = x_or_y_response._parse(text)
        with(self.subTest(text)):
            if expected_x or expected_y:
                self.assertTrue(results)
                for result in results:
                    self.assertTrue(result)
                    actual_x = result["x"]
                    actual_y = result["y"]
                    actual_pre = result["pre"]
                    actual_post = result["post"]

                    self.assertEqual(actual_x, expected_x)
                    self.assertEqual(actual_y, expected_y)

                if pre:
                    self.assertEqual(actual_pre, pre)
                if post:
                    self.assertEqual(actual_post, post)

            else:
                self.assertFalse(results)
