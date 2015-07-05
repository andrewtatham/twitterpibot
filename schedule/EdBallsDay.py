from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime

class EdBallsDay(ScheduledTask):


    def GetTrigger(args):


        

        #return CronTrigger(second = datetime.datetime.now().second + 15)

        # 28th April 4:20 pm
        return CronTrigger(month = 4, day = 28, hour = 16, minute = 20)
    

    def onRun(args):
        year = str(datetime.date.today().year)

        #text = "@andrewtatham TEST #" + year
        text = "@edballs ED BALLS #EdBallsDay #EdBallsDay" + year

        tweet = OutgoingTweet(text=text)
        args.context.outbox.put(tweet)