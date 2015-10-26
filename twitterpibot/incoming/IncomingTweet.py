from twitterpibot.incoming.InboxTextItem import InboxTextItem

try:
    import html.parser

    h = html.parser.HTMLParser()
except ImportError:
    import HTMLParser

    h = HTMLParser.HTMLParser()

from itertools import cycle
from colorama import Fore, Style
import twitterpibot.users.Users as Users
import twitterpibot.Identity as Identity

tweetcolours = cycle([Fore.GREEN, Fore.YELLOW])
trendcolours = cycle([Fore.MAGENTA, Fore.WHITE])
searchcolours = cycle([Fore.CYAN, Fore.WHITE])


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
        if 'tweetsource' in data:
            self.source = data['tweetsource']
            if 'trend' in self.source:
                self.sourceIsTrend = True
            elif 'search' in self.source:
                self.sourceIsSearch = True

        self.text = h.unescape(data["text"])
        self.words = self.text.split()

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

    def Display(self):
        colour = ""
        text = ""
        if self.source:
            text += '[' + self.source + '] '
            if self.sourceIsTrend:
                colour = next(trendcolours)
            elif self.sourceIsSearch:
                colour = next(searchcolours)
        else:
            colour = next(tweetcolours)
            text += "* "

        text += self.sender.name + ' [@' + self.sender.screen_name + '] ' + self.text.replace('\n', ' ')

        if self.to_me:
            colour += Style.BRIGHT
        elif self.from_me:
            colour += Style.NORMAL
        else:
            colour += Style.DIM

        print(colour + text)
