from Task import Task

from apscheduler.triggers import *
from apscheduler.triggers.cron import CronTrigger
import datetime
from TwitterHelper import Send, ReplyWith


class ScheduledTask(Task):

    def GetTrigger(args):
        return CronTrigger(second = datetime.datetime.now().second + 5)