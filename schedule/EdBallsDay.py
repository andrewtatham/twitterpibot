
from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet

import datetime

class EdBallsDay(ScheduledTask):

    def GetTrigger(args):
        return CronTrigger(month = 4, day = 28, hour = 16, minute = 20)
 
    def onRun(args):
        year = str(datetime.date.today().year)
        text = "@edballs ED BALLS #EdBallsDay #EdBallsDay" + year
        tweet = OutgoingTweet(text=text)
        Send(tweet)