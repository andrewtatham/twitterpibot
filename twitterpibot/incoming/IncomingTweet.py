import html
import logging
import os
import pprint
from itertools import cycle

import dateutil.parser
from colorama import Fore, Style

from twitterpibot.incoming.InboxItem import InboxItem
from twitterpibot.logic import english, location, unicode_helper
from twitterpibot.logic.string_helper import clean_string
from twitterpibot.topics import topichelper
from twitterpibot.users.scores import TweetScore

logger = logging.getLogger(__name__)

tweetcolours = cycle([Fore.GREEN, Fore.WHITE])
trendcolours = cycle([Fore.MAGENTA, Fore.WHITE])
searchcolours = cycle([Fore.CYAN, Fore.WHITE])
streamcolours = cycle([Fore.YELLOW, Fore.WHITE])


class dynamic(object):
    pass


class Media(object):
    def __init__(self, data):
        self._data = data
        self.type = data["type"]
        self.sizes = data["sizes"]
        self.indices = data["indices"]

        self.display_url = data["display_url"]
        self.expanded_url = data["expanded_url"]
        self.media_url_https = data["media_url_https"]
        self.url = data["url"]

    def __str__(self):
        return pprint.pformat(self._data)

    def short_description(self):
        text = self.display_url + " -> " + self.url
        # text += os.linesep + " [ " + self.expanded_url + " ]"
        # text += os.linesep + " L: " + self.get_large()
        # text += os.linesep + " M: " + self.get_medium()
        # text += os.linesep + " S: " + self.get_small()
        # text += os.linesep + " T: " + self.get_thumbnail()
        return text

    def get_large(self):
        return self._get_size("large")

    def get_medium(self):
        return self._get_size("medium")

    def get_small(self):
        return self._get_size("small")

    def get_thumbnail(self):
        return self._get_size("thumb")

    def _get_size(self, size):
        if size in self.sizes:
            return self.media_url_https + ":" + size
        else:
            return self.media_url_https


class Medias(object):
    def __init__(self, data):
        self._data = data
        self._medias = []
        for media in data:
            self._medias.append(Media(media))

    def __str__(self):
        return pprint.pformat(self._data)

    def __iter__(self):
        return iter(self._medias)

    def __len__(self):
        return len(self._medias)

    def __getitem__(self, item):
        return self._medias.__getitem__(item)


