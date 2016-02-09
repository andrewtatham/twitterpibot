from twitterpibot.twitter.topics.Topic import SpamTopic


class TooKeen(SpamTopic):
    def __init__(self):
        super(TooKeen, self).__init__(
            ["(follow|DM|join|retweet|contact) (me|us|back|now)"]
        )


class SmutSpam(SpamTopic):
    def __init__(self):
        super(SmutSpam, self).__init__(
            ["kinky", "frisky", "cum", "horny", "housewi(fe|ves?)", "boobs?", "tits?", "puss(y|ies)",
             "milf", "hoes?", "boot(y|ies)", "18\+", "slut", "bitch"],
            ["latina", "sexy", "ass", "dirty", "naked", "naughty", "bored", "teen", "sex", "xxx", "babe"]
        )


class BizSpam(SpamTopic):
    def __init__(self):
        super(BizSpam, self).__init__(
            ["Buy followers"]
        )


class Clickbait(SpamTopic):
    def __init__(self):
        super(Clickbait, self).__init__(
            [
                "Which .* character are you",
                "[\d]+ .* (you'?(r|re|ll)?|only|that|why|would|success|for|to|do)",
                "before you die",
                "is this the",
                "you probably didn't",
                "are the most",
                "in your life",
                "(things|reasons) you (probably|should)",
                "most (important|outrageous|awesome|cutest)",
                "will blow your mind",
                "signs you're",
                "what (is|are)"
            ]
        )


def get():
    return [
        TooKeen(),
        SmutSpam(),
        BizSpam(),
        Clickbait()
    ]
