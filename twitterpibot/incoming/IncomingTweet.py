from twitterpibot.incoming.InboxItem import InboxItem
from twitterpibot.logic import english
from twitterpibot.twitter.topics import Topics

try:
    # noinspection PyUnresolvedReferences
    import html.parser

    h = html.parser.HTMLParser()
except ImportError:
    # noinspection PyUnresolvedReferences
    import HTMLParser

    h = HTMLParser.HTMLParser()

from itertools import cycle
from colorama import Fore, Style

import logging

logger = logging.getLogger(__name__)

tweetcolours = cycle([Fore.GREEN, Fore.WHITE])
trendcolours = cycle([Fore.MAGENTA, Fore.WHITE])
searchcolours = cycle([Fore.CYAN, Fore.WHITE])
streamcolours = cycle([Fore.YELLOW, Fore.WHITE])


class Coordinates(object):
    def __init__(self, data):
        if data["type"] == "Point":
            coordinates = data["coordinates"]
            if coordinates:
                self.lat = coordinates[0]
                self.long = coordinates[1]


class IncomingTweet(InboxItem):
    def __init__(self, data, identity):
        # https://dev.twitter.com/overview/api/tweets

        super(IncomingTweet, self).__init__(data, identity)
        self.identity_screen_name = identity.screen_name
        self.is_tweet = True
        self.status_id = data.get("id_str")
        self.sender = identity.users.get_user(user_data=data.get("user"))
        self.from_me = self.sender and self.sender.isMe
        self.favorited = bool(data.get("favorited"))
        self.retweeted = bool(data.get("retweeted"))
        self.in_reply_to_status_id_str = data.get("in_reply_to_status_id_str")

        self.source = data.get('tweet_source')
        self.sourceIsTrend = self.source and 'trend' in self.source
        self.sourceIsSearch = self.source and 'search' in self.source
        self.sourceIsStream = self.source and 'stream' in self.source

        self.text = data.get("text")
        if self.text:
            self.text = h.unescape(self.text)
            self.topics = Topics.get_topics(self.text)
            self.to_me = False
            self.targets = []
            self.text_stripped = self.text
            self.hashtags = None
            self.mentions = None
            self.urls = None
            if "entities" in data:
                entities = data["entities"]
                if "user_mentions" in entities:
                    mentions = entities["user_mentions"]
                    self.mentions = list(map(lambda m: m["screen_name"], mentions))
                    for mention in mentions:
                        self.text_stripped = self.text_stripped.replace("@" + mention["screen_name"], "").strip()
                        if mention["screen_name"] != identity.screen_name:
                            self.targets.append(mention["screen_name"])
                        if mention["screen_name"] == identity.screen_name:
                            self.to_me = True
                if "hashtags" in entities:
                    self.hashtags = list(map(lambda h: h["text"], entities["hashtags"]))
                    self.text_stripped = self.text_stripped.replace("#", "").strip()
                if "urls" in entities:
                    for url in entities["urls"]:
                        # pprint.pprint(url)
                        self.text_stripped = self.text_stripped.replace(url["url"], "").strip()
                if "media" in entities:
                    self.has_media = True
                    for media in entities["media"]:
                        # pprint.pprint(media)
                        self.text_stripped = self.text_stripped.replace(media["url"], "").strip()

            self.words = self.text_stripped.split()
            self.words_interesting = list(filter(lambda w: w.lower() not in english.common_words, self.words))
            self.text_interesting = ""
            for word_interesting in self.words_interesting:
                self.text_interesting += " " + word_interesting

        self.coordinates = None
        coords = data.get("coordinates")
        if coords:
            self.coordinates = Coordinates(coords)

        self.retweeted_status = None
        self.is_retweet_of_my_status = False
        if "retweeted_status" in data:
            self.retweeted_status = IncomingTweet(data["retweeted_status"], identity)  # retweet recursion!

            if self.retweeted_status.from_me:
                self.is_retweet_of_my_status = True

    def display(self):
        colour = self.identity.colour
        text = "[" + self.identity_screen_name + "] "

        if self.coordinates:
            text += "({},{}) ".format(self.coordinates.lat, self.coordinates.long)

        text += self.sender.name + ' [@' + self.sender.screen_name + '] '
        text += self.text.replace('\n', ' ')

        if self.to_me:
            colour += Style.BRIGHT
        elif self.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM

        logger.info(colour + text)
