from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import random
from OutgoingTweet import OutgoingTweet
from TwitterHelper import Send
class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=7)
    
    def onRun(args):      
        Send(OutgoingTweet(text= "@BBCWeatherBot Leeds Today"))