import twitterpibot
import twitterpibot.processing.MyAstral as MyAstral
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime


class SunsetTimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=15)

    def on_run(self):
        sun = MyAstral.get_today_times()

        timelapse = Timelapse(
            identity=self.identity,
            name='sunset',
            start_time=sun['sunset'] + datetime.timedelta(minutes=-20),
            end_time=sun['dusk'] + datetime.timedelta(minutes=+20),
            interval_seconds=90,
            tweet_text="Goodnight!")


        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            twitterpibot.schedule.add(task)
