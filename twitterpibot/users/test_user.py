from unittest import TestCase

import datetime

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.users.user import User, get_recent_tweet_rate


class TestUser(TestCase):
    def test_id_str(self):
        self.assertEqual("123", User({"id_str": "123"}).id_str)

    def test_name(self):
        self.assertEqual("name", User({"name": "name"}).name)

    def test_screen_name(self):
        self.assertEqual("screen_name", User({"screen_name": "screen_name"}).screen_name)

    def test_created_at(self):
        created_at = datetime.datetime.now(datetime.timezone.utc)
        created_at_str = str(created_at)
        self.assertEqual(created_at, User({"created_at": created_at_str}).created_at)

    def test_account_age(self):
        account_age = datetime.timedelta(days=365 * 3)
        created_at = datetime.datetime.now(datetime.timezone.utc) - account_age
        created_at_str = str(created_at)
        user = User({"created_at": created_at_str})
        self.assertEqual(created_at, user.created_at)
        self.assertEqual(account_age.days, user.account_age.days)

    def test_tweet_rate_lifetime(self):
        statuses_count = 365 * 3
        account_age = datetime.timedelta(days=365 * 3)
        created_at = datetime.datetime.now(datetime.timezone.utc) - account_age
        created_at_str = str(created_at)

        user = User({
            "created_at": created_at_str,
            "statuses_count": statuses_count,
        })

        self.assertEqual(created_at, user.created_at)
        self.assertEqual(account_age.days, user.account_age.days)
        self.assertEqual(statuses_count / account_age.days, user.tweet_rate_lifetime)

    def test_tweet_rate_recent(self):
        statuses_count = 100
        tweet_date_range = datetime.timedelta(days=50)

        latest_tweet_at = datetime.datetime.now(datetime.timezone.utc)
        earliest_tweet_at = latest_tweet_at - tweet_date_range
        delta = tweet_date_range / statuses_count

        user = User()

        recent_tweets = []
        for i in range(statuses_count + 1):
            created_at = earliest_tweet_at + i * delta
            tweet = IncomingTweet({"created_at": str(created_at)})
            recent_tweets.append(tweet)
        self.assertEquals(latest_tweet_at, created_at)

        user.tweet_rate_recent = get_recent_tweet_rate(recent_tweets)

        self.assertAlmostEqual(statuses_count / tweet_date_range.days, user.tweet_rate_recent, delta=0.1)

    def test_is_inactive(self):
        user = {
            "status": {
                "created_at": None
            }
        }
        self.assertFalse(User(user).is_inactive())

        active_user = {
            "status": {
                "created_at": str(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(-364))
            }
        }
        self.assertFalse(User(active_user).is_inactive())

        inactive_user = {
            "status": {
                "created_at": str(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(-366))
            }
        }
        self.assertTrue(User(inactive_user).is_inactive())
