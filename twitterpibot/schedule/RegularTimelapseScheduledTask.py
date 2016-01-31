import random

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.processing import MyAstral
from twitterpibot.schedule.ScheduledTask import ScheduledTask
from twitterpibot.processing.Timelapse import Timelapse

messages = [
    "Worst timelapse ever",
    "Isn't greyscale ideal for sky timelapses?",
    "I should put some tranquil piano music over this",
    "Why do all timelapses have dubstep music on them?",
    "Here's another"
]


class RegularTimelapseScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(hour='3')

    def onRun(self):
        n = 20

        sun = MyAstral.get_today_times()

        dawn = sun['dawn']
        dusk = sun['dusk']
        delta = (dusk - dawn) / n

        for i in range(n):
            start = dawn + delta * i
            end = dawn + delta * (i + 1)

            timelapse = Timelapse(
                name='timelapse%s' % i,
                start_time=start,
                end_time=end,
                interval_seconds=120,
                tweet_text=random.choice(messages))

            import twitterpibot.schedule.MySchedule as Schedule
            tasks = timelapse.GetScheduledTasks()
            for task in tasks:
                Schedule.add(task)
