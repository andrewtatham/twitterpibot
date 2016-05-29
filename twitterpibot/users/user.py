import datetime
import os
import random
import re

import dateutil.parser
import humanize

from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.topics import topichelper

import logging

logger = logging.getLogger(__name__)


def parse_int(param):
    if param:
        return int(param)
    else:
        return 0


bot_rx = re.compile("bot|ebooks|#botALLY", re.IGNORECASE)


class UserScore(object):
    def __init__(self, user):
        self._scores = {"total": 0}

        if user.is_arsehole:
            self.add(-200, "arsehole")

        if user.is_friend:
            self.add(100, "friend")
        if user.is_awesome_bot:
            self.add(75, "awesome bot")
        if user.verified:
            self.add(5, "verified")

        if user.follower:
            self.add(5, "follower")
        if user.following:
            self.add(5, "following")
        if user.is_retweet_more:
            self.add(25, "retweet more")
        if user.protected:
            self.add(5, "protected")

        if user.is_reply_less:
            self.add(-10, "reply less")
        if user.is_do_not_retweet:
            self.add(-10, "do not retweet")

        if user.is_possibly_bot:
            self.add(5, "possibly bot")

        if user.lang == "en-gb":
            self.add(5, "the queens english")
        elif user.lang == "en-US":
            self.add(-5, "bloody yanks")
        elif user.lang != "en":
            self.add(-10, "bloody foreigners")

        if user.last_tweeted_at:
            delta = user.get_last_tweet_delta()
            if delta.days >= 60:
                last_tweeted_score = -int(delta.days * 50 / 365)
                self.add(last_tweeted_score, "last tweeted " + user.get_last_tweeted())

        user_topics = self.get_user_topics(user)
        if user_topics:
            topics_score = self.get_score(user_topics)
            self.extend(topics_score)

        tweets = user.get_latest_tweets()
        if tweets:
            tweet_topics = self._get_tweet_topics(tweets)
            if tweet_topics:
                tweet_score = self.get_score(tweet_topics)
                self.extend(tweet_score)

    def __str__(self):
        return str(self._scores)

    def add(self, score, name=None):
        if name:
            if name not in self._scores:
                self._scores[name] = 0
            self._scores[name] += score

        self._scores["total"] += score

    def total(self):
        return self._scores["total"]

    def _get_tweet_topics(self, tweets):
        if tweets:
            topic_text = os.linesep.join(map(lambda t: " " + t.text, tweets))
            if topic_text:
                topics = topichelper.get_topics(topic_text)
                return topics

    def get_user_topics(self, user):
        topic_text = ""
        if user.name:
            topic_text += user.name
        if user.screen_name:
            topic_text += " " + user.screen_name
        if user.description:
            topic_text += " " + user.description

        topics = topichelper.get_topics(topic_text)
        return topics

    def extend(self, topics_score):
        if topics_score:
            for k, v in topics_score.items():
                self.add(v, k)

    def get_score(self, topics):
        user_score = {}
        if topics:
            for topic in topics.list():
                if "definite_matches" in topic:
                    definite_score = 5 * topic["score"] * len(topic["definite_matches"])
                    definite_description = "topic: " + topic["topic"] \
                                           + ", definite_matches: " + str(topic["definite_matches"])
                    user_score[definite_description] = definite_score
                if "possible_matches" in topic:
                    possible_score = topic["score"] * len(topic["possible_matches"])
                    possible_description = "topic: " + topic["topic"] \
                                           + " possible_matches: " + str(topic["possible_matches"])
                    user_score[possible_description] = possible_score
            return user_score


class User(object):
    def __init__(self, data, identity):

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
        if self.created_at:
            self.created_at = dateutil.parser.parse(self.created_at)

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
        self.user_score = None

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

    def short_description(self):
        desc = "{} [@{}".format(
            self.name,
            self.screen_name,
        )
        if self.flags:
            desc += ", flags:{}".format(self.flags)
        if self.user_score:
            desc += ", score:{}".format(self.user_score.total())
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
        return self._latest_tweets

    def get_user_score(self):
        if not self.user_score:
            logger.debug("scoring user: {}".format(self.short_description()))
            # todo update
            user_score = UserScore(self)
            self.user_score = user_score
            logger.info("scored user: {}".format(self.short_description()))

        return self.user_score

    def is_inactive(self):
        delta = self.get_last_tweet_delta()
        return delta and delta > datetime.timedelta(365)


if __name__ == '__main__':
    import identities

    identity = identities.AndrewTathamPiIdentity(None)
    user_ids = list(identity.users.get_followers())
    random.sample(user_ids, 2)

    i = 0
    for user_id in user_ids:
        user = identity.users.get_user(user_id)
        print("-" * 80)
        user.get_user_score()
        print("user: " + user.long_description())
        # print("tweets: " + os.linesep.join(map(lambda t: t.description(), user.get_latest_tweets())))
        # print("follower score: " + str(user.get_follower_score()))
        # print("following score: " + str(user.get_following_score()))
