from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import hardware

class LightsScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(minutes = 1)
    def onRun(self):
        hardware.OnLightsScheduledTask()
       
