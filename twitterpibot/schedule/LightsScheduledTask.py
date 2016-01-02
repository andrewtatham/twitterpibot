from twitterpibot.schedule.ScheduledTask import ScheduledTask
from apscheduler.triggers.interval import IntervalTrigger
import twitterpibot.hardware.hardware as hardware


class LightsScheduledTask(ScheduledTask):
    def GetTrigger(self):
        return IntervalTrigger(minutes=3)

    def onRun(self):
        hardware.on_lights_scheduled_task()
