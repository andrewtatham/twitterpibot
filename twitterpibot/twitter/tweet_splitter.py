import logging

import textwrap
from twitterpibot.logic import urlhelper
from twitterpibot.outgoing.OutgoingSplitTweet import OutgoingSplitTweet

logger = logging.getLogger(__name__)


def _cap(s, l):
    return s if len(s) <= l else s[0:l - 3] + '...'


def _split_text(large_text, link_count=0, image_count=0,
                characters_reserved_per_media=23, short_url_length_https=23):
    if link_count == 0 and image_count == 0 and len(large_text) <= 140:
        return [large_text]
    else:
        wrap_at = 140
        wrap_at -= image_count * characters_reserved_per_media
        wrap_at -= link_count * short_url_length_https
        logger.info("wrap at %s" % wrap_at)
        lines = textwrap.wrap(large_text, wrap_at)
        lines_count = len(lines)
        line_number = 0
        return_value = []
        for line in lines:
            is_continuation = lines_count > 1 and line_number != 0
            has_continuation = lines_count > 1 and line_number != lines_count - 1
            text = ""
            if is_continuation:
                text += "..."
            text += line
            if has_continuation:
                text += "..."
            return_value.append(text)
            line_number += 1
        return return_value


def split_tweet(outbox_item, twitter_configuration, media_ids):
    split_tweets = []

    media_count = 0
    if media_ids:
        media_count = len(media_ids)

    link_count = urlhelper.count_urls(outbox_item.status)

    statuses = _split_text(
        _cap(outbox_item.status, 140 * 100),
        link_count=link_count,
        image_count=media_count,
        characters_reserved_per_media=twitter_configuration["characters_reserved_per_media"],
        short_url_length_https=twitter_configuration["short_url_length_https"])

    line_number = 0
    for status in statuses:
        logger.info("status %s: %s chars: %s", line_number, len(status), status)

        tweet = OutgoingSplitTweet()
        tweet.status = status
        tweet.location = outbox_item.location
        if line_number == 0:
            if media_ids:
                tweet.media_ids = media_ids

        split_tweets.append(tweet)
        line_number += 1

    return split_tweets
