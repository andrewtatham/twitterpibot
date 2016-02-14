import datetime
import abc

from apscheduler.triggers.cron import CronTrigger

from twitterpibot.tasks.Task import Task


class ScheduledTask(Task):

    @abc.abstractmethod
    def get_trigger(self):
        return CronTrigger(second=(datetime.datetime.now().second + 10) % 60)
