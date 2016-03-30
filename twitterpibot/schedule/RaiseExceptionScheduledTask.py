import random

from apscheduler.triggers.interval import IntervalTrigger

from twitterpibot import exceptionmanager
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class RaiseExceptionScheduledTask(ScheduledTask):
    def get_trigger(self):
        return IntervalTrigger(minutes=1)

    def on_run(self):
        exceptionmanager.raise_test_exception()
