from twitterpibot.topics.Topic import GoodTopic


class MyFaceWhen(GoodTopic):
    def __init__(self):
        super(MyFaceWhen, self).__init__([
            "mfw"
        ], except_regexes=["milan", "fashion"])


class NyanCat(GoodTopic):
    def __init__(self):
        super(NyanCat, self).__init__([
            "Nyan Cat"
        ])


# todo memes

def get():
    return [
        MyFaceWhen(),
        NyanCat()
    ]
