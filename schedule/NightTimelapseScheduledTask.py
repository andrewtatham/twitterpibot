from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
import datetime
class NightTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour = 18, minute = 1) 

    def onRun(args):


        astral = MyAstral()
        today = astral.GetTimes()
        tommorrow = astral.GetTommorrowTimes()

        timelapse = Timelapse(context = args.context, 
            name = 'night',
            startTime = today['sunset'], 
            endTime = tommorrow['sunrise'],
            intervalSeconds = 600,
            tweetText = "The cosmic ballet goes on...")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            args.context.scheduler.add(task)


