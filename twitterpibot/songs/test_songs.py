from unittest import TestCase

import twitterpibot.songs.songhelper as Songs
from twitterpibot.logic.xmas import is_christmas


class TestSongs(TestCase):
    def test_AllKeys(self):
        k = Songs.songhelper().all_keys()
        self.assertTrue("hammertime" in k)
        self.assertTrue("jinglebells" in k)
        self.assertTrue("indaclub" in k)

    def test_Keys(self):

        k = Songs.songhelper().keys()

        self.assertTrue("hammertime" in k)

        ischristmas = is_christmas()

        if ischristmas:
            self.assertTrue("jinglebells" in k)
        else:
            self.assertFalse("jinglebells" in k)

        self.assertFalse("indaclub" in k)
