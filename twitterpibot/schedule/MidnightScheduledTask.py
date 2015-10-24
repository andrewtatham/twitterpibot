from apscheduler.triggers.cron import CronTrigger

from ScheduledTask import ScheduledTask
from twitterpibot.outgoing.OutgoingDirectMessage import OutgoingDirectMessage
from twitterpibot.Statistics import GetStatistics, Reset
from twitterpibot.twitter.TwitterHelper import Send


class MidnightScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=0)

    def onRun(self):
        stats = GetStatistics()
        tweet = OutgoingDirectMessage(
            text=stats,
            screen_name="andrewtatham",
            user_id="19201332")
        Send(tweet)
        Reset()
