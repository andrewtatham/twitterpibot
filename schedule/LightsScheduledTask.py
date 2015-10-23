from ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import hardware

class LightsScheduledTask(ScheduledTask):
    def GetTrigger(args):
        return IntervalTrigger(minutes = 1)
    def onRun(args):
        print("LightsScheduledTask")
        hardware.OnLightsScheduledTask()
       
