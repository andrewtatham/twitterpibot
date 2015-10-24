from Task import Task
from apscheduler.triggers.cron import CronTrigger
import datetime


class ScheduledTask(Task):

    def GetTrigger(self):
        return CronTrigger(second = (datetime.datetime.now().second + 10) % 60)