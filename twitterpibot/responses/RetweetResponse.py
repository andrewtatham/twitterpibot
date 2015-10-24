import random
import re

from Response import Response
from twitterpibot.twitter.MyTwitter import MyTwitter


class RetweetResponse(Response):
    def __init__(self):
        self.bannedTopics = [
            # RT to Win
            "(RT|Retweet|chance|follow).*(to|2).*win",

            # RT/Fav voting
            "(RT|Retweet).*(Fav)",
            "(Fav).*(RT|Retweet)",

            # Football

            # Job Adverts
            "is.*(looking for|hiring)",
            "Jobs available",
            "Apply now"
        ]

        self.rx = re.compile("|".join(self.bannedTopics), re.IGNORECASE)

    def Condition(self, inboxItem):
        return inboxItem.isTweet \
               and not inboxItem.from_me \
               and not inboxItem.to_me \
               and not inboxItem.retweeted \
               and not inboxItem.sender.protected \
               and not inboxItem.sender.isArsehole \
               and not bool(self.rx.match(inboxItem.text)) \
               and ((inboxItem.sender.isBot and random.randint(0, 50) == 0) or
                    (inboxItem.sender.isFriend and random.randint(0, 3) == 0) or
                    (inboxItem.sender.isRetweetMore and random.randint(0, 9) == 0) or
                    (inboxItem.sourceIsTrend and random.randint(0, 20) == 0) or
                    (inboxItem.sourceIsSearch and random.randint(0, 20) == 0) or
                    (random.randint(0, 99) == 0))

    def Favourite(self, inboxItem):
        return False

    def Respond(self, inboxItem):
        with MyTwitter() as twitter:
            twitter.retweet(id=inboxItem.status_id)