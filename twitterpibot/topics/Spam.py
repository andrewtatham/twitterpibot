from twitterpibot.topics.Topic import SpamTopic


class SmutSpamSpecific(SpamTopic):
    def __init__(self):
        super(SmutSpamSpecific, self).__init__(
            [
                "selenaxxxusaxxx", "webcam789", "CAM456",
                "I can fulfill any wish for you", "show this post and get me for free",
                "Let's chat tonight! Join me!",

            ]
        )


class SmutSpamGeneral(SpamTopic):
    def __init__(self):
        super(SmutSpamGeneral, self).__init__(
            [
                "kinky", "frisky", "cum", "horny", "housewi(fe|ves?)", "boobs?", "tits?", "puss(y|ies)",
                "milf", "hoes?", "boot(y|ies)", "18 ?\+", "slut", "bitch",
                "dildo", "fuckbuddy", "adult dating"
            ], [
                "latina", "sexy", "ass", "dirty", "naked", "naughty", "bored", "teen", "sex", "xxx", "babe",
                "blonde", "redhead", "brunette"
            ]
        )


class BizSpam(SpamTopic):
    def __init__(self):
        super(BizSpam, self).__init__(
            [

                "NOW HIRING",
                "per hour jobs",
                "Learn more",
                "Apply now",

            ]
        )


class BuyFollowers(SpamTopic):
    def __init__(self):
        super(BuyFollowers, self).__init__({
            "Buy followers"
        })


class RayBanSunglasses(SpamTopic):
    def __init__(self):
        super(RayBanSunglasses, self).__init__({
            "Discount Ray Ban sunglasses"
        })


class TheRealStrategy(SpamTopic):
    def __init__(self):
        super(TheRealStrategy, self).__init__({
            "The Real Strategy", "TheRealStrategy\.com"
        })


#
# class Clickbait(SpamTopic):
#     def __init__(self):
#         super(Clickbait, self).__init__(
#             [
#                 "Which .* character are you",
#                 "[\d]+ .* (you'?(r|re|ll)?|only|that|why|would|success|for|to|do)",
#                 "before you die",
#                 "is this the",
#                 "you probably didn't",
#                 "are the most",
#                 "in your life",
#                 "(things|reasons) you (probably|should)",
#                 "most (important|outrageous|awesome|cutest)",
#                 "will blow your mind",
#                 "signs you're",
#                 "what (is|are)"
#             ]
#         )
#

def get():
    return [
        # TooKeen(),
        SmutSpamSpecific(),
        SmutSpamGeneral(),
        BizSpam(),
        BuyFollowers(),
        RayBanSunglasses(),
        TheRealStrategy(),
        # Clickbait()
    ]
