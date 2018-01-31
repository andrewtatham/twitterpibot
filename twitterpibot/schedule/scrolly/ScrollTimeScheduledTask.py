import datetime

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.hardware import myperipherals
from twitterpibot.schedule.ScheduledTask import ScheduledTask


class ScrollTimeScheduledTask(ScheduledTask):
    def __init__(self, identity):
        super(ScrollTimeScheduledTask, self).__init__(identity)

    def get_trigger(self):
        return CronTrigger(minute="*/5")

    def on_run(self):
        myperipherals.myscrollhat.jump_queue(datetime.datetime.now().strftime("%H:%M"))


