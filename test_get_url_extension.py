from unittest import TestCase

from twitterpibot.logic import fsh


class Testfilesystemhelper(TestCase):
    def test_get_url_extension(self):
        self.assertEqual(".gif", fsh.get_url_extension("http://blah.com/blah/blah.gif"))

    def test_root(self):
        self.assertEqual("../../", fsh.root)
