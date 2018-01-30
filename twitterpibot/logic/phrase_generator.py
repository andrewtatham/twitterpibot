import random
import re

import logging

logger = logging.getLogger(__name__)

__author__ = 'andrewtatham'
_choice_rx = re.compile("\(.*?\)")


def generate_phrase(response, text=""):
    if isinstance(response, list):
        return generate_phrase(random.choice(response), text)
    elif isinstance(response, dict):
        key = random.choice(response)
        text += " " + key
        return generate_phrase(random.choice(response[key]), text)
    else:
        # string
        matches = _choice_rx.findall(response)
        if matches:

            for match in matches:
                logger.debug(match)
                choices = match[1:-1].split("|")
                logger.debug(choices)
                choice = random.choice(choices)
                logger.debug(choice)
                response = response.replace(match, choice)
                logger.debug(response)
            text += " " + response
        else:
            return response

        return text


def phrase_wrap_list(word_list):
    return "({})".format("|".join(word_list))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    blah = "{}{}".format(phrase_wrap_list(["a", "b", "c"]),
                         phrase_wrap_list(["1", "2", "3"]))
    logger.info(blah)
    for _ in range(1):
        logger.info(generate_phrase(blah))
