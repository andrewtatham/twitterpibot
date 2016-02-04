from apscheduler.triggers.cron import CronTrigger
import twitterpibot.processing.MyAstral as MyAstral

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.processing.Timelapse import Timelapse


class SunTimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(hour=3)

    def on_run(self):
        sun = MyAstral.get_today_times()

        timelapse = Timelapse(
            name='sun',
            start_time=sun['dawn'],
            end_time=sun['dusk'],
            interval_seconds=600,
            tweet_text="The cosmic ballet goes on...")

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            add(task)
