class OutboxItem(object):
    def __init__(self):
        self.is_tweet = False
        self.is_direct_message = False

        # Tweets
        self.status = None
        self.mentions = None
        self.media_ids = None
        self.in_reply_to_id_str = None

        # DM
        self.user_id = None
        self.screen_name = None
        self.text = None

    def display(self):
        pass
