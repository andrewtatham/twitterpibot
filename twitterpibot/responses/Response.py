import logging
import random
import abc

friend_rt_fav = 4
rt_more = 10
bot_rt_fav = 100
trend_rt_fav = 100
search_rt_fav = 100
random_rt_fav = 500

logger = logging.getLogger(__name__)


def one_in(prob):
    return random.randint(0, prob - 1) == 0


class Response(object):
    def __init__(self, identity):
        self.identity = identity

    @abc.abstractmethod
    def condition(self, inbox_item):
        return False

    def mentioned_reply_condition(self, inbox_item):
        mentioned = (inbox_item.is_direct_message or inbox_item.is_tweet) \
                    and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
                    and inbox_item.to_me \
                    and inbox_item.sender \
                    and (not inbox_item.sender.is_reply_less or one_in(4)) \
                    and inbox_item.sender.screen_name != "numberwang_host"
        logger.debug("%s mentioned: %s", self, mentioned)
        return mentioned

    def unmentioned_reply_condition(self, inbox_item):
        unmentoned = inbox_item.is_tweet and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
                     and ((inbox_item.sender.is_bot and random.randint(0, 3) == 0)
                          or (inbox_item.sender.is_friend and random.randint(0, 2) == 0)
                          or (inbox_item.sender.is_retweet_more and random.randint(0, 9) == 0)
                          or random.randint(0, 99) == 0)
        logger.debug("%s unmentoned: %s", self, unmentoned)
        return unmentoned

    def retweet_condition(self, inbox_item):
        return inbox_item.is_tweet \
               and not inbox_item.from_me \
               and not inbox_item.to_me \
               and not (inbox_item.retweeted or inbox_item.retweeted_status and inbox_item.retweeted_status.retweeted) \
               and not inbox_item.sender.protected \
               and not inbox_item.sender.is_arsehole \
               and not (inbox_item.sender.is_do_not_retweet or
                        inbox_item.retweeted_status and inbox_item.retweeted_status.sender.is_do_not_retweet) \
               and (not inbox_item.topics or inbox_item.topics.retweet()) \
               and ((inbox_item.sender.is_bot and one_in(bot_rt_fav)) or
                    (inbox_item.sender.is_friend and one_in(friend_rt_fav)) or
                    (inbox_item.sender.is_retweet_more and one_in(rt_more)) or
                    (inbox_item.sourceIsTrend and one_in(trend_rt_fav)) or
                    (inbox_item.sourceIsSearch and one_in(search_rt_fav)) or
                    one_in(random_rt_fav))

    def favourite_condition(self, inbox_item):
        return inbox_item.is_tweet \
               and not inbox_item.from_me \
               and not inbox_item.to_me \
               and not (inbox_item.favorited or inbox_item.retweeted_status and inbox_item.retweeted_status.favorited) \
               and not inbox_item.sender.is_arsehole \
               and (not inbox_item.topics or inbox_item.topics.retweet()) \
               and ((inbox_item.sender.is_bot and one_in(bot_rt_fav)) or
                    (inbox_item.sender.is_friend and one_in(friend_rt_fav)) or
                    (inbox_item.sourceIsTrend and one_in(trend_rt_fav)) or
                    (inbox_item.sourceIsSearch and one_in(search_rt_fav)) or
                    one_in(random_rt_fav))

    @abc.abstractmethod
    def respond(self, inbox_item):
        return None
