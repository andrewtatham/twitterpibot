import logging
import pprint
import re

from twitterpibot.logic import fsh
from twitterpibot.text import textfilehelper


def sorter(w):
    l = levels.get(w.lower())
    if l is None:
        return None
    else:
        return l


logger = logging.getLogger(__name__)

rx = re.compile("[\w\-']+")

path = fsh.root + "google-10000-english/20k.txt"
all_words = textfilehelper.get_text(path=path)
level = 1
levels = {}
for word in all_words:
    levels[word.lower()] = level
    level += 1


def get_common_words(text):
    words = rx.findall(text)
    words = list(map(lambda w: (w, sorter(w)), words))
    logger.debug("words = {}".format(words))

    common_words = list(filter(lambda w: w[1], words))
    uncommon_words = list(filter(lambda w: not w[1], words))

    common_words.sort(key=lambda w: w[1])
    common_words.reverse()

    uncommon_words.sort(key=lambda w: len(w[0]))
    uncommon_words.reverse()

    logger.debug("common_words = {}".format(common_words))
    logger.debug("uncommon_words = {}".format(uncommon_words))

    common_words = list(map(lambda w: w[0], common_words))
    uncommon_words = list(map(lambda w: w[0], uncommon_words))

    return {
        "common": common_words,
        "uncommon": uncommon_words
    }


if __name__ == '__main__':

    import identities

    identity = identities.AndrewTathamPiIdentity(None)
    tweets = identity.twitter.get_user_timeline()
    logging.basicConfig(level=logging.DEBUG)
    for tweet in tweets:
        tweet_text = tweet["text"]
        logger.info(tweet_text)
        analysis = get_common_words(tweet_text)
        logger.info(pprint.pformat(analysis))
