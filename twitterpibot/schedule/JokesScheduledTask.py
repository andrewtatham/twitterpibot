import random

from apscheduler.triggers.interval import IntervalTrigger
import pyjokes

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet


class JokesScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=2, minutes=random.randint(0, 59))

    def on_run(self):
        text = pyjokes.get_joke()
        self.identity.twitter.send(OutgoingTweet(text=text))
