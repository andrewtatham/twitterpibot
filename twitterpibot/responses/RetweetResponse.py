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

    def Condition(self, inbox_item):
        return inbox_item.isTweet \
               and not inbox_item.from_me \
               and not inbox_item.to_me \
               and not inbox_item.retweeted \
               and not inbox_item.sender.protected \
               and not inbox_item.sender.isArsehole \
               and not bool(self.rx.match(inbox_item.text)) \
               and ((inbox_item.sender.isBot and random.randint(0, 50) == 0) or
                    (inbox_item.sender.isFriend and random.randint(0, 3) == 0) or
                    (inbox_item.sender.isRetweetMore and random.randint(0, 9) == 0) or
                    (inbox_item.sourceIsTrend and random.randint(0, 20) == 0) or
                    (inbox_item.sourceIsSearch and random.randint(0, 20) == 0) or
                    (random.randint(0, 99) == 0))

    def Favourite(self, inbox_item):
        return False

    def Respond(self, inbox_item):
        with MyTwitter() as twitter:
            twitter.retweet(id=inbox_item.status_id)
