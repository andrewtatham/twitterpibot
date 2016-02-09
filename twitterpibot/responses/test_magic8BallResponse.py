from unittest import TestCase

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.responses.Magic8BallResponse import Magic8BallResponse

__author__ = 'Andrew'


class TestMagic8BallResponse(TestCase):
    def test_condition(self):
        response = Magic8BallResponse()

        # Always respond to streamed tweets
        self.assertTrue(response.condition(IncomingTweet({
            "tweet_source": "stream:#Magic8Ball",
            "text": "blah?"
        })))

        self.assertFalse(response.condition(IncomingTweet({
            "text": "blah?"
        })))
