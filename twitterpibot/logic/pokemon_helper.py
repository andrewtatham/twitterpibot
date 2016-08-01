import logging
import os
import pprint
import random

from twitterpibot.logic import urlhelper

logger = logging.getLogger(__name__)

base_url = "http://pokeapi.co/api/v2/"
pokemons = {}
pokemon_details = {}


class Pokemon(object):
    def __init__(self, data):
        logger.debug(pprint.pformat(data))
        self.name = data["name"]
        self.height = data["height"]
        self.weight = data["weight"]
        # todo calc BMI
        self.type = "/".join([slot["type"]["name"] for slot in data["types"]])
        self.sprites = self._get_sprites(data=data["sprites"])
        self.abilities = self._get_abilities(data=data["abilities"])
        self.moves = self._get_moves(data=data["moves"])
        self.stats = self._get_stats(data=data["stats"])

        self.species = self._get_species(url=data["species"]["url"])

    def __str__(self):

        return "{name} {type} {species.desc}".format(**self.__dict__)

    @staticmethod
    def _get_species(url):
        response = urlhelper.get_response(url)
        species = Species(response)
        return species

    @staticmethod
    def _get_sprites(data):
        keys = ["front_default"]
        sprites = []
        for key in keys:
            sprite = data.get(key)
            if sprite:
                sprites.append(sprite)
        return sprites

    @staticmethod
    def _get_abilities(data):
        return list(map(lambda a: a["ability"]["name"], data))

    @staticmethod
    def _get_moves(data):
        return list(map(lambda m: m["move"]["name"], data))

    @staticmethod
    def _get_stats(data):
        return dict(map(lambda s: (s["stat"]["name"], s["base_stat"]), data))




def _get_name(data, language):
    return list(filter(lambda n: n["language"]["name"] == language, data["names"]))[0]["name"]


class Species(object):
    def __init__(self, data):
        logger.debug(pprint.pformat(data))
        self.name = data["name"]
        self.name_en = _get_name(data, "en")
        self.name_jp = _get_name(data, "ja")

        english = filter(lambda ft: ft["language"]["name"] == "en", data["flavor_text_entries"])
        kvp = list(map(lambda ft: ft["flavor_text"].replace(os.linesep, " "), english))
        kvp.sort(key=len, reverse=True)
        self.desc = kvp[0]

        # self.variety_default = list(filter(lambda v: v["is_default"], data["varieties"]))[0]["pokemon"]["name"]
        # self.variety_others = list(map(lambda v: v["name"], filter(lambda v: not v["is_default"], data["varieties"])))

        self.capture_rate = data["capture_rate"]

        self.has_gender_differences = data["has_gender_differences"]

        self.habitat = data["habitat"]

        self.shape = data["shape"]["name"]



def _get_all_pokemons():
    global pokemons
    if not pokemons:
        url = base_url + "pokemon/"
        params = {
            "limit": 1000
        }
        request_url = urlhelper.parameterise(params, url)
        response = urlhelper.get_response(request_url)
        pokemons = dict([(result["name"], result["url"]) for result in response["results"]])
    return pokemons


def _get_pokemon_details(id_or_name):
    if not id_or_name in pokemon_details:
        url = pokemons[id_or_name]
        response = urlhelper.get_response(url)
        pokemon_details[id_or_name] = Pokemon(response)

    return pokemon_details[id_or_name]


def _get_all_names():
    names = _get_all_pokemons()
    return names


def get_random_pokemon_details():
    all_names = _get_all_names()

    name = random.choice(all_names)

    details = _get_pokemon_details(name)

    return details


if __name__ == '__main__':

    logging.basicConfig(level=logging.INFO)
    for _ in range(3):
        print(str(get_random_pokemon_details()))
