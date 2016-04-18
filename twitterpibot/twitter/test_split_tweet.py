import random
from unittest import TestCase
from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.twitter.tweet_splitter import split_tweet

__author__ = 'andrewtatham'


class TestSplitTweet(TestCase):
    def test_split_tweet(self):
        config = {
            "characters_reserved_per_media": 24,
            "short_url_length": 23,
            "short_url_length_https": 23,
        }

        tweet = OutgoingTweet(
            text="@mention" + " blah" * random.randint(0, 200) + " http://www.text.com",
            urls=["http://www.url.com"],
            quote=IncomingTweet(
                {
                    "id_str": "1234",
                    "sender_screen_name": "sender_screen_name"
                },
                None),
            file_paths=[
                "img0.gif",
                "img1.gif",
                "img2.gif"
            ]
        )
        tweet.media_ids = [str(i) for i in range(random.randint(0, 8))]

        split_tweets = split_tweet(tweet, config)

        for i in range(len(split_tweets)):
            with self.subTest(i):
                x = split_tweets[i]
                print(x.status, x.media_ids)
                x.display()
