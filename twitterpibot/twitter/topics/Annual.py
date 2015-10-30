from twitterpibot.twitter.topics.Topic import Topic


class Halloween(Topic):
    def __init__(self):
        super(Halloween, self).__init__(["Halloween"])

    

def get():
    return [Halloween()]
