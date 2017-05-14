import datetime
import logging
import os
import random
import re

import dateutil.parser
import humanize

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.topics import topichelper
from twitterpibot.users.scores import UserScore

logger = logging.getLogger(__name__)


def parse_int(param):
    if param:
        return int(param)
    else:
        return 0


bot_rx = re.compile("bot|ebooks|#botALLY", re.IGNORECASE)


def get_recent_tweet_rate(tweets):
    if tweets:
        tweet_times = list(map(lambda t: t.created_at,tweets))
        earliest_recent_tweet_at = min(tweet_times)
        latest_recent_tweet_at = max(tweet_times)
        recent_tweets_time_range = (latest_recent_tweet_at - earliest_recent_tweet_at).days
        number_of_recent_tweets = len(tweet_times)
        if recent_tweets_time_range:
             return number_of_recent_tweets / recent_tweets_time_range


class User(object):
    def __init__(self, data={}, identity=None):

        self.id_str = data.get("id_str")
        self.name = data.get("name")
        self.screen_name = data.get("screen_name")
        self.profile_url = "https://twitter.com/" + str(self.screen_name)
        self.description = data.get("description")
        self.url = data.get("url")
        self.profile_image_url = data.get("profile_image_url")
        self.profile_banner_url = data.get("profile_banner_url")
        if self.profile_banner_url:
            self.profile_banner_url += "/300x100"

        self.created_at = data.get("created_at")
        self.account_age = None
        if self.created_at:
            self.created_at = dateutil.parser.parse(self.created_at)
            self.account_age = datetime.datetime.now(datetime.timezone.utc) - self.created_at

        self.entities = data.get("entities")  # TODO get mentions/display urls
        self.lang = data.get("lang")
        self.time_zone = data.get("time_zone")
        self.utc_offset = data.get("utc_offset")

        self.identity = identity
        self.is_me = identity and bool(self.screen_name == identity.screen_name)

        self.following = bool(data.get("following"))
        self.follower = bool(data.get("following"))
        self.verified = bool(data.get("verified"))
        self.location = data.get("location")
        self.protected = bool(data.get("protected"))
        self.follow_request_sent = bool(data.get("follow_request_sent"))

        self.friends_count = parse_int(data.get("friends_count"))
        self.followers_count = parse_int(data.get("followers_count"))
        self.statuses_count = parse_int(data.get("statuses_count"))
        self.listed_count = parse_int(data.get("listed_count"))

        self.tweet_rate_lifetime = None
        if self.statuses_count and self.account_age and self.account_age.days:
            self.tweet_rate_lifetime = self.statuses_count / self.account_age.days

        self.updated = None

        self.is_arsehole = False
        self.is_do_not_retweet = False
        self.is_retweet_more = False
        self.is_awesome_bot = False
        self.is_friend = False
        self.is_reply_less = False

        self.is_possibly_bot = self.screen_name and bot_rx.search(self.screen_name) \
                               or self.name and bot_rx.search(self.name) \
                               or self.description and bot_rx.search(self.description)

        self.flags = ""

        status = data.get("status")
        self.status = None
        if status:
            self.status = IncomingTweet(status, self.identity, skip_user=True)

        self.last_tweeted_at = None
        if self.status:
            self.last_tweeted_at = self.status.created_at

        self._latest_tweets = []
        self.tweet_rate_recent = None

        self.topics = None
        self.get_user_topics()

        self.user_score = UserScore(self, include_recent_tweets_score=False)

    def get_user_topics(self):
        topic_text = ""
        if self.name:
            topic_text += self.name
        if self.screen_name:
            topic_text += " " + self.screen_name
        if self.description:
            topic_text += " " + self.description

        self.topics = topichelper.get_topics(topic_text)

    def update_flags(self):
        self.flags = ""
        if self.following and self.follower:
            self.flags += " FF"
        elif self.following:
            self.flags += " Fg"
        elif self.follower:
            self.flags += " Fr"

        if self.verified: self.flags += " V"
        if self.protected: self.flags += " P"

        if self.is_arsehole: self.flags += " AH"
        if self.is_friend: self.flags += " FR"
        if self.is_awesome_bot: self.flags += " AB"
        if self.is_possibly_bot: self.flags += " PB"
        if self.is_retweet_more: self.flags += " RT+"
        if self.is_do_not_retweet: self.flags += " RT-"
        if self.is_reply_less: self.flags += " RP-"
        self.flags = self.flags.strip()

    def is_stale(self):
        if self.updated:
            # noinspection PyTypeChecker
            delta = datetime.datetime.utcnow() - self.updated
            mins = divmod(delta.days * 86400 + delta.seconds, 60)[0]
            return mins > 45
        else:
            return True

    def __str__(self):
        return "@{} {}".format(
            self.screen_name,
            self.flags
        )

    def short_display(self):
        desc = "{} @{}".format(
            self.name,
            self.screen_name,
        )
        return desc

    def short_description(self):
        desc = "{} [screen name: @{}".format(
            self.name,
            self.screen_name,
        )
        if self.flags:
            desc += ", user flags: {}".format(self.flags)
        if self.user_score:
            desc += ", user score: {}".format(self.user_score.total())
        desc += "]"
        return desc

    def get_last_tweet_delta(self):
        if self.last_tweeted_at:
            return datetime.datetime.now(datetime.timezone.utc) - self.last_tweeted_at

    def get_last_tweeted(self):
        if self.last_tweeted_at:
            return humanize.naturaldelta(self.get_last_tweet_delta())

    def long_description(self):

        text = self.short_description() + " " + self.profile_url
        if self.description:
            text += os.linesep + "description: " + self.description.replace(os.linesep, " ")
        if self.status:
            text += os.linesep + "status: " + self.status.display()
        if self.lang:
            text += os.linesep + "lang: " + self.lang
        if self.location:
            text += os.linesep + "location: " + self.location
        if self.time_zone:
            text += os.linesep + "time_zone: " + self.time_zone
        if self.utc_offset:
            text += os.linesep + "utc_offset: " + self.location
        if self.last_tweeted_at:
            text += os.linesep + "last tweeted {} ago".format(self.get_last_tweeted())
        if self.user_score:
            text += os.linesep + "user score: " + str(self.user_score)

        return text

    def update_list_memberships(self, list_memberships):
        self.is_arsehole = "Arseholes" in list_memberships
        self.is_reply_less = "Reply Less" in list_memberships
        self.is_do_not_retweet = "Dont Retweet" in list_memberships
        self.is_retweet_more = "Retweet More" in list_memberships
        self.is_awesome_bot = "Awesome Bots" in list_memberships
        self.is_friend = "Friends" in list_memberships

    def get_latest_tweets(self):
        # todo invalidate cache
        if not self._latest_tweets:
            logger.debug("getting tweets")
            tweets = self.identity.twitter.get_user_timeline(user_id=self.id_str)
            logger.debug("tweets = {}".format(tweets))
            if tweets:
                self._latest_tweets = list(map(lambda t: IncomingTweet(t, self.identity, skip_user=True), tweets))

                self.tweet_rate_recent = get_recent_tweet_rate(self._latest_tweets)
        return self._latest_tweets

    def get_user_score(self, include_recent_tweets_score=False):
        if not self.user_score or self.user_score and (
                    not self.user_score.include_recent_tweets_score or self.user_score.is_stale()):
            logger.debug("scoring user: {}".format(self.short_description()))
            self.user_score = UserScore(self, include_recent_tweets_score)
            logger.debug("scored user: {}".format(self.short_description()))

    def is_inactive(self):
        delta = self.get_last_tweet_delta()
        return delta and delta > datetime.timedelta(365)


if __name__ == '__main__':
    import identities_pis

    identity = identities_pis.AndrewTathamPiIdentity(None)
    user_ids = list(identity.users.get_followers())
    random.sample(user_ids, 2)

    i = 0
    for user_id in user_ids:
        user = identity.users.get_user(user_id)
        print("-" * 80)
        print("user: " + user.long_description())
        # print("tweets: " + os.linesep.join(map(lambda t: t.description(), user.get_latest_tweets())))
        # print("follower score: " + str(user.get_follower_score()))
        # print("following score: " + str(user.get_following_score()))
