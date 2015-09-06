from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
import datetime
class SunsetTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(hour=15,minute=0)


    def onRun(args):

        sun = MyAstral().GetTimes()

        timelapse = Timelapse(
            context = args.context, 
            name = 'sunset',
            startTime = sun['sunset'] + datetime.timedelta(hours = -1), 
            endTime = sun['dusk'] + datetime.timedelta(hours = +1),
            intervalSeconds = 30,
            tweetText = "Goodnight!")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            args.context.scheduler.add(task)

