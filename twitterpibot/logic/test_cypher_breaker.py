from unittest import TestCase
from twitterpibot.logic.cypher_breaker import is_cypher

__author__ = 'andrewtatham'


class TestIsCypher(TestCase):
    def test_is_cypher(self):

        self.assertTrue(is_cypher("A IHZ DHTDO KRCF TDAZL"))

        self.assertFalse(is_cypher("I CANT STAND IT ANY LONGER"))
