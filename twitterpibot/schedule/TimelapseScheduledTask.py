import datetime

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot import schedule
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.logic.Timelapse import Timelapse


class TimelapseScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=9)

    def on_run(self):
        now = datetime.datetime.now()
        timelapse = Timelapse(
            identity=self.identity,
            name='now',
            start_time=now + datetime.timedelta(seconds=1),
            end_time=now + datetime.timedelta(seconds=8),
            interval_seconds=1,
            tweet_text="")

        tasks = timelapse.get_scheduled_tasks()
        for task in tasks:
            schedule.add(task)
