from twitterpibot.incoming.InboxTextItem import InboxTextItem
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
import twitterpibot.users.Users as Users
import twitterpibot.Identity as Identity
import logging
logger = logging.getLogger(__name__)

tweetcolours = cycle([Fore.GREEN, Fore.WHITE])
trendcolours = cycle([Fore.MAGENTA, Fore.WHITE])
searchcolours = cycle([Fore.CYAN, Fore.WHITE])
streamcolours = cycle([Fore.YELLOW, Fore.WHITE])

class IncomingTweet(InboxTextItem):
    def __init__(self, data):
        # https://dev.twitter.com/overview/api/tweets

        super(IncomingTweet, self).__init__()

        self.isTweet = True
        self.status_id = data["id_str"]
        self.sender = Users.getUser(data=data["user"])
        self.from_me = self.sender.isMe
        self.favorited = bool(data["favorited"])
        self.retweeted = bool(data["retweeted"])
        self.source = None
        self.sourceIsTrend = False
        self.sourceIsSearch = False
        self.sourceIsStream = False
        if 'tweetsource' in data:
            self.source = data['tweetsource']
            if 'trend' in self.source:
                self.sourceIsTrend = True
            elif 'search' in self.source:
                self.sourceIsSearch = True
            elif 'stream' in self.source:
                self.sourceIsStream = True

        self.text = h.unescape(data["text"])
        self.words = self.text.split()

        self.topic = Topics.get_topic(self.text)

        self.to_me = False
        self.targets = []
        if "entities" in data:
            entities = data["entities"]

            if "user_mentions" in entities:
                mentions = entities["user_mentions"]
                for mention in mentions:
                    if mention["id_str"] != Identity.twid:
                        self.targets.append(mention["screen_name"])

                    if mention["id_str"] == Identity.twid:
                        self.to_me = True

    def display(self):
        colour = ""
        text = ""
        if self.source:
            text += '[' + self.source + '] '
            if self.sourceIsTrend:
                colour = next(trendcolours)
            elif self.sourceIsSearch:
                colour = next(searchcolours)
            elif self.sourceIsStream:
                colour = next(streamcolours)
        else:
            colour = next(tweetcolours)
            text += "[user] "

        if self.topic:
            text += "{topic: " + str(self.topic) + "} "

        text += self.sender.name + ' [@' + self.sender.screen_name + '] ' + self.text.replace('\n', ' ')

        if self.to_me:
            colour += Style.BRIGHT
        elif self.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM

        logger.info(colour + text)
