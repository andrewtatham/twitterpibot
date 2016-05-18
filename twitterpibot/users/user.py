import datetime
import logging
import os
import pprint
import random

import re

import dateutil.parser
import humanize

from twitterpibot import topics
from twitterpibot.incoming.IncomingTweet import IncomingTweet
from twitterpibot.topics import topichelper


def parse_int(param):
    if param:
        return int(param)
    else:
        return 0


bot_rx = re.compile("bot|ebooks|#botALLY", re.IGNORECASE)


class UserScore(object):
    def __init__(self):
        self._scores = {"total": 0}

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


class User(object):
    def __init__(self, data, identity):

        self.id_str = data.get("id_str")
        self.name = data.get("name")
        self.screen_name = data.get("screen_name")
        self.description = data.get("description")
        self.url = data.get("url")
        self.profile_image_url = data.get("profile_image_url")
        self.profile_banner_url = data.get("profile_banner_url")
        if self.profile_banner_url:
            self.profile_banner_url += "/300x100"
        self.identity = identity
        self.is_me = bool(self.screen_name == identity.screen_name)

        self.following = bool(data.get("following"))
        self.follower = bool(data.get("following"))
        self.verified = bool(data.get("verified"))
        self.location = data.get("location")
        self.protected = bool(data.get("protected"))
        self.follow_request_sent = bool(data.get("follow_request_sent"))

        self.friends_count = parse_int(data.get("friends_count"))
        self.followers_count = parse_int(data.get("followers_count"))
        self.statuses_count = parse_int(data.get("statuses_count"))

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

        status = data.get("status")

        self.last_tweeted_at = None
        if status:
            self.last_tweeted_at = dateutil.parser.parse(status.get("created_at"))

        self._latest_tweets = []
        self._user_score = None
        self._follower_score = None
        self._following_score = None

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
        return "{} [@{}] {}".format(
            self.name,
            self.screen_name,
            self.flags,

        )

    def long_description(self):

        text = self.short_description() + " https://twitter.com/" + self.screen_name
        if self.description:
            text += os.linesep + "description: " + self.description.replace(os.linesep, " ")
        if self.location:
            text += os.linesep + "location: " + self.location
        if self.last_tweeted_at:
            delta = datetime.datetime.now(datetime.timezone.utc) - self.last_tweeted_at
            humanized = humanize.naturaldelta(delta)
            text += os.linesep + "last tweeted {} ago".format(humanized)
        if self._user_score:
            text += os.linesep + "user score: " + str(self._user_score)
        if self._follower_score:
            text += os.linesep + "follower score: " + str(self._follower_score)
        if self._following_score:
            text += os.linesep + "following score: " + str(self._following_score)

        return text

    def update_list_memberships(self, list_memberships):
        self.is_arsehole = "Arseholes" in list_memberships
        self.is_reply_less = "Reply Less" in list_memberships
        self.is_do_not_retweet = "Dont Retweet" in list_memberships
        self.is_retweet_more = "Retweet More" in list_memberships
        self.is_awesome_bot = "Awesome Bots" in list_memberships
        self.is_friend = "Friends" in list_memberships

    def _get_latest_tweets(self):
        # todo invalidate cache
        if not self._latest_tweets:
            tweets = self.identity.twitter.get_user_timeline(user_id=self.id_str)
            if tweets:
                self._latest_tweets = list(map(lambda t: IncomingTweet(t, self.identity), tweets))
        return self._latest_tweets

    def _get_topic_text(self):
        topic_text = ""
        if self.name:
            topic_text += self.name
        if self.screen_name:
            topic_text += " " + self.screen_name
        if self.description:
            topic_text += " " + self.description

        topic_text += os.linesep
        tweets = self._get_latest_tweets()
        if tweets:
            tweets_text = map(lambda t: " " + t.text, tweets)
            topic_text += os.linesep.join(tweets_text)
        return topic_text

    def get_user_score(self):
        if not self._user_score:
            user_score = UserScore()

            if self.is_arsehole:
                user_score.add(-200, "arsehole")

            if self.is_friend:
                user_score.add(100, "friend")
            if self.is_awesome_bot:
                user_score.add(75, "awesome bot")
            if self.verified:
                user_score.add(50, "verified")

            if self.follower:
                user_score.add(25, "follower")
            if self.following:
                user_score.add(25, "following")
            if self.is_retweet_more:
                user_score.add(25, "retweet more")

            if self.is_reply_less:
                user_score.add(-10, "reply less")
            if self.is_do_not_retweet:
                user_score.add(-10, "do not retweet")

            if self.is_possibly_bot:
                user_score.add(5, "possibly bot")

            self.get_tweet_score(user_score)

            # todo why does not work?
            self._user_score = user_score

        return self._user_score

    def get_tweet_score(self, user_score):

        topics = topichelper.get_topics(self._get_topic_text())
        if topics:
            for topic in topics.list():
                if "definite_matches" in topic:
                    definite_score = 5 * topic["score"] * len(topic["definite_matches"])
                    definite_description = "topic: " + topic["topic"] \
                                           + ", definite_matches: " + str(topic["definite_matches"])
                    user_score.add(definite_score, definite_description)
                if "possible_matches" in topic:
                    possible_score = topic["score"] * len(topic["possible_matches"])
                    possible_description = "topic: " + topic["topic"] \
                                           + " possible_matches: " + str(topic["possible_matches"])
                    user_score.add(possible_score, possible_description)

    def get_follower_score(self):
        if not self._follower_score:
            follower_score = self.get_user_score()
            # todo are they a spam bot
            # are they always tweeting links
            self._follower_score = follower_score
        return self._follower_score

    def get_following_score(self):
        if not self._following_score:
            following_score = self.get_user_score()
            # todo have they tweeted recently
            self._following_score = following_score
        return self._following_score


if __name__ == '__main__':
    import identities

    identity = identities.AndrewTathamPiIdentity(None)
    user_ids = list(identity.users.get_followers())
    random.shuffle(user_ids)
    user_ids = user_ids[:2]

    i = 0
    for user_id in user_ids:
        user = identity.users.get_user(user_id)
        print("-" * 80)
        user.get_user_score()
        print("user: " + user.long_description())
        # print("tweets: " + os.linesep.join(map(lambda t: t.description(), user._get_latest_tweets())))
        # print("follower score: " + str(user.get_follower_score()))
        # print("following score: " + str(user.get_following_score()))
