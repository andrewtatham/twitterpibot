import random


class Response(object):
    def condition(self, inbox_item):
        return (inbox_item.is_direct_message or inbox_item.is_tweet) \
            and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
            and inbox_item.sender \
            and inbox_item.to_me and (not inbox_item.sender.is_reply_less or random.randint(0, 3) == 0)

    def respond(self, inbox_item):
        return None
