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
            name = 'sunset',
            startTime = sun['sunset'] + datetime.timedelta(minutes = -20), 
            endTime = sun['dusk'] + datetime.timedelta(minutes = +20),
            intervalSeconds = 90,
            tweetText = "Goodnight!")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            scheduler.add(task)

