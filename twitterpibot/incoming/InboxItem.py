class InboxItem(object):
    def __init__(self):
        self.from_me = False
        self.to_me = False
        self.status_id = None
        self.isTweet = False
        self.isDirectMessage = False
        self.isEvent = False

        self.isRespondedTo = False

    def Display(self):
        pass
