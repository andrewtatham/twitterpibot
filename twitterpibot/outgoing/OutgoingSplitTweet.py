from twitterpibot.outgoing.OutboxTextItem import OutboxTextItem

__author__ = 'andrewtatham'


class OutgoingSplitTweet(OutboxTextItem):
    def __init__(self):
        super(OutgoingSplitTweet, self).__init__()
        self.is_tweet = True
        self.status = None
        self.media_ids = None
        self.location = None
        self.id_str = None
        self.in_reply_to_id_str = None

    def get_tweet_params(self):
        tweet_params = {
            "status": self.status
        }
        if self.media_ids:
            tweet_params["media_ids"] = self.media_ids
        if self.location:
            if self.location.latitude and self.location.longitude:
                tweet_params["lat"] = self.location.latitude
                tweet_params["long"] = self.location.longitude
            if self.location.place_id_twitter:
                tweet_params["place_id"] = self.location.place_id_twitter
        if self.in_reply_to_id_str:
            tweet_params["in_reply_to_status_id"] = self.in_reply_to_id_str
        return tweet_params
