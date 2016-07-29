import logging
import random
from time import sleep

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import pokemon_helper, imagemanager
from twitterpibot.logic.conversation import hello_words
from twitterpibot.logic.phrase_generator import generate_phrase
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

logger = logging.getLogger(__name__)


class PokemonScheduledTask(ScheduledTask):
    def __init__(self, identity, converse_with_identity, armed=True):
        super(PokemonScheduledTask, self).__init__(identity)
        self._converse_with = converse_with_identity
        self._armed = armed

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        pokemon = pokemon_helper.get_random_pokemon_details()

        reply_to = self._found_pokemon(pokemon)

        reply_to = self._tell_me_more(reply_to)

        reply_to = self._description(pokemon, reply_to)

        reply_to = self._tell_me_more(reply_to)

        reply_to = self._details(pokemon, reply_to)

    def _tell_me_more(self, reply_to):
        text = ".@" + self.identity.screen_name + " " + generate_phrase([
            "(Wow|Cool|Nice|Sweet|Awesome), tell me more about it..."
        ])
        logger.info(text)
        if self._armed:
            reply_to = self._converse_with.twitter.send(OutgoingTweet(text=text, in_reply_to_id_str=reply_to))
            sleep(2)
        return reply_to
    
    def _found_pokemon(self, pokemon, reply_to=None):
        text = generate_phrase(
            hello_words) + " @" + self._converse_with.screen_name + " I found a " + pokemon.species.name_en
        logger.info(text)
        if self._armed:
            images = imagemanager.download_images(pokemon.sprites)
            reply_to = self.identity.twitter.send(OutgoingTweet(text=text, file_paths=images))
            sleep(2)
        return reply_to

    def _details(self, pokemon, reply_to):

        texts = [
            "{} is a {} type".format(pokemon.species.name_en, pokemon.type),
            "{} is known as {} in Japan".format(pokemon.species.name_en, pokemon.species.name_jp),
            "{} has a height of {}".format(pokemon.species.name_en, pokemon.height),
            "{} has a weight of {}".format(pokemon.species.name_en, pokemon.weight),
        ]

        texts.extend(self._subset(pokemon.species.name_en, pokemon.moves, "moves", 10))
        texts.extend(self._subset(pokemon.species.name_en, pokemon.abilities, "abilities", 5))

        # for name, stat in pokemon.stats.items():
        #     texts.append("{} has a {} of {}".format(pokemon.species.name_en, name, stat))

        random.shuffle(texts)
        for text in texts:
            text = ".@" + self._converse_with.screen_name + " " + text
            logger.info(text)
            if self._armed:
                reply_to = self.identity.twitter.send(OutgoingTweet(text=text, in_reply_to_id_str=reply_to))
                sleep(2)
        return reply_to

    def _subset(self, pokemon_name, pokemon_list, list_type, n):
        texts = []
        if len(pokemon_list) >= n:
            pokemon_list_subset = random.sample(pokemon_list, n)
            texts.append("{} {} include {}".format(pokemon_name, list_type, ", ".join(pokemon_list_subset)))
        else:
            texts.append("{} {} are {}".format(pokemon_name, list_type, ", ".join(pokemon_list)))
        return texts

    def _description(self, pokemon, reply_to):
        text = ".@" + self._converse_with.screen_name + " " + pokemon.species.desc
        logger.info(text)
        if self._armed:
            reply_to = self.identity.twitter.send(OutgoingTweet(text=text, in_reply_to_id_str=reply_to))
            sleep(2)
        return reply_to


if __name__ == '__main__':
    import identities

    logging.basicConfig(level=logging.INFO)

    converse_with_identity = identities.AndrewTathamPiIdentity()
    identity = identities.AndrewTathamPi2Identity(converse_with_identity)

    task = PokemonScheduledTask(identity=identity, converse_with_identity=converse_with_identity, armed=False)
    task.on_run()
