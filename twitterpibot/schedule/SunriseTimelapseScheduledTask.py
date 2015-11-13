import twitterpibot.processing.MyAstral as MyAstral
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime


class SunriseTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour=3)

    def onRun(self):
        sun = MyAstral.get_today_times()

        timelapse = Timelapse(
            name='sunrise',
            start_time=sun['dawn'] + datetime.timedelta(minutes=-20),
            end_time=sun['sunrise'] + datetime.timedelta(minutes=+20),
            interval_seconds=90,
            tweet_text="Morning!")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
