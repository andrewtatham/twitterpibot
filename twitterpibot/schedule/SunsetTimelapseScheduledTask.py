from ScheduledTask import ScheduledTask
from twitterpibot.processing.MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime


class SunsetTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=15, minute=0)

    def onRun(self):
        sun = MyAstral().GetTimes()

        timelapse = Timelapse(
            name='sunset',
            startTime=sun['sunset'] + datetime.timedelta(minutes=-20),
            endTime=sun['dusk'] + datetime.timedelta(minutes=+20),
            intervalSeconds=90,
            tweetText="Goodnight!")

        from MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
