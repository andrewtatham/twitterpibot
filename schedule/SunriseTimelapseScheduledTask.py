from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
import datetime
class SunriseTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour = 3,minute = 0)

    def onRun(args):

        sun = MyAstral().GetTimes()

        timelapse = Timelapse(context = args.context, 
            name = 'sunrise',
            startTime = sun['dawn'] + datetime.timedelta(minutes = -20), 
            endTime = sun['sunrise'] + datetime.timedelta(minutes = +20),
            intervalSeconds = 90,
            tweetText = "Morning!")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            args.context.scheduler.add(task)


