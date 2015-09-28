
from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from OutgoingTweet import OutgoingTweet
import datetime
import random

piracy = [
    # TODO Piraty things
] 
class TalkLikeAPirateDayScheduledTask(ScheduledTask):
        
    def GetTrigger(args):
        return CronTrigger(month = 9, day = 19, minute = "*/10")
 
    def onRun(args):
        text = random.choice(piracy) + " #TalkLikeAPirateDay"
        tweet = OutgoingTweet(text=text)
        args.context.outbox.put(tweet)