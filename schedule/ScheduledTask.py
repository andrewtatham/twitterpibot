from Task import Task

from apscheduler.triggers import *

class ScheduledTask(Task):

    def GetTrigger(args):
        return None