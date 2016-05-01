class InboxItem(object):
    def __init__(self, data, identity):
        self.data = data
        self.identity = identity
        self.sender = None
        self.from_me = False
        self.to_me = False
        self.id_str = None
        self.is_tweet = False
        self.is_direct_message = False
        self.is_event = False
        self.is_retweet_of_my_status = False
        self.words = None
        self.in_reply_to_id_str = None
        self.has_media = False
        self.text = None
        self.text_stripped = None
        self.conversation = None

    def display(self):
        pass
