import datetime
from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.processing.Timelapse import Timelapse
import twitterpibot.schedule.MySchedule as MySchedule


class TimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(minutes=9)

    def onRun(self):
        now = datetime.datetime.now()
        timelapse = Timelapse(
            name='now',
            start_time=now + datetime.timedelta(seconds=1),
            end_time=now + datetime.timedelta(seconds=8),
            interval_seconds=1,
            tweet_text="")

        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            MySchedule.add(task)
