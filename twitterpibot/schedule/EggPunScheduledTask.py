from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.logic import eggpuns, giphyhelper
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class EggPunScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=17)

    def on_run(self):
        pun = eggpuns.make_egg_pun_phrase()
        text = eggpuns.get_gif_search_text()
        gif = giphyhelper.get_gif(screen_name=self.identity.screen_name, text=text)
        file_paths = [gif]
        self.identity.twitter.send(OutgoingTweet(text=pun, file_paths=file_paths))
