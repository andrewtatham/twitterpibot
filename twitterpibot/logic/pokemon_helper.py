import os
import pprint
import random

from twitterpibot.logic import urlhelper

base_url = "http://pokeapi.co/api/v2/"
pokemons = {}
pokemon_details = {}

_species = {}
_species_details = {}


class Pokemon(object):
    def __init__(self, data):
        self._data = data
        pprint.pprint(self._data)
        self._data["type"] = "/".join([slot["type"]["name"] for slot in self._data["types"]])

    def __str__(self):
        # return pprint.pformat(self._data)

        return "{id} {name} {type} {weight}".format(**self._data)


class Species(object):
    def __init__(self, data):
        self._data = data
        pprint.pprint(self._data)
        self.name = self._data["name"]

        self.name_en = list(filter(lambda n: n["language"]["name"] == "en", self._data["names"]))[0]["name"]
        self.name_jp = list(filter(lambda n: n["language"]["name"] == "ja", self._data["names"]))[0]["name"]

        english = filter(lambda ft: ft["language"]["name"] == "en", self._data["flavor_text_entries"])
        kvp = list(map(lambda ft: ft["flavor_text"].replace(os.linesep, " "), english))
        kvp.sort(key=len, reverse=True)
        self.desc = kvp[0]

        self.variety_default = list(filter(lambda v: v["is_default"], self._data["varieties"]))[0]["pokemon"]["name"]

        self.sprites = self.get_sprites(self._data["sprites"])

    def __str__(self):
        return "{name_en} {name_jp} {desc}".format(**self.__dict__)

    def get_sprites(self, data):
        keys = ["front_default"]
        sprites = []
        for key in keys:
            sprite = data.get(key)
            if sprite:
                sprites.append(sprite)
        return sprites


def get_all_pokemons():
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


def get_pokemon_details(id_or_name):
    if not id_or_name in pokemon_details:
        if id_or_name in pokemons:
            url = pokemons[id_or_name]
        else:
            url = base_url + "pokemon/{}/".format(id_or_name)
        response = urlhelper.get_response(url)
        pokemon_details[id_or_name] = Pokemon(response)

    return pokemon_details[id_or_name]


def get_all_species():
    global _species
    if not _species:
        url = base_url + "pokemon-species/"
        params = {
            "limit": 1000
        }
        request_url = urlhelper.parameterise(params, url)
        response = urlhelper.get_response(request_url)
        _species = dict([(result["name"], result["url"]) for result in response["results"]])
    return _species


def get_species_details(id_or_name):
    if not id_or_name in _species_details:
        if id_or_name in _species:
            url = _species[id_or_name]
        else:
            url = base_url + "pokemon-species/{}/".format(id_or_name)
        response = urlhelper.get_response(url)
        _species_details[id_or_name] = Species(response)

    return _species_details[id_or_name]


def get_all_names():
    names = get_all_pokemons()
    return names


def get_random_pokemon_details():
    names = get_all_names()
    name = random.choice(names)
    details = get_pokemon_details(name)
    return details


if __name__ == '__main__':
    species_names = get_all_species()
    for _ in range(1):
        species_name = random.choice(species_names)
        species_details = get_species_details(species_name)
        print(species_details)

        pokemon_details = get_pokemon_details(species_details.variety_default)
        print(pokemon_details)
