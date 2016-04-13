from twitterpibot.outgoing.OutboxTextItem import OutboxTextItem

__author__ = 'andrewtatham'


class OutgoingSplitTweet(OutboxTextItem):
    def __init__(self, is_first, status, media_ids, outbox_item):
        super(OutgoingSplitTweet, self).__init__()
        self.tweet_params = {
            "status": status
        }
        self.is_tweet = True

        if is_first and media_ids:
            self.tweet_params["media_ids"] = media_ids
        if outbox_item.location:
            self.tweet_params["lat"] = outbox_item.location.latitude,
            self.tweet_params["long"] = outbox_item.location.longitude,
            self.tweet_params["place_id"] = outbox_item.location.place_id_twitter

    def get_tweet_params(self, in_reply_to_id_str):
        if in_reply_to_id_str:
            self.tweet_params["in_reply_to_status_id"] = in_reply_to_id_str
        return self.tweet_params
