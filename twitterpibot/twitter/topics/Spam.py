from twitterpibot.twitter.topics.Topic import SpamTopic


class TooKeen(SpamTopic):
    def __init__(self):
        super(TooKeen, self).__init__(
            ["(follow|DM|join|retweet|contact) (me|us|back|now)"]
        )


class SmutSpam(SpamTopic):
    def __init__(self):
        super(SmutSpam, self).__init__(
            ["sexy", "naughty", "kinky", "frisky", "bored", "cum", "horny", "housewi(fe|ves?)", "teen",
             "latina", "ass", "boobs?", "tits?", "puss(y|ies)",
             "milf", "hoes?", "boot(y|ies)", "18+", "xxx", "slut", "babe", "dirty", "naked", "bitch", "sex"]
        )


class BizSpam(SpamTopic):
    def __init__(self):
        super(BizSpam, self).__init__(
            []
        )


def get():
    return [
        TooKeen(),
        SmutSpam()
        # ,BizSpam()
    ]
