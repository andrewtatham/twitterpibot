from collections import Counter
import logging
import os

import twitterpibot.outgoing.OutgoingDirectMessage
import twitterpibot.twitter.twitterhelper
from twitterpibot.twitter.topics import Topics

logger = logging.getLogger(__name__)

get_tweets = get_user_timeline


def _is_user_bot(identity, user):
    block_follower = False
    reasons = []
    profile_text = ""
    tweets_text = ""

    if not user.following and not user.verified:

        if user.name:
            profile_text += user.name
        if user.screen_name:
            profile_text += " @" + user.screen_name
        if user.description:
            profile_text += " " + user.description

        logger.info("Checking user profile: " + profile_text)

        profile_topics = Topics.get_topics(profile_text)
        if profile_topics:
            logger.info("Profile topics: " + str(profile_topics))
            block_follower = profile_topics.spam()
            reasons.append(str(profile_topics))

        if not block_follower and (user.following or not user.protected):

            last_tweets = get_tweets(identity, user)

            for tweet in last_tweets:
                tweets_text += tweet["text"] + os.linesep

            if tweets_text:
                logger.info("Checking user tweets: " + tweets_text)

                word_count = Counter(tweets_text.split())
                n_count = len(list(word_count.keys()))
                sum_count = sum(word_count.values())
                max_count = max(word_count.values())
                avg_count = sum_count / n_count
                if max_count > 20 or avg_count > 2:
                    r = "User word count: " + str(word_count) + os.linesep \
                        + "User word count max: " + str(max_count) + " avg: " + str(avg_count)
                    logger.info(r)
                    block_follower = True
                    reasons.append(str(r))

                if not block_follower:
                    tweet_topics = Topics.get_topics(tweets_text)
                    if tweet_topics:
                        logger.info("User tweet topics: " + str(tweet_topics))
                        block_follower = tweet_topics.spam()
                        reasons.append(str(tweet_topics))
    return block_follower, reasons, profile_text, tweets_text


def _block_user(identity, user, reasons, text1, text2):
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
    identity.twitter.send(twitterpibot.outgoing.OutgoingDirectMessage.OutgoingDirectMessage(text=txt))
    identity.lists.add_user(list_name="Blocked Users", user_id=user.id, screen_name=user.screen_name)
    identity.twitter.block_user(identity, user.id, user.screen_name)


def check_user(identity, user):
    block, reasons, text1, text2 = _is_user_bot(identity, user)
    if block:
        _block_user(identity, user, reasons, text1, text2)
