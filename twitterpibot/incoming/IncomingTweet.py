import html
import logging
import os
from itertools import cycle

import dateutil.parser
from colorama import Fore, Style

from twitterpibot.incoming.InboxItem import InboxItem
from twitterpibot.logic import english, location
from twitterpibot.topics import topichelper

logger = logging.getLogger(__name__)

tweetcolours = cycle([Fore.GREEN, Fore.WHITE])
trendcolours = cycle([Fore.MAGENTA, Fore.WHITE])
searchcolours = cycle([Fore.CYAN, Fore.WHITE])
streamcolours = cycle([Fore.YELLOW, Fore.WHITE])


class dynamic(object):
    pass


class IncomingTweet(InboxItem):
    def __init__(self, data, identity, skip_user = False):
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
        self.favorited = bool(data.get("favorited"))
        self.retweeted = bool(data.get("retweeted"))
        self.created_at = dateutil.parser.parse(data.get("created_at"))
        self.in_reply_to_id_str = data.get("in_reply_to_status_id_str")
        self.mentions = []
        self.urls = []
        self.medias = []
        self.text_stripped = ""
        self._text(data, identity)

        self._location(data)

        self._retweet(data, identity, skip_user)

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
        self.text = data.get("text")
        if self.text:
            self.text = html.unescape(self.text)
            self.topics = topichelper.get_topics(self.text)
            self.to_me = False

            self.text_stripped = self.text
            self._entities(data, identity)

            self.english = english.get_common_words(self.text_stripped)

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
                self.medias = entities["media"]
                for media in entities["media"]:
                    self.has_media = True
                    logger.debug("media: {}".format(media))

                    self.replace_entity(media["indices"])

    def display(self):
        colour = self.identity.colour
        text = "[" + self.identity_screen_name + "] "

        if self.location:
            text += " location = " + str(self.location)

        text += self.sender.short_description()

        text += " " + self.text.replace(os.linesep, ' ')

        if self.to_me:
            colour += Style.BRIGHT
        elif self.from_me:
            colour += Style.BRIGHT
        else:
            colour += Style.NORMAL

        logger.info("=" * 80)
        logger.info(colour + text)

        logger.info("         text: " + self.text.replace(os.linesep, ' '))
        logger.info("text_stripped: " + self.text_stripped.replace(os.linesep, ' '))
        logger.info("       common: " + str(self.english["common"]))
        logger.info("     uncommon: " + str(self.english["uncommon"]))

        if self.conversation:
            self.conversation.display()

    def description(self):
        text = ""
        text += "text: " + self.text.replace(os.linesep, ' ')
        if self.medias:
            for media in self.medias:
                text += os.linesep + "medis: " + media["type"] + " " + media["expanded_url"]
        if self.urls:
            for url in self.urls:
                text += os.linesep + "url: " + url["expanded_url"]

        return text

    def replace_entity(self, indices):
        start = indices[0]
        end = indices[1]
        length = end - start

        self.text_stripped = self.text_stripped[:start] + " " * length + self.text_stripped[end:]


if __name__ == '__main__':
    import identities

    logging.basicConfig(level=logging.INFO)
    identity = identities.AndrewTathamPiIdentity(None)
    tweets = identity.twitter.get_user_timeline()
    for tweet_data in tweets:
        tweet = IncomingTweet(tweet_data, identity)
        tweet.display()
