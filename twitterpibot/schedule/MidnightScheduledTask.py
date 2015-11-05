from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.Statistics import GetStatistics, Reset
from twitterpibot.twitter.TwitterHelper import send


class MidnightScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=0)

    def onRun(self):
        stats = GetStatistics()
        send(OutgoingDirectMessage(text=stats))
        Reset()
