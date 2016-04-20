from unittest import TestCase
from twitterpibot.logic.cypher_helper import SimpleCypher, CeaserCypher
from twitterpibot.logic.leetspeak import LeetSpeak
from twitterpibot.logic.morse_code import MorseCode


class TestSimpleCypher(TestCase):
    cypher = SimpleCypher()

    def test_encode(self):
        self.assertEqual("SVOOL DLIOW 8765", self.cypher.encode("HELLO WORLD 1234"))

    def test_decode(self):
        self.assertEqual("HELLO WORLD 1234", self.cypher.decode("SVOOL DLIOW 8765"))


class TestMorseCode(TestCase):
    cypher = MorseCode()

    def test_encode(self):
        self.assertEqual(".... . .-.. .-.. ---  .-- --- .-. .-.. -..  .---- ..--- ...-- ....-",
                         self.cypher.encode("HELLO WORLD 1234"))

    def test_decode(self):
        self.assertEqual("HELLO WORLD 1234",
                         self.cypher.decode(".... . .-.. .-.. ---  .-- --- .-. .-.. -..  .---- ..--- ...-- ....-"))


class TestCeaserCypherPositive(TestCase):
    cypher = CeaserCypher(1)

    def test_encode(self):
        self.assertEqual("IFMMP XPSME 2345", self.cypher.encode("HELLO WORLD 1234"))

    def test_decode(self):
        self.assertEqual("HELLO WORLD 1234", self.cypher.decode("IFMMP XPSME 2345"))


class TestCeaserCypherNegative(TestCase):
    cypher = CeaserCypher(-1)

    def test_encode(self):
        self.assertEqual("GDKKN VNQKC 0123", self.cypher.encode("HELLO WORLD 1234"))

    def test_decode(self):
        self.assertEqual("HELLO WORLD 1234", self.cypher.decode("GDKKN VNQKC 0123"))


class TestLeetSpeak(TestCase):
    cypher = LeetSpeak()

    def test_encode(self):
        self.assertEqual("4LL Y0UR 8453 4R3 83L0NG 70 U5", self.cypher.encode("ALL YOUR BASE ARE BELONG TO US"))

    def test_decode(self):
        self.assertEqual("ALL YOUR BASE ARE BELONG TO US", self.cypher.decode("4LL Y0UR 8453 4R3 83L0NG 70 U5"))
