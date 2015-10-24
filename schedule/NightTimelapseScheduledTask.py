from ScheduledTask import ScheduledTask
from MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from Timelapse import Timelapse
import datetime

class NightTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour = 18, minute = 1) 

    def onRun(self):


        astral = MyAstral()
        today = astral.GetTimes()
        tommorrow = astral.GetTommorrowTimes()

        timelapse = Timelapse(
            name = 'night',
            startTime = today['sunset'], 
            endTime = tommorrow['sunrise'],
            intervalSeconds = 600,
            tweetText = "The cosmic ballet goes on...")

        from MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)


