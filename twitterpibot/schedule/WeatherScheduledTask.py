from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
import random
from OutgoingTweet import OutgoingTweet
from TwitterHelper import Send
class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=7)
    
    def onRun(self):
        Send(OutgoingTweet(text= "@BBCWeatherBot Leeds Today"))