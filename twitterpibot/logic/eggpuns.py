import random

from twitterpibot.logic import wordnikwrapper

puns = wordnikwrapper.get_egg_puns()
print(puns)


def get_egg_pun():
    pun = random.choice(puns)
    print(pun)
    return pun
