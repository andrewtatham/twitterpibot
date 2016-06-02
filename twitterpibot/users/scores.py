import datetime

from twitterpibot.logic import unicode_helper


class Score(object):
    def __init__(self):
        self._scores = {"total": 0}
        self._created = datetime.datetime.utcnow()

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

    def extend(self, topics_score):
        if topics_score:
            for k, v in topics_score.items():
                self.add(v, k)

    # todo move to topics
    def get_topic_score(self, topics):
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
            self.extend(user_score)

    def score_lang(self, lang):
        if lang == "en-gb":
            self.add(5, "the queens english")
        elif lang == "en-US":
            self.add(-5, "bloody yanks")
        elif lang != "en":
            self.add(-10, "bloody foreigners")

    def is_stale(self):
        return datetime.datetime.utcnow() - self._created > datetime.timedelta(days=2)


class UserScore(Score):
    def __init__(self, user, include_recent_tweets_score=False):
        super(UserScore, self).__init__()
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

        self.score_lang(user.lang)

        if user.status:
            last_tweet_score = user.status.tweet_score.total()
            self.add(last_tweet_score, "last_tweet_score")

        if user.last_tweeted_at:
            delta = user.get_last_tweet_delta()
            if delta.days >= 60:
                last_tweeted_score = -int(delta.days * 50 / 365)
                self.add(last_tweeted_score, "last tweeted " + user.get_last_tweeted())

        self.include_recent_tweets_score = include_recent_tweets_score
        if include_recent_tweets_score:
            tweets = user.get_latest_tweets()
            if tweets:
                tweet_score = 0
                for tweet in tweets:
                    if tweet.tweet_score:
                        tweet_score += tweet.tweet_score.total()
                        self.add(tweet_score, "tweet_score for id {}".format(tweet.id_str))
            else:
                # todo if user has never tweeted
                self.include_recent_tweets_score = False


class TweetScore(Score):
    def __init__(self, tweet):
        super(TweetScore, self).__init__()

        self.score_lang(tweet.lang)

        if tweet.favorite_count:
            self.add(int(tweet.favorite_count / 1000), "favorite_count")
        if tweet.retweet_count:
            self.add(int(tweet.retweet_count / 1000), "retweet_count")

        if tweet.has_media:
            # todo score gifs higher
            self.add(2 * len(tweet.medias), "medias")

        if tweet.location:
            self.add(2, "location: {}".format(tweet.location))

        if tweet._classification and isinstance(tweet._classification, unicode_helper.UnicodeArt):
            self.add(5, "UnicodeArt")

        if tweet.topics:
            self.get_topic_score(tweet.topics)
