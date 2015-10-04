
from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
from OutgoingDirectMessage import OutgoingDirectMessage

class MidnightScheduledTask(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(hour = 0)
 
    def onRun(args):

        stats = args.context.statistics.GetStatistics()
        tweet = OutgoingDirectMessage(
            text=stats,
            screen_name = "andrewtatham", 
            user_id = "19201332")
        args.context.send(tweet)
        args.context.statistics.Reset()
