from unittest import TestCase

from twitterpibot.logic.admin_commands import SetTokenResponse


class TestSetTokenResponse(TestCase):
    def test_parse(self):
        key, value = SetTokenResponse.parse("set token blah1 blah2 = blah3 blah4")
        self.assertEqual(key, "blah1 blah2")
        self.assertEqual(value, "blah3 blah4")
