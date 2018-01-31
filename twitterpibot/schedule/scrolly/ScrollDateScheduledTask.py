import datetime

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.hardware import myperipherals
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class ScrollDateScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ScrollDateScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return CronTrigger(minute="*/15")

    def on_run(self):
        myperipherals.myscrollhat.enqueue(datetime.datetime.now().strftime("%A"))
        myperipherals.myscrollhat.enqueue(datetime.datetime.now().strftime("%d %b %Y"))