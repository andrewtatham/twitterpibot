from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import random
from OutgoingTweet import OutgoingTweet
class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=7)
    
    def onRun(args):      
        args.context.send(OutgoingTweet(text= "@BBCWeatherBot Leeds Today"))