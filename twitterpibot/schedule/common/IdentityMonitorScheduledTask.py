from apscheduler.triggers.cron import CronTrigger
from twitterpibot.schedule.ScheduledTask import ScheduledTask

__author__ = 'andrewtatham'


class IdentityMonitorScheduledTask(ScheduledTask):
    def get_trigger(self):
        return CronTrigger(minute='*/15')

    def on_run(self):
        self.identity.conversations.housekeep()
