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
        urls = ["http://www.url{}.com".format(i) for i in range(random.randint(0, 3))]
        quote_tweet = IncomingTweet(
            {
                "id_str": "1234",
                "sender_screen_name": "sender_screen_name"
            },
            None)
        lines = [
            "@mention{} {} http://www.text{}.com".format(i, " ".join(["blah" for _ in range(random.randint(0, 20))]), i)
            for i in range(random.randint(0, 4))
            ]
        text = " ".join(lines)
        tweet = OutgoingTweet(
            text=text,
            urls=urls,
            quote=quote_tweet,
        )
        # upload
        tweet.media_ids = [str(i) for i in range(random.randint(0, 8))]

        split_tweets = split_tweet(tweet, config)

        for i in range(len(split_tweets)):
            with self.subTest(i):
                x = split_tweets[i]
                print(x.status, x.media_ids)
                x.display()
