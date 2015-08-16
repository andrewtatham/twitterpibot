from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
class WeatherScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=7)
    
    def onRun(args):
        
        

        texts = [
            "@BBCWeatherBot Leeds Today"
    
        ]

        text = random.choice()
        
        args.context.outbox.put(OutgoingTweet(text=text))