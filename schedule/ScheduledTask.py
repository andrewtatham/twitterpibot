from Task import Task
from apscheduler.triggers.cron import CronTrigger
import datetime


class ScheduledTask(Task):

    def GetTrigger(args):
        return CronTrigger(second = datetime.datetime.now().second + 5)