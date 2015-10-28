from unittest import TestCase
import twitterpibot.songs.Songs as Songs
from twitterpibot.processing.christmas import is_christmas


class TestSongs(TestCase):
    def test_AllKeys(self):
        k = Songs.Songs().AllKeys()
        self.assertTrue("hammertime" in k)
        self.assertTrue("jinglebells" in k)
        self.assertTrue("indaclub" in k)

    def test_Keys(self):

        k = Songs.Songs().Keys()

        self.assertTrue("hammertime" in k)

        ischristmas = is_christmas()

        if ischristmas:
            self.assertTrue("jinglebells" in k)
        else:
            self.assertFalse("jinglebells" in k)

        self.assertFalse("indaclub" in k)