import twitterpibot.processing.MyAstral as MyAstral
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime


class SunsetTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=15)

    def onRun(self):
        sun = MyAstral.GetTimes()

        timelapse = Timelapse(
            name='sunset',
            startTime=sun['sunset'] + datetime.timedelta(minutes=-20),
            endTime=sun['dusk'] + datetime.timedelta(minutes=+20),
            intervalSeconds=90,
            tweetText="Goodnight!")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
