import logging
import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import eggpuns, imagemanager, fsh
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class EggPunScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        file_paths = None
        try:
            pun = eggpuns.make_egg_pun_phrase()
            text = eggpuns.get_gif_search_text()
            gif = imagemanager.get_gif(screen_name=self.identity.screen_name, text=text)
            if gif:
                file_paths = [gif]

            self.identity.twitter.send(OutgoingTweet(text=pun, file_paths=file_paths))
        finally:
            fsh.delete_files(file_paths)

if __name__ == '__main__':
    import identities_pis

    logging.basicConfig(level=logging.INFO)
    identity = identities_pis.EggPunBotIdentity(None)
    task = EggPunScheduledTask(identity)
    task.on_run()
