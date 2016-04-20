import logging
import math

from ttp import ttp

from twitterpibot.outgoing.OutgoingSplitTweet import OutgoingSplitTweet

logger = logging.getLogger(__name__)

twitter_parser = ttp.Parser()


def _cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


def _add_quote(tweet, tweet_number, quote_url):
    if tweet_number == 0 and quote_url:
        tweet.status += quote_url


def split_tweet(outbox_item, twitter_configuration):
    max_tweet_length = 140
    len_media = twitter_configuration["characters_reserved_per_media"]
    len_url = twitter_configuration["short_url_length_https"]

    parse_result = twitter_parser.parse(outbox_item.status)

    mentions_string = ""
    if outbox_item.mentions:
        mentions_string = ".@" + " @".join(outbox_item.mentions)

    # todo count in-status urls properly
    number_of_tweets = 1
    for _ in range(5):
        total_chars = len(mentions_string) * number_of_tweets \
                      + len(outbox_item.status) \
                      + len(outbox_item.media_ids) * len_media \
                      + len(outbox_item.urls) * len_url \
                      + int(bool(outbox_item.quote_url)) * len_url * number_of_tweets

        number_of_tweets = int(math.ceil(total_chars / max_tweet_length))
        print(number_of_tweets)

    words = outbox_item.status.split()
    words.reverse()

    medias = outbox_item.media_ids
    medias.reverse()

    urls = outbox_item.urls
    urls.reverse()

    tweet_number = 0
    tweets = []
    while words or medias or urls:
        tweet = OutgoingSplitTweet()
        tweet.location = outbox_item.location

        if outbox_item.mentions:
            tweet.status += ".@" + " @".join(outbox_item.mentions)

        _add_media(tweet, tweet_number, number_of_tweets, medias)

        _add_words(tweet, tweet_number, len_media, len_url, max_tweet_length, parse_result, words,
                   outbox_item.quote_url, urls)

        tweets.append(tweet)
        tweet_number += 1

    return tweets


def _add_words(tweet, tweet_number, len_media, len_url, max_tweet_length, parse_result, words, quote_url, urls):
    can_add_word = bool(words)
    can_add_url = bool(urls)
    while can_add_word or can_add_url:

        if words:
            word = words.pop()
        else:
            word = None
        if words:
            next_word = words[0]
        else:
            next_word = None

        if can_add_word:
            if tweet.status:
                tweet.status += " "
            tweet.status += word

        # reserve space for media ids
        media_chars = int(bool(tweet.media_ids)) * len(tweet.media_ids) * len_media
        # reserve space for quote url
        len_quote_url = int(bool(quote_url)) * (1 + len_url)

        len_status = len(tweet.status) + media_chars + len_quote_url

        if next_word:
            if next_word in parse_result.urls:
                next_word_chars = 1 + len_url
            else:
                next_word_chars = len(" " + next_word)
            can_add_word = len_status + next_word_chars < max_tweet_length
        else:
            can_add_word = False

        can_add_url = urls and len_status + (1 + len_url) < max_tweet_length

        # add urls after all words
        if not can_add_word and urls and can_add_url:
            if tweet.status: tweet.status += " "
            tweet.status += urls.pop()


        # add quote url to end of first tweet
        if not can_add_word and not can_add_url and quote_url:
            if tweet.status: tweet.status += " "
            tweet.status += quote_url


def _add_media(tweet, tweet_number, number_of_tweets, medias):
    if medias:
        if medias and len(tweet.media_ids) < 4:
            tweet.media_ids.append(medias.pop())
        # add extra medias if not enough tweets remaining
        while medias and (number_of_tweets - tweet_number - 1) < len(medias) and len(tweet.media_ids) < 4:
            tweet.media_ids.append(medias.pop())
