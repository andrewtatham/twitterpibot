import pyjokes
from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from OutgoingTweet import OutgoingTweet

class JokesScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return IntervalTrigger(minutes = 2)

    def onRun(args):
        text = pyjokes.get_joke() + "#pyjokes"
        args.context.outbox.put(OutgoingTweet(text = text))


    




