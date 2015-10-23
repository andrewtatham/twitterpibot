from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import hardware

class LightsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return IntervalTrigger(minutes = 3)
    def onRun(args):
        hardware.OnLightsScheduledTask()
       
