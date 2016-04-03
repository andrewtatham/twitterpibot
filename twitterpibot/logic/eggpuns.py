import random
import re
import logging

from twitterpibot.logic import wordnikwrapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

trigger_list = ["egg", "eggs", "shell", "chicken", "hen", "omlette", "yolk", "albumen"]

trigger_rx = re.compile("|".join(trigger_list), re.IGNORECASE)

replacements = {
    "eg": "egg",
    "ex": "eggs",

    "sel": "shell",
    "shel": "shell",
    "hell": "shell",
    "shall": "shell",

    "of": "oeuf",
    "ofs": "oeufs",

    "album": "albumen",

    "folk": "yolk",
    "joke": "yolk",
    "jok": "yolk",

    # sketchy
    "ag": "egg",
    "ig": "egg",
    "og": "egg",
    "ug": "egg",
    "ek": "egg"
}

stem_rxs = {
    # "eg": "eg[^g]",  # match eg but not egg
    # "shel": "shel[^l]",  # match shelf but not shell
    # "hell": "[^s]hell",  # match hello but not shell
}


def get_stem_rx(k):
    if k in stem_rxs:
        return stem_rxs[k]
    else:
        return k


stem_list = list(map(lambda key: key, replacements))
stem_rx = re.compile("|".join(map(lambda k: get_stem_rx(k), stem_list)), re.IGNORECASE)


def is_egg_pun_trigger(text):
    match = trigger_rx.match(text)
    return bool(match)


def get_gif_search_text():
    return random.choice(trigger_list)


def make_egg_pun(text):
    logger.info(text)
    matches = stem_rx.findall(text)
    if matches:
        logger.debug("matches: {}".format(matches))
        unique_matches = set(matches)
        for match in unique_matches:
            key = match.lower()
            logger.debug("replacing {} with {}".format(match, replacements[key].upper()))
            text = re.sub(pattern=match, repl=replacements[key].upper(), string=text, flags=re.IGNORECASE)
            logger.debug("text: {}".format(text))
        return text
    return None


def make_egg_pun_phrase(phrase=None):
    if not phrase:
        stem = random.choice(stem_list)
        logger.debug("stem: %s" % stem)
        word = wordnikwrapper.get_word_matching(stem, None)  # stem_rx)
        logger.debug("word: %s" % word)
        phrase = wordnikwrapper.get_example(word)
    logger.debug("phrase: %s" % phrase)
    pun = make_egg_pun(phrase)
    logger.debug("pun: %s" % pun)
    return pun


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info(stem_rx)
    logger.info(replacements)
    phrases = [
        "there was an explosion",
        "very selfish",
        "hello what shall i ",
        "dalek",
        "six of these",
        "Egypt",
        "aggregate",
        "enough",
        "ignite",
        "it was a funny joke",
        "they were joking around",
        "listening to folk music",
        "self-aware",
        "eggregious",

    ]

    for phrase in phrases:
        logger.info("%s -> %s" % (phrase, make_egg_pun_phrase(phrase)))

    for i in range(20):
        logger.info(make_egg_pun_phrase())
