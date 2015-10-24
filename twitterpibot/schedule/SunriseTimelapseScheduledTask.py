from ScheduledTask import ScheduledTask
from twitterpibot.processing.MyAstral import MyAstral
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime


class SunriseTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=3, minute=0)

    def onRun(self):
        sun = MyAstral().GetTimes()

        timelapse = Timelapse(
            name='sunrise',
            startTime=sun['dawn'] + datetime.timedelta(minutes=-20),
            endTime=sun['sunrise'] + datetime.timedelta(minutes=+20),
            intervalSeconds=90,
            tweetText="Morning!")

        from MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)