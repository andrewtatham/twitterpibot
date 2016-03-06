from apscheduler.triggers.interval import IntervalTrigger

import twitterpibot.logic.GiphyWrapper
import twitterpibot.logic.eggpuns

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class EggPunScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=2)

    def on_run(self):
        pun = twitterpibot.logic.eggpuns.make_egg_pun_phrase()

        file_paths = [twitterpibot.logic.GiphyWrapper.get_gif("egg")]
        self.identity.twitter.send(OutgoingTweet(
            text=pun,
            file_paths=file_paths))
