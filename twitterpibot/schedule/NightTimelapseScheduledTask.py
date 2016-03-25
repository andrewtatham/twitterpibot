from apscheduler.triggers.cron import CronTrigger

from twitterpibot import schedule
from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.logic.MyAstral as MyAstral
from twitterpibot.logic.Timelapse import Timelapse


class NightTimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=15)

    def on_run(self):
        today = MyAstral.get_today_times()
        tomorrow = MyAstral.get_tomorrow_times()

        timelapse = Timelapse(
            identity=self.identity,
            name='night',
            start_time=today['sunset'],
            end_time=tomorrow['sunrise'],
            interval_seconds=600,
            tweet_text="The cosmic ballet goes on...")

        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            schedule.add(task)
