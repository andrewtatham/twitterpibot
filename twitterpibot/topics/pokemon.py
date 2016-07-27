from twitterpibot.logic import pokemon_helper
from twitterpibot.topics.Topic import GoodTopic

definite_matches = [
    "Pokemon", "pokedex",
]
definite_matches.extend(pokemon_helper.get_all_names())


class Pokemon(GoodTopic):
    def __init__(self):
        super(Pokemon, self).__init__(definite_matches)


def get():
    return [
        Pokemon()
    ]
