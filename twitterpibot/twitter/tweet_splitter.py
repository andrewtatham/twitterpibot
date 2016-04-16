import logging

import textwrap
from twitterpibot.logic import urlhelper
from twitterpibot.outgoing.OutgoingSplitTweet import OutgoingSplitTweet
from ttp import ttp, utils

logger = logging.getLogger(__name__)

twitter_parser = ttp.Parser()


def _cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


def split_tweet(outbox_item, twitter_configuration):
    max_tweet_length = 140
    len_media = twitter_configuration["characters_reserved_per_media"]
    len_url = twitter_configuration["short_url_length_https"]

    parse_result = twitter_parser.parse(outbox_item.status)

    total_chars = len(outbox_item.status) \
                  + len(outbox_item.media_ids) * len_media
                  # + len(parse_result.urls) * len_url # todo count urls properly, not twice
    number_of_tweets = total_chars / max_tweet_length
    print(number_of_tweets)
    words = outbox_item.status.split()
    words.reverse()

    medias = outbox_item.media_ids
    medias.reverse()

    tweet_number = 0
    tweets = []
    while words or medias:

        tweet = OutgoingSplitTweet()
        tweet.location = outbox_item.location

        _add_media(tweet, tweet_number, number_of_tweets, medias)

        _add_words(tweet, len_media, len_url, max_tweet_length, parse_result, words)

        tweets.append(tweet)
        tweet_number += 1

    return tweets


def _add_words(tweet, len_media, len_url, max_tweet_length, parse_result, words):
    can_add_word = bool(words)
    while can_add_word:

        if words:
            word = words.pop()
        else:
            word = None
        if words:
            next_word = words[0]
        else:
            next_word = None

        if tweet.status:
            tweet.status += " "
        tweet.status += word

        if next_word:
            if next_word in parse_result.urls:
                next_word_chars = len_url
            else:
                next_word_chars = len(next_word)

            if tweet.media_ids:
                media_chars = len(tweet.media_ids) * len_media
            else:
                media_chars = 0

            can_add_word = len(tweet.status) + media_chars + next_word_chars < max_tweet_length
        else:
            can_add_word = False


def _add_media(tweet, tweet_number, number_of_tweets, medias):
    if medias:
        if medias and len(tweet.media_ids) < 4:
            tweet.media_ids.append(medias.pop())
        # add extra medias if not enough tweets remaining
        while medias and (number_of_tweets - tweet_number) < len(medias) and len(tweet.media_ids) < 4:
            tweet.media_ids.append(medias.pop())
