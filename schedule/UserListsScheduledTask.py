from ScheduledTask import ScheduledTask
from MyTwitter import MyTwitter
import os
from UserList import UserList
import logging
from apscheduler.triggers.cron import CronTrigger


class UserListsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return CronTrigger(minute="5/15")

    def onInit(args):
        args.UpdateUserLists()


    def onRun(args):
        args.UpdateUserLists()


    def UpdateUserLists(args):
        args.context.users.updateLists()