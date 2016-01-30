import logging
import os
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.twitter import Lists
import twitterpibot.twitter.TwitterHelper as TwitterHelper
from twitterpibot.twitter.topics import Topics

logger = logging.getLogger(__name__)


get_tweets = TwitterHelper.get_user_timeline

def _is_user_bot(user):
    block_follower = False
    reasons=[]

    if not user.following and not user.verified:

        search_text = ""
        if user.name:
            search_text += user.name
        if user.screen_name:
            search_text += " " + user.screen_name
        if user.description:
            search_text += " " + user.description

        logger.info("Checking user profile: " + search_text)

        topics1 = Topics.get_topics(search_text)
        if topics1:
            logger.info("Profile topics:" + str(topics1))
            block_follower = topics1.spam()
            reasons.append(str(topics1))

        if not block_follower and (user.following or not user.protected):

            last_tweets = get_tweets(user)

            search_text = ""
            for tweet in last_tweets:
                search_text += tweet["text"]
            logger.info("Checking user tweets" + search_text)
            topics2 = Topics.get_topics(search_text)
            if topics2:
                logger.info("User tweet topics" + str(topics2))
                block_follower = topics2.spam()
                reasons.append(str(topics2))
    return block_follower, reasons


def _block_user(user):
    Lists.add_user(list_name="Bad Bots", user_id=user.id, screen_name=user.screen_name)
    TwitterHelper.block_user(user.id, user.screen_name)


def check_user(user):
    block, reasons = _is_user_bot(user)
    if block:

        txt = "[Botblock] BLOCKED: "
        if user.name:
            txt += user.name + " "
        if user.screen_name:
            txt += "[@" + user.screen_name + "] "
        if user.description:
            txt += os.linesep + user.description
        if reasons:
            txt += os.linesep + "Reasons:"
            for reason in reasons:
                txt += os.linesep + reason

        logger.warn(txt)
        TwitterHelper.send(OutgoingDirectMessage(text=txt))

        _block_user(user)
