import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import eggpuns, giphyhelper
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class EggPunScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=random.randint(3, 6), minutes=random.randint(0, 59))

    def on_run(self):
        pun = eggpuns.make_egg_pun_phrase()
        text = eggpuns.get_gif_search_text()
        gif = giphyhelper.get_gif(screen_name=self.identity.screen_name, text=text)
        file_paths = None
        if gif:
            file_paths = [gif]
        self.identity.twitter.send(OutgoingTweet(text=pun, file_paths=file_paths))


if __name__ == '__main__':
    import main

    identity = main.EggPunBotIdentity(None)
    task = EggPunScheduledTask(identity)
    task.on_run()
