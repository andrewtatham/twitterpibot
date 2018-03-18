import logging
import random
import re

# from twitterpibot.logic import wordnikwrapper

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class EggPun(object):
    def __init__(self, find_rx, replace_rx, replace_text):
        self.find_rx = find_rx
        self.replace_rx = replace_rx
        self._find_rx = re.compile(find_rx, re.IGNORECASE)
        self._replace_rx = re.compile(replace_rx, re.IGNORECASE)
        self._replace_text = replace_text

    def __str__(self):
        return "found '{}' replacing '{}' with '{}'".format(self.find_rx, self.replace_rx, self._replace_text)

    def find_all(self, mask):
        return self._find_rx.findall(mask)

    def replace_all(self, text, mask):
        matches = list(self._replace_rx.finditer(mask))
        matches.sort(key=lambda m: m.start(), reverse=True)
        for match in matches:
            indices = (match.start(), match.end())
            logger.debug("text before: '{}'".format(text[:indices[0]]))
            logger.debug("text after: '{}'".format(text[indices[1]:]))

            mask = mask[:indices[0]] + self._replace_text.upper() + mask[indices[1]:]
            text = text[:indices[0]] + self._replace_text.upper() + text[indices[1]:]
        return text, mask


replacements = [
    EggPun("eg(\\b|[^g])", "egg?", "egg"),
    EggPun("e[ck]", "e[ck]", "egg"),
    EggPun("[aiou]g", "[aiou]gg?", "egg"),

    EggPun("ex", "ex", "eggs"),

    EggPun("(\\b|[^s])hell", "hell", "shell"),  # add s
    EggPun("shel(\\b|[^l])", "shell?", "shell"),  # add l
    EggPun("sel", "sell?", "shell"),  # add h
    EggPun("shall", "shall", "shell"),  # change a to e

    EggPun("of", "of", "oeuf"),

    EggPun("ofs", "ofs", "oeufs"),

    EggPun("album", "album", "albumen"),

    EggPun("folk", "folk", "yolk"),
    EggPun("joke?", "joke?", "yolk"),

    EggPun("i'm a lit", "i'm a lit", "omlette"),
    EggPun("i'm lit", "i'm lit", "omlette"),
    EggPun("over", "over", "ovum"),
]

trigger_rx = re.compile("|".join(map(lambda r: r.find_rx, replacements)), re.IGNORECASE)


def is_egg_pun_trigger(text):
    match = trigger_rx.findall(text)
    return bool(match)


gif_search_words = ["egg", "eggs", "egged", "egging", "egg shell", "chicken", "hen", "omlette", "yolk", "albumen"]


def get_gif_search_text():
    return random.choice(gif_search_words)


def make_egg_pun(text, mask=None):
    if mask is None:
        mask = text

    matches = []
    for r in replacements:
        r_matches = r.find_all(mask)
        if r_matches:
            matches.append(r)

    if matches:
        logger.debug("text: {}".format(text))
        logger.debug("mask: {}".format(mask))
        for match in matches:
            logger.debug("pun: {}".format(match))
            text, mask = match.replace_all(text, mask)
            logger.debug("text: {}".format(text))
            logger.debug("mask: {}".format(mask))
        return text
    return None


_egg_puns = [
    "Egg-?splosion",
    "Egg-?straordinary",
    "Egg-?straordinarily",
]
_egg_puns_rx = re.compile("|".join(_egg_puns), re.IGNORECASE)


def is_egg_pun(text):
    return bool(_egg_puns_rx.search(text))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    text = "@imagebot explosion http://ex.com #joke"
    mask = "          explosion               #joke"
    pun = make_egg_pun(text, mask)
    print("({}: {}),".format(text, pun))
