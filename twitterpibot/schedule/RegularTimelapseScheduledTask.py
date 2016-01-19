import random
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger
from twitterpibot.processing.Timelapse import Timelapse
import datetime

messages = [
    "Worst timelapse ever",
    "Isn't greyscale ideal for sky timelapses?",
    "I should put some tranquil piano music over this",
    "Why do all timelapses have dubstep music on them?",
    "Here's another"
]


class RegularTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour='*')

    def onRun(self):
        now = datetime.datetime.now()

        start = now + datetime.timedelta(hours=1)
        end = now + datetime.timedelta(hours=2)

        timelapse = Timelapse(
            name='timelapse%s' % start.hour(),
            start_time=start,
            end_time=end,
            interval_seconds=60,
            tweet_text=random.choice(messages))

        from twitterpibot.schedule.MySchedule import add
        tasks = timelapse.GetScheduledTasks()
        for task in tasks:
            add(task)
