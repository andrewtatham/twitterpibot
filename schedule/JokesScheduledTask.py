import pyjokes
from ScheduledTask import ScheduledTask
from OutgoingTweet import OutgoingTweet
from apscheduler.triggers.cron import CronTrigger

class JokesScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour = "*/2")

    def onRun(args):
        text = pyjokes.get_joke()
        Send(OutgoingTweet(text = text))


    




