from ScheduledTask import ScheduledTask
import datetime
from apscheduler.triggers.date import DateTrigger
from astral import Astral
from OutgoingTweet import OutgoingTweet
from apscheduler.triggers.cron import CronTrigger

class MidnightScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=0,minute=0)


    def onRun(args):

        astral = Astral()
            
        city = astral['Leeds']

        sun = city.sun(date=datetime.date.today(), local = True)
     
        tasks = []

        tasks.append(AstralScheduledTask(text = "dawn", time = sun['dawn']))
        tasks.append(AstralScheduledTask(text = "sunrise", time = sun['sunrise']))
        tasks.append(AstralScheduledTask(text = "noon", time = sun['noon']))
        tasks.append(AstralScheduledTask(text = "sunset", time = sun['sunset']))
        tasks.append(AstralScheduledTask(text = "dusk", time = sun['dusk']))

        for task in tasks:
            args.context.scheduler.add(task)




class AstralScheduledTask(ScheduledTask):
    def __init__(self, time, text, *args, **kwargs):
        self.text = text                
        self.time = time        
    def GetTrigger(args):
        return DateTrigger(run_date = args.time)
    def onRun(args):        
        args.context.outbox.put(OutgoingTweet(text=args.text))
    