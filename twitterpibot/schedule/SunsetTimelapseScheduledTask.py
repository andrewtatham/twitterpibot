import twitterpibot.processing.MyAstral as MyAstral
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime


class SunsetTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=15)

    def onRun(self):
        sun = MyAstral.get_today_times()

        timelapse = Timelapse(
            name='sunset',
            start_time=sun['sunset'] + datetime.timedelta(minutes=-20),
            end_time=sun['dusk'] + datetime.timedelta(minutes=+20),
            interval_seconds=90,
            tweet_text="Goodnight!")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
