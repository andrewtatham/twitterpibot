import logging
import random
import abc

mentioned_reply_less = 4  # reply less

bot_unmentioned_reply = 100
unmentioned_reply = 1000

friend_rt_fav = 100
rt_more = 100
bot_rt_fav = 1000
random_rt_fav = 1000

logger = logging.getLogger(__name__)


def one_in(prob):
    return random.randint(0, prob - 1) == 0


class Response(object):
    def __init__(self, identity):
        self.identity = identity

    @abc.abstractmethod
    def condition(self, inbox_item):
        return False

    @abc.abstractmethod
    def respond(self, inbox_item):
        return None


def mentioned_reply_condition(inbox_item):
    mentioned = (inbox_item.is_direct_message or inbox_item.is_tweet) \
                and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status \
                and inbox_item.to_me \
                and not inbox_item.from_me \
                and inbox_item.sender \
                and (not inbox_item.sender.is_reply_less or one_in(mentioned_reply_less)) \
                and inbox_item.sender.screen_name != "numberwang_host"
    logger.debug("to_me = {}".format(inbox_item.to_me))
    logger.debug("mentioned = {}".format(mentioned))
    return mentioned


def unmentioned_reply_condition(inbox_item):
    unmentoned = inbox_item.is_tweet and not inbox_item.from_me and not inbox_item.is_retweet_of_my_status and \
                 (
                     (inbox_item.sender.is_awesome_bot and one_in(bot_unmentioned_reply)) or
                     (inbox_item.sender.is_possibly_bot and one_in(bot_unmentioned_reply)) or
                     one_in(unmentioned_reply)
                 )

    logger.debug("unmentioned = {}".format(unmentoned))
    return unmentoned


def retweet_condition(inbox_item):
    return inbox_item.is_tweet and \
           not inbox_item.from_me and \
           not inbox_item.to_me and \
           not (
               inbox_item.retweeted or
               inbox_item.retweeted_status and
               inbox_item.retweeted_status.retweeted
           ) and \
           not inbox_item.sender.protected and \
           not inbox_item.sender.is_arsehole and \
           not (
               inbox_item.sender.is_do_not_retweet or
               inbox_item.retweeted_status and
               inbox_item.retweeted_status.sender.is_do_not_retweet
           ) and \
           (not inbox_item.topics or inbox_item.topics.retweet()) and \
           (
               (inbox_item.sender.is_awesome_bot and one_in(bot_rt_fav)) or
               (inbox_item.sender.is_possibly_bot and one_in(bot_rt_fav)) or
               (inbox_item.sender.is_friend and one_in(friend_rt_fav)) or
               (inbox_item.sender.is_retweet_more and one_in(rt_more)) or
               one_in(random_rt_fav))


def testing_reply_condition(inbox_item):
    return inbox_item.sender and inbox_item.sender.screen_name == "andrewtatham"


def favourite_condition(inbox_item):
    return inbox_item.is_tweet and \
           not inbox_item.from_me and \
           not inbox_item.to_me and \
           not (
               inbox_item.favorited or
               inbox_item.retweeted_status and
               inbox_item.retweeted_status.favorited
           ) and \
           not inbox_item.sender.is_arsehole and \
           (not inbox_item.topics or inbox_item.topics.retweet()) and \
           (
               (inbox_item.sender.is_awesome_bot and one_in(bot_rt_fav)) or
               (inbox_item.sender.is_possibly_bot and one_in(bot_rt_fav)) or
               (inbox_item.sender.is_friend and one_in(friend_rt_fav)) or
               one_in(random_rt_fav))
