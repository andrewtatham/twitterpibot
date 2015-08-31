import re
from MyTwitter import MyTwitter
from colorama import Fore, Style

class BotBlocker(object):
    def IsUserBot(self, user):
        #print("[Botblock] checking: " + user.name + " [@" + user.screen_name + "] " + user.description)
        blockFollower = False
        score = 0
        if not user.verified and not user.isFriend and not user.description:
            # description is blank
            score += 7
        searchText = user.name + user.screen_name + user.description
        for rx in self.rxs:
            matches = rx[0].findall(searchText)
            if any(matches):
                #print("[Botblock] Matches: " + str(matches))
                score += rx[1] * len(matches)
        #print("[Botblock] Profile score: " + str(score))
        if score > 10:
            blockFollower = True
        if not blockFollower:
            with MyTwitter() as twitter:
                lastTweets = twitter.get_user_timeline(user_id = user.id,
                    screen_name = user.screen_name,
                    trim_user = True,
                    count = 20)

                # todo chec against bottweets


                # todo check for similarities




                searchText = ""
                for tweet in lastTweets:
                    searchText += tweet["text"]
                for rx in self.rxs:
                    matches = rx[0].findall(searchText)
                    if any(matches):
                        #print("[Botblock] Matches: " + str(matches))
                        score += rx[1] * len(matches)

        #print("[Botblock] Tweet score: " + str(score))
        if score > 10:
            blockFollower = True
        return blockFollower

    def BlockUser(self, user):
        print(Fore.RED + Style.BRIGHT + "[Botblock] BLOCKED: " + user.name + " [@" + user.screen_name + "] " + user.description)
        with MyTwitter() as twitter:
            twitter.create_block(user_id = user.id,
                screen_name = user.screen_name)

    def __init__(self, *args, **kwargs):
        tooKeen = ["(follow|DM|join|retweet|contact) (me|us|back|now)"]
        pornWords = ["sexy","naughty","kinky","frisky","bored","cum","horny","housewi(fe|ves?)","teen","latina","ass","boobs?","tits?","puss(y|ies)",
                     "milf","hoes?","boot(y|ies)","18+","xxx","slut","babe","dirty","naked","bitch"]
        businessWords = ["team","professionals ","Recruitment", "Training","Leadership","business","discount","cheap","betting","industry","casino",
                         "economic","entrepreneur","veture","capital","startup","angel","invest","enterprise","special", "offerring", "custom",
                         "website","hosting","domain","cms","brand(ing)?","media","client","project","TweetBoss", "marketing", "promotion", "leverage", "influence","happylowuk[\\d]"]
        tooKeenRx = re.compile("|".join(tooKeen), re.IGNORECASE)
        businessRx = re.compile("|".join(businessWords), re.IGNORECASE)
        pornRx = re.compile("|".join(pornWords), re.IGNORECASE)
        self.rxs = [(tooKeenRx, 5), (pornRx, 4), (businessRx, 1)]
        return super(BotBlocker, self).__init__(*args, **kwargs)
