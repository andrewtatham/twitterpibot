import logging
import random

import cities_and_towns
from phrase_generator import phrase_wrap_list, generate_phrase

logger = logging.getLogger(__name__)


def get_place():
    return random.choice(cities_and_towns.cities)


def get_car():
    return generate_phrase("a (black|white|silver) (bmw|audi|mercedes|van|4x4)")


def get_accident():
    return generate_phrase([
        "collided with",
        "made a (close|punishment) pass"
    ])


def get_target():
    return generate_phrase(["(cyclist|pedestrian|bus stop|tree)"])


def get_deaths():
    return generate_phrase([
        "nobody was hurt",
        "minor injuries were sustained",
        "(one|1) person was (injured|killed)",
        "(two|2) people were (injured|killed)",
    ])


def get_excuse():
    return generate_phrase([
        "sorry mate I didn't see you",
        "they don't even pay road tax",
        "(he|she) wasn't even wearing (a helmet|high-viz)",
        "I was making an important phone call",
        "they wern't using the cycle lane",
        "they were in the middle of the road"

    ])


def get():
    return "{} {} with a{} in {}. {}. the driver said \"{}\"".format(


        get_car(),
        get_accident(),
        get_target(),
        get_place(),
        get_deaths(),
        get_excuse())


if __name__ == '__main__':
    for _ in range(4):
        print(get())
