from unittest import TestCase

import datetime

from twitterpibot.users.user import User


class TestUser(TestCase):
    def test_update_flags(self):
        self.fail()

    def test_is_stale(self):
        self.fail()

    def test_short_description(self):
        self.fail()

    def test_get_last_tweet_delta(self):
        self.fail()

    def test_get_last_tweeted(self):
        self.fail()

    def test_long_description(self):
        self.fail()

    def test_update_list_memberships(self):
        self.fail()

    def test_get_latest_tweets(self):
        self.fail()

    def test_get_user_score(self):
        self.fail()

    def test_is_inactive(self):
        user = {
            "status": {
                "created_at": None
            }
        }
        self.assertFalse(User(user, None).is_inactive())

        active_user = {
            "status": {
                "created_at": str(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(-364))
            }
        }
        self.assertFalse(User(active_user, None).is_inactive())

        inactive_user = {
            "status": {
                "created_at": str(datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(-366))
            }
        }
        self.assertTrue(User(inactive_user, None).is_inactive())
