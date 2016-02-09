from unittest import TestCase

from twitterpibot.logic import FileSystemHelper


class TestGet_url_extension(TestCase):
    def test_get_url_extension(self):
        self.assertEqual(".gif", FileSystemHelper.get_url_extension("http://blah.com/blah/blah.gif"))
