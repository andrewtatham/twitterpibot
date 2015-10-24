from ScheduledTask import ScheduledTask
from apscheduler.triggers.cron import CronTrigger

import Users


class UserListsScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return CronTrigger(minute="5/15")


    def onRun(self):
        Users.updateLists()

       