from itertools import cycle

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.outgoing.OutgoingTweet import OutgoingTweet
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.twitter.TwitterHelper import send
from twitterpibot.logic.zen import zen_of_python

mantra = cycle(zen_of_python)


class ZenOfPythonScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(hours=13)

    def onRun(self):
        send(OutgoingTweet(text=next(mantra) + " #ZenOfPython"))
