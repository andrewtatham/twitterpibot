import random


class Response(object):
    def condition(self, inbox_item):
        return (inbox_item.is_direct_message or inbox_item.is_tweet) \
               and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
               and (inbox_item.to_me and (not inbox_item.sender.is_reply_less or random.randint(0, 3) == 0)
                    or (inbox_item.sender.is_bot and random.randint(0, 3) == 0)
                    or (inbox_item.sender.is_friend and random.randint(0, 1) == 0)
                    or (inbox_item.sender.is_retweet_more and random.randint(0, 9) == 0)
                    or random.randint(0, 99) == 0)

    def favourite(self, inbox_item):
        return False

    def respond(self, inbox_item):
        return None
