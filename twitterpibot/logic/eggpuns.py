import random
import re
import logging

# from twitterpibot.logic import wordnikwrapper

logger = logging.getLogger(__name__)

replacements = {
    "eg": "egg",
    "ex": "eggs",
    "ec": "egg",

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

    "i'm a lit": "omlette",
    "i'm lit": "omlette",

    "over":"ovum",

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
    match = stem_rx.findall(text)
    return bool(match)


trigger_list = ["egg", "eggs", "egged", "egging", "egg shell", "chicken", "hen", "omlette", "yolk", "albumen"]


def get_gif_search_text():
    return random.choice(trigger_list)


def make_egg_pun(text, mask=None):
    if mask:
        matches = stem_rx.finditer(mask)
        if matches:
            matches = list(matches)
            matches.sort(key=lambda m: m.start())
            matches.reverse()
            for match in matches:
                key = match.group().lower()
                indices = (match.start(), match.end())
                logger.debug("matched key {} at {}".format(key, indices))
                logger.debug("text before: '{}'".format(text[:indices[0]]))
                logger.debug("text after: '{}'".format(text[indices[1]:]))

                text = text[:indices[0]] + replacements[key].upper() + text[indices[1]:]
                text = "".join(text)
            return text
    else:
        matches = stem_rx.findall(text)
        if matches:
            # logger.debug("matches: {}".format(matches))
            unique_matches = set(matches)
            for match in unique_matches:
                key = match.lower()
                logger.debug("replacing {} with {}".format(match, replacements[key].upper()))
                text = re.sub(pattern=match, repl=replacements[key].upper(), string=text, flags=re.IGNORECASE)
                logger.debug("text: {}".format(text))
            return text
    return None


def make_egg_pun_phrase(phrase, mask=None):
    # if not phrase:
    #     stem = random.choice(stem_list)
    #     logger.debug("stem: %s" % stem)
    #     word = wordnikwrapper.get_word_matching(stem, None)  # stem_rx)
    #     logger.debug("word: %s" % word)
    #     phrase = wordnikwrapper.get_example(word)
    logger.debug("phrase: %s" % phrase)
    logger.debug("mask: %s" % str(mask))
    pun = make_egg_pun(phrase, mask)
    logger.debug("pun: %s" % pun)
    return pun
