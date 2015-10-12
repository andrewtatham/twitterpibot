from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger

import Users


class UserListsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(minute="5/15")


    def onRun(args):
        Users.updateLists()

       