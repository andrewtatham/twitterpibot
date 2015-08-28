from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
import random
from OutgoingTweet import OutgoingTweet
class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=7)
    
    def onRun(args):      
        args.context.outbox.put(OutgoingTweet(text= "@BBCWeatherBot Leeds Today"))