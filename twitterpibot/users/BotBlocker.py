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
    reasons = []
    profile_text = ""
    tweets_text = ""

    if not user.following and not user.verified:

        if user.name:
            profile_text += user.name
        if user.screen_name:
            profile_text += " " + user.screen_name
        if user.description:
            profile_text += " " + user.description

        logger.info("Checking user profile: " + profile_text)

        profile_topics = Topics.get_topics(profile_text)
        if profile_topics:
            logger.info("Profile topics:" + str(profile_topics))
            block_follower = profile_topics.spam()
            reasons.append(str(profile_topics))

        if not block_follower and (user.following or not user.protected):

            last_tweets = get_tweets(user)

            for tweet in last_tweets:
                tweets_text += tweet["text"] + os.linesep
            logger.info("Checking user tweets" + tweets_text)
            tweet_topics = Topics.get_topics(tweets_text)
            if tweet_topics:
                logger.info("User tweet topics" + str(tweet_topics))
                block_follower = tweet_topics.spam()
                reasons.append(str(tweet_topics))
    return block_follower, reasons, profile_text, tweets_text


def _block_user(user):
    Lists.add_user(list_name="Bad Bots", user_id=user.id, screen_name=user.screen_name)
    TwitterHelper.block_user(user.id, user.screen_name)


def check_user(user):
    block, reasons, text1, text2 = _is_user_bot(user)
    if block:
        txt = "[Botblock] BLOCKED: "
        txt += user.name + " [@" + user.screen_name + "] "
        txt += " Following: " + str(user.following)
        txt += " Verified: " + str(user.verified)

        if reasons:
            txt += os.linesep + "Reasons:"
            for reason in reasons:
                txt += os.linesep + reason

        if text1:
            txt += os.linesep + "Profile:"
            txt += os.linesep + text1

        if text2:
            txt += os.linesep + "Tweets:"
            txt += os.linesep + text2

        logger.warn(txt)
        TwitterHelper.send(OutgoingDirectMessage(text=txt))

    _block_user(user)
