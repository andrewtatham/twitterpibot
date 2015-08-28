
from Response import Response
import re
from MyTwitter import MyTwitter


tooKeen = [
    "(follow|DM|join) (me|us|back|now)",
    ]

pornWords = [
    "sexy",
    "naughty",
    "kinky",
    "frisky",
    "bored",
    "cum",
    "horny",
    "housewi(fe|ves?)",
    "teen",
    "latina",
    "ass",
    "boob?",
    "tits?",
    "puss(y|ies)",
    "milf",
    "hoes?",
    "boot(y|ies)",
    "cam",
    "18+",
    "xxx",
    "slut",
    "babe",
    "dirty",
    "naked",
    "bitch"

    ]

businessWords = [
    "team",
    "professionals ",
    "Recruitment",
    "Training ",
    "Leadership",
    "business",
    "discount",
    "cheap",
    "betting",
    "industry",
    "casino",
    "economic ",
    "entrepreneur",
    "veture",
    "capital",
    "startup",
    "angel",
    "invest",
    "enterprise"
    ]





class BotBlocker(Response):
    def __init__(self, *args, **kwargs):

        tooKeenRx = re.compile("|".join(tooKeen))
        businessRx = re.compile("|".join(businessWords))
        pornRx = re.compile("|".join(pornWords))

        self.rxs = [
            (tooKeenRx, 5),
            (pornRx, 4),
            (businessRx, 1),
            ]

    def Condition(args, inboxItem):
        isNewFollower = inboxItem.isEvent and not inboxItem.from_me and inboxItem.to_me and inboxItem.isFollow
        if isNewFollower:
            score = 0

            # description is blank
            if not inboxItem.followerDescription: 
                score += 7


            searchText = inboxItem.followerName + inboxItem.followerScreenName + inboxItem.followerDescription
            for rx in args.rxs:

                match = rx[0].findall(searchText)
                if match:
                    score += rx[1] * len(match)


            print("Botblocker score: " + str(score))
            blockFollower = score > 10
            if blockFollower:
                print("BOTTERIFFIC")
            return blockFollower
        else:
            return False

        



        

    def Respond(args, inboxItem):
        print("BLOCKING")
        with MyTwitter() as twitter:
            twitter.create_block(
                user_id = inboxItem.sourceID,
                screen_name = inboxItem.followerScreenName)
        print("BLOCKED")

        


