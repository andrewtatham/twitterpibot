from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
import datetime
class SunTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour = 3, minute = 1) 

    def onRun(args):

        sun = MyAstral().GetTimes()

        timelapse = Timelapse(context = args.context, 
            name = 'sun',
            startTime = sun['dawn'], 
            endTime = sun['dusk'],
            intervalSeconds = 600,
            tweetText = "The cosmic ballet goes on...")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            args.context.scheduler.add(task)


