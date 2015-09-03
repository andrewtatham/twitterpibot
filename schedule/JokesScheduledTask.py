import pyjokes
from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from OutgoingTweet import OutgoingTweet

class JokesScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return IntervalTrigger(hours = 1)

    def onRun(args):
        text = pyjokes.get_joke()
        args.context.outbox.put(OutgoingTweet(text = text))


    