class IncomingTweet(InboxItem):
    def __init__(self, data, identity=None, skip_user=False):
        # https://dev.twitter.com/overview/api/tweets

        super(IncomingTweet, self).__init__(data, identity)
        if identity:
            self.identity_screen_name = identity.screen_name
            if not skip_user:
                self.sender = identity.users.get_user(user_data=data.get("user"))
                self.from_me = self.sender and self.sender.is_me
        else:
            self.sender = dynamic()
            self.sender.screen_name = data.get("sender_screen_name")
            self.sender.is_me = False
        self.is_tweet = True
        self.id_str = data.get("id_str")
        self.url = None
        if self.sender and self.id_str:
            self.url = "https://twitter.com/{}/status/{}".format(self.sender.screen_name, self.id_str)
        self.lang = data.get("lang")
        if self.lang and self.lang == "und":
            self.lang = None
        self.possibly_sensitive = bool(data.get("possibly_sensitive"))
        self.favorited = bool(data.get("favorited"))
        self.retweeted = bool(data.get("retweeted"))
        self.favorite_count = data.get("favorite_count")
        if self.favorite_count: self.favorite_count = int(self.favorite_count)
        self.retweet_count = data.get("retweet_count")
        if self.retweet_count: self.retweet_count = int(self.retweet_count)
        self.created_at = data.get("created_at")
        self.source = "source"
        if self.created_at:
            self.created_at = dateutil.parser.parse(self.created_at)
        self.in_reply_to_id_str = data.get("in_reply_to_status_id_str")
        self.quoted_status_id_str = data.get("quoted_status_id_str")
        self.mentions = []
        self.urls = []
        self.medias = []
        self.text_stripped = ""
        self.text_stripped_whitespace_removed = ""
        self._text(data, identity)

        self._location(data)

        self.retweeted_status = None
        self._retweet(data, identity, skip_user)

        self.quoted_status = None
        self._quote_tweet(data, identity)

        topic_text = self.text
        if self.quoted_status:
            topic_text += os.linesep + self.quoted_status.text
        if self.retweeted_status:
            topic_text += os.linesep + self.retweeted_status.text

        self.topics = None
        if topic_text:
            self.topics = topichelper.get_topics(topic_text)

        self._classification = None
        self.tweet_score = TweetScore(self)

    def _retweet(self, data, identity, skip_user):
        self.retweeted_status = None
        self.is_retweet_of_my_status = False
        if "retweeted_status" in data:
            self.retweeted_status = IncomingTweet(data["retweeted_status"], identity, skip_user)  # retweet recursion!

            if self.retweeted_status.from_me:
                self.is_retweet_of_my_status = True

    def _location(self, data):
        self.location = None
        place = data.get("place")
        coordinates = data.get("coordinates")
        if place or coordinates:
            self.location = location.Location(
                tweet_coordinates=coordinates,
                tweet_place=place)

    def _text(self, data, identity):
        self.text = clean_string(data.get("text"))
        if self.text:
            self.text = self.text
            self.to_me = False

            self.text_stripped = self.text
            self._entities(data, identity)
            self.english = english.get_common_words(self.text_stripped)

            self.text_stripped_whitespace_removed = self.text_stripped
            while "  " in self.text_stripped_whitespace_removed:
                self.text_stripped_whitespace_removed = self.text_stripped_whitespace_removed.replace("  ", " ")

            self._classification = unicode_helper.analyse(self.text_stripped_whitespace_removed)

    def _entities(self, data, identity):

        if "entities" in data:
            entities = data["entities"]
            if "user_mentions" in entities:
                mentions = entities["user_mentions"]
                for mention in mentions:
                    logger.debug("mention: {}".format(mention))
                    self.replace_entity(mention["indices"])
                    if mention["screen_name"] != identity.screen_name:
                        self.mentions.append(mention["screen_name"])
                    if mention["screen_name"] == identity.screen_name:
                        self.to_me = True
            if "hashtags" in entities:
                hashtags = entities["hashtags"]
                for hashtag in hashtags:
                    logger.debug("hashtag: {}".format(hashtag))
                    # self.replace_entity(hashtag["indices"])
            if "urls" in entities:
                self.urls = entities["urls"]
                for url in entities["urls"]:
                    logger.debug("url: {}".format(url))
                    self.replace_entity(url["indices"])

            if "media" in entities:
                self.medias = Medias(entities["media"])

                for media in entities["media"]:
                    self.has_media = True
                    logger.debug("media: {}".format(media))

                    self.replace_entity(media["indices"])

    def short_display(self):
        text = ""
        if self.sender:
            text += self.sender.short_display()
        text += ": " + self.text.replace(os.linesep, ' ')
        return text

    def short_description(self):
        text = ""
        if self.sender:
            text += self.sender.short_description()
        if self.tweet_score:
            text += " tweet score:{}".format(self.tweet_score.total())

        text += " " + self.text.replace(os.linesep, ' ')
        return text

    def display(self):
        colour = self.identity.colour
        if self.to_me:
            colour += Style.BRIGHT
        elif self.from_me:
            colour += Style.BRIGHT
        else:
            colour += Style.NORMAL

        text = colour

        text += "[" + self.identity_screen_name + "] "
        text += self.short_description()

        n = 16
        if self.text:
            text += os.linesep + "text: ".rjust(n, " ") + self.text.replace(os.linesep, ' ')
        if self.text_stripped and self.text_stripped != self.text:
            text += os.linesep + "text_stripped: ".rjust(n, " ") + self.text_stripped.replace(os.linesep, ' ')
        if self.text_stripped_whitespace_removed and self.text_stripped_whitespace_removed != self.text_stripped:
            text += os.linesep + "text_stripped_whitespace_removed: ".rjust(n, " ") \
                    + self.text_stripped_whitespace_removed.replace(os.linesep, ' ')
        if self._classification:
            text += os.linesep + "classification: ".rjust(n, " ") + str(self._classification)
        if self.english:
            if self.english["common"]:
                text += os.linesep + "common: ".rjust(n, " ") + str(self.english["common"])
            if self.english["uncommon"]:
                text += os.linesep + "uncommon: ".rjust(n, " ") + str(self.english["uncommon"])
        if self.location:
            text += os.linesep + "location: ".rjust(n, " ") + str(self.location)
        if self.lang:
            text += os.linesep + "lang: ".rjust(n, " ") + str(self.lang)
        if self.medias:
            for media in self.medias:
                text += os.linesep + (media.type + ": ").rjust(n, " ") + media.short_description()
        if self.urls:
            for url in self.urls:
                if "expanded_url" in url and url["expanded_url"]:
                    text += os.linesep + "url: ".rjust(n, " ") + url["expanded_url"]

        if self.conversation:
            text += os.linesep + "conversation: ".rjust(n, " ") + self.conversation.display()

        if self.quoted_status:
            text += os.linesep + "quoted_status: ".rjust(n, " ") + self.quoted_status.short_description()

        if self.tweet_score:
            text += os.linesep + "tweet_score: ".rjust(n, " ") + str(self.tweet_score)

        return text

    def replace_entity(self, indices):
        start = indices[0]
        end = indices[1]
        length = end - start

        self.text_stripped = self.text_stripped[:start] + " " * length + self.text_stripped[end:]

    def _quote_tweet(self, data, identity):
        if "quoted_status" in data:
            self.quoted_status = IncomingTweet(data.get("quoted_status"), identity)
            self.is_quote_of_my_status = self.quoted_status.from_me


if __name__ == '__main__':
    import identities_pis

    logging.basicConfig(level=logging.INFO)

    identity = identities_pis.AndrewTathamPiIdentity(None)

    id_str = "757389498254659584"
    tweet_data = identity.twitter.get_status(id_str)
    logger.info(pprint.pformat(tweet_data))
    tweet = IncomingTweet(tweet_data, identity)
    logger.info(tweet.display())

    # tweets = identity.twitter.get_user_timeline()

    # id_strs = [
    #
    # ]
    # tweets = identity.twitter.get_statuses(id_strs)

    # for tweet_data in tweets:
    #     tweet = IncomingTweet(tweet_data, identity)
    #     logger.info(tweet.display())
