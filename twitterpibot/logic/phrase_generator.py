import random
import re

__author__ = 'andrewtatham'
_choice_rx = re.compile("\(.*\)")


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
                choices = match[1:-1].split("|")
                choice = random.choice(choices)
                response = response.replace(match, choice)

        text += " " + response
        return text