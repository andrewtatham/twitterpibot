import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import pokemon_helper, imagemanager
from twitterpibot.logic.conversation import hello_words
from twitterpibot.logic.phrase_generator import generate_phrase
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class PokemonScheduledTask(ScheduledTask):
    def __init__(self, identity, converse_with_identity):
        super(PokemonScheduledTask, self).__init__(identity)
        self._converse_with = converse_with_identity

    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        pokemon = pokemon_helper.get_random_pokemon_details()

        text = generate_phrase(hello_words) + " @" + self._converse_with.screen_name + " I found a " + pokemon.name_en
        images = imagemanager.download_images(pokemon.sprites)
        reply_to = self.identity.twitter.send(OutgoingTweet(text=text, file_paths=images))

        text = generate_phrase([
            "(Wow|Cool|Nice|Sweet|Awesome), (tell me more about it)"

        ])
        reply_to = self._converse_with.twitter.send(OutgoingTweet(text=text, reply_to=reply_to))


        text = generate_phrase([
            "It's a {} type.".format(pokemon.type),
            "It's known as a {} in Japan.".format(pokemon.name_jp),
            pokemon.species.desc
        ])
        reply_to = self.identity.twitter.send(OutgoingTweet(text=text,  reply_to=reply_to))
