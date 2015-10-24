import re
from twitterpibot.twitter.MyTwitter import MyTwitter
from colorama import Fore, Style


class BotBlocker(object):
    def __init__(self):
        tooKeen = ["(follow|DM|join|retweet|contact) (me|us|back|now)"]
        pornWords = ["sexy", "naughty", "kinky", "frisky", "bored", "cum", "horny", "housewi(fe|ves?)", "teen",
                     "latina", "ass", "boobs?", "tits?", "puss(y|ies)",
                     "milf", "hoes?", "boot(y|ies)", "18+", "xxx", "slut", "babe", "dirty", "naked", "bitch"]
        businessWords = ["team", "professionals ", "Recruitment", "Training", "Leadership", "business", "discount",
                         "cheap", "betting", "industry", "casino",
                         "economic", "entrepreneur", "veture", "capital", "startup", "angel", "invest", "enterprise",
                         "special", "offerring", "custom",
                         "website", "hosting", "domain", "cms", "brand(ing)?", "media", "client", "project",
                         "TweetBoss", "marketing", "promotion", "leverage", "influence", "happylowuk[\\d]"]
        tooKeenRx = re.compile("|".join(tooKeen), re.IGNORECASE)
        businessRx = re.compile("|".join(businessWords), re.IGNORECASE)
        pornRx = re.compile("|".join(pornWords), re.IGNORECASE)
        self.rxs = [(tooKeenRx, 5), (pornRx, 4), (businessRx, 1)]

    def IsUserBot(self, user):
        blockFollower = False
        score = 0
        if not user.verified and not user.isFriend and not user.description:
            score += 7

        searchText = ""
        if user.name:
            searchText += user.name
        if user.screen_name:
            searchText += user.screen_name
        if user.description:
            searchText += user.description

        for rx in self.rxs:
            matches = rx[0].findall(searchText)
            if any(matches):
                score += rx[1] * len(matches)
        if score > 10:
            blockFollower = True
        if not blockFollower:
            with MyTwitter() as twitter:
                lastTweets = twitter.get_user_timeline(user_id=user.id,
                                                       screen_name=user.screen_name,
                                                       trim_user=True,
                                                       count=20)
                searchText = ""
                for tweet in lastTweets:
                    searchText += tweet["text"]
                for rx in self.rxs:
                    matches = rx[0].findall(searchText)
                    if any(matches):
                        score += rx[1] * len(matches)
        if score > 10:
            blockFollower = True
        return blockFollower

    def BlockUser(self, user):
        txt = "[Botblock] BLOCKED: "
        if user.name:
            txt += user.name + " "
        if user.screen_name:
            txt += "[@" + user.screen_name + "] "   
        if user.description:
            txt += "- " + user.description

        print(Fore.RED + Style.BRIGHT + txt)
        with MyTwitter() as twitter:
            twitter.create_block(user_id=user.id,
                                 screen_name=user.screen_name)
