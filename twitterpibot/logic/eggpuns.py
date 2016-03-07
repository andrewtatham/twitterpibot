import random
import re
import logging

from twitterpibot.logic import wordnikwrapper

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

trigger_list = ["egg", "eggs," "egg shell", "chicken", "hen", "omlette", "yolk"]

trigger_rx = re.compile("|".join(trigger_list), re.IGNORECASE)

replacements = {
    "eg": "egg",
    "ex": "eggs",

    "shel": "shell",
    "sel": "shell",
    "hell": "shell",
    "shall": "shell",

    # sketchy
    "ag": "egg",
    "ig": "egg",
    "og": "egg",
    "ug": "egg",

}

stem_rxs = {
    "eg": "eg[^g]",  # match eg but not egg
    "shel": "shel[^l]",  # match shelf but not shell
    "hell": "[^s]hell",  # match hello but not shell
}


def get_stem_rx(k):
    if k in stem_rxs:
        return stem_rxs[k]
    else:
        return k


stem_list = list(replacements)
stem_rx = re.compile("|".join(map(lambda k: get_stem_rx(k), stem_list)), re.IGNORECASE)


def is_egg_pun_trigger(text):
    match = trigger_rx.match(text)
    return bool(match)


def make_egg_pun(text):
    matches = stem_rx.findall(text)
    if matches:
        for k, v in replacements.items():
            text = re.sub(k, v.upper(), text)
        return text
    return None


def make_egg_pun_phrase(phrase=None):
    if not phrase:
        stem = random.choice(stem_list)
        logger.debug("stem: %s" % stem)
        word = wordnikwrapper.get_word_matching(stem, stem_rx)
        logger.debug("word: %s" % word)
        phrase = wordnikwrapper.get_example(word)
    logger.debug("phrase: %s" % phrase)
    pun = make_egg_pun(phrase)
    logger.debug("pun: %s" % pun)
    return pun


if __name__ == "__main__":
    phrases = [
        "there was an explosion",
        "very selfish",
        "what shall i "
    ]
    for phrase in phrases:
        print(make_egg_pun_phrase(phrase))

    for i in range(3):
        print(make_egg_pun_phrase())


def get_gif_search_text():
    return random.choice(trigger_list)
