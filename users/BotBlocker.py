import re
from MyTwitter import MyTwitter

class BotBlocker(object):
    def IsUserBot(self, userid, username, screen_name, description):
        print("[Botblock] checking: " + username + " [@" + screen_name + "] " + description)
        blockFollower = False
        score = 0
        if not description:
            # description is blank
            score += 7
        searchText = username + screen_name + description
        for rx in self.rxs:
            match = rx[0].findall(searchText)
            print("[Botblock] Matches: " + str(match))
            score += rx[1] * len(match)
        print("[Botblock] Profile score: " + str(score))
        if score > 10:
            blockFollower = True
        if not blockFollower:
            with MyTwitter() as twitter:
                lastTweets = twitter.get_user_timeline(user_id = userid,
                    screen_name = screen_name,
                    trim_user = True,
                    count = 20)
                searchText = ""
                for tweet in lastTweets:
                    searchText += tweet["text"]

                for rx in self.rxs:
                    matches = rx[0].findall(searchText)
                    print("[Botblock] Matches: " + str(matches))
                    score += rx[1] * len(matches)

        print("[Botblock] Tweet score: " + str(score))
        if score > 10:
            blockFollower = True
        return blockFollower

    def BlockUser(self, user_id, screen_name):
        with MyTwitter() as twitter:
            twitter.create_block(user_id = user_id,
                screen_name = screen_name)
        print("BLOCKED")

    def __init__(self, *args, **kwargs):
        tooKeen = ["(follow|DM|join|retweet|contact) (me|us|back|now)"]
        pornWords = ["sexy","naughty","kinky","frisky","bored","cum","horny","housewi(fe|ves?)","teen","latina","ass","boobs?","tits?","puss(y|ies)",
                     "milf","hoes?","boot(y|ies)","cam","18+","xxx","slut","babe","dirty","naked","bitch"]
        businessWords = ["team","professionals ","Recruitment", "Training","Leadership","business","discount","cheap","betting","industry","casino",
                         "economic","entrepreneur","veture","capital","startup","angel","invest","enterprise","special", "offerring", "custom",
                         "website","hosting","domain","cms","brand(ing)?","media","client","project"]
        tooKeenRx = re.compile("|".join(tooKeen), re.IGNORECASE)
        businessRx = re.compile("|".join(businessWords), re.IGNORECASE)
        pornRx = re.compile("|".join(pornWords), re.IGNORECASE)
        self.rxs = [(tooKeenRx, 5), (pornRx, 4), (businessRx, 1)]
        return super(BotBlocker, self).__init__(*args, **kwargs)
