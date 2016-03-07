from itertools import cycle
import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask

from twitterpibot.logic.zen import zen_of_python

mantra = cycle(zen_of_python)


class ZenOfPythonScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(hours=2, minutes=random.randint(0, 59))

    def on_run(self):
        self.identity.twitter.send(OutgoingTweet(text=next(mantra) + " #ZenOfPython"))
