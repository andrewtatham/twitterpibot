import datetime
from unittest import TestCase

from twitterpibot.logic import astronomy


class TestAstronomy(TestCase):
    def test_get_daytimeness_factor(self):
        self.assertEquals(astronomy.get_daytimeness_factor(datetime.datetime.today()), 0)
