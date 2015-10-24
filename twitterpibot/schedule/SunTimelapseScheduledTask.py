from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
import datetime

class SunTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour = 3, minute = 1) 

    def onRun(self):

        sun = MyAstral().GetTimes()

        timelapse = Timelapse(
            name = 'sun',
            startTime = sun['dawn'], 
            endTime = sun['dusk'],
            intervalSeconds = 600,
            tweetText = "The cosmic ballet goes on...")

        from MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)


