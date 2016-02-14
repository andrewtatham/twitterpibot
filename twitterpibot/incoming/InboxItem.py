class InboxItem(object):
    def __init__(self):
        self.sender = None
        self.from_me = False
        self.to_me = False
        self.status_id = None
        self.is_tweet = False
        self.is_direct_message = False
        self.is_event = False
        self.is_retweet_of_my_status = False
        self.words = None
        self.in_reply_to_status_id_str = None

    def display(self):
        pass
