from apscheduler.triggers.cron import CronTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
import twitterpibot.processing.MyAstral as MyAstral
from twitterpibot.processing.Timelapse import Timelapse


class NightTimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=15)

    def on_run(self):
        today = MyAstral.get_today_times()
        tomorrow = MyAstral.get_tomorrow_times()

        timelapse = Timelapse(
            name='night',
            start_time=today['sunset'],
            end_time=tomorrow['sunrise'],
            interval_seconds=600,
            tweet_text="The cosmic ballet goes on...")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            add(task)
